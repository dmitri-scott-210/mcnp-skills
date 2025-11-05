#!/usr/bin/env python
# ==================================================================================================
"""Script to setup, run, postprocess and analyze laqgsm validation test problems"""


# ==================================================================================================
# Load standard python modules
import logging
import os
import sys

from matplotlib.collections import PolyCollection
import numpy as np

logging.basicConfig(level=logging.INFO)
FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(1, os.path.join(FILE_PATH, "..", "..", "support"))


# ==================================================================================================
# Load local python modules
import mcnpvnv
import vnv
from vnv.plotndoc import LatexString


# ==================================================================================================
# Module-level variables
PATH = os.getcwd()
NAME = "validation laqgsm"
BENCHMARKS_DIR = "experiments"
CALCULATIONS_DIR = "calculations"
DOCUMENTS_DIR = "documents"
BENCHMARKS_PATH = os.path.join(FILE_PATH, BENCHMARKS_DIR)
CALCULATIONS_PATH = os.path.join(PATH, CALCULATIONS_DIR)
DOCUMENTS_PATH = os.path.join(PATH, DOCUMENTS_DIR)
ALL_TESTS = vnv.build_dir_list(BENCHMARKS_PATH, name_only=True)

# ==================================================================================================
# Local laqgsm VnV-specific functions
def collect_benchmark_results(benchmarks, results, label):
    """Unique information and data retrieval from the benchmarks dictionaries (JSON).
    Returns a general data object along with a value/uncertainty map.
    """

    val = label + " Val."
    unc = label + " Unc."

    data = {
        "Name": [benchmark.info["general_info"]["name"] for benchmark in benchmarks],
        "Material": [
            benchmark.info["general_info"]["details"]["material"]
            for benchmark in benchmarks
        ],
        "Energy": [
            benchmark.info["general_info"]["details"]["energy"]
            for benchmark in benchmarks
        ],
        "Type": [
            benchmark.info["general_info"]["details"]["type"]
            for benchmark in benchmarks
        ],
        "Angle": [
            benchmark.info["general_info"]["details"]["angle"]
            for benchmark in benchmarks
        ],
        "FMR": [
            benchmark.info["general_info"]["details"]["fmr"] for benchmark in benchmarks
        ],
        "FMR Index": [
            benchmark.info["general_info"]["details"]["fmr_index"]
            for benchmark in benchmarks
        ],
        val: [benchmark.info[results]["tally"]["val"] for benchmark in benchmarks],
        unc: [benchmark.info[results]["tally"]["err"] for benchmark in benchmarks],
    }
    vumap = {"val": val, "unc": unc}

    return data, vumap


# ==================================================================================================
# Local general functions
def list_tests(tests=ALL_TESTS):
    """List all available tests in benchmark suite."""

    print("All available tests in {}:".format(NAME))
    for test in tests:
        print("  {}".format(test))


def setup_calc(calc_name, tests=ALL_TESTS):
    """Setup unique calculation directory with selected tests within the benchmark suite."""

    _ = vnv.benchcalc.setup_benchmark_suite_calc_directory(
        BENCHMARKS_PATH, CALCULATIONS_PATH, calc_name, tests
    )


def exec_slurm(config):
    """Generate a Slurm sbatch script, run it, and wait for the results."""

    calc_path = os.path.join(CALCULATIONS_PATH, config.calcdir_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    n_runs = len(bench_names)

    slurm_ctl = vnv.slurmin.SlurmManager(
        config.calcdir_name,
        config.executable_name,
        FILE_PATH,
        CALCULATIONS_PATH,
        n_runs,
        config.jobs,
        config.stride,
        config.ntrd,
        config.mpi_provider,
        config.nmpi,
        config.nodes,
        config.time,
        config.pre_cmd,
        config.post_cmd,
        config.clopts,
    )
    slurm_ctl.generate_sbatch()
    slurm_ctl.execute()
    if config.wait:
        slurm_ctl.wait()


def exec_calc(config):
    """Execute an already setup calculation with some execution-specific information provided."""

    calc_path = os.path.join(CALCULATIONS_PATH, config.calcdir_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    if config.run_index is not None:
        if config.run_index >= len(bench_names):
            sys.exit(
                """
Error: run_index ({}) is greater than the index of the last problem ({})
""".format(
                    config.run_index, len(bench_names) - 1
                )
            )
        bench_names = bench_names[config.run_index : config.run_index + config.stride]

    benchmarks = [
        mcnpvnv.build_mcnp_benchmark(
            calc_path,
            bench_name,
            executable=config.executable_name,
            mpi_provider=config.mpi_provider,
            nodes=config.nodes,
            nmpi=config.nmpi,
            ntrd=config.ntrd,
        )
        for bench_name in bench_names
    ]

    vnv.commandline.execute(benchmarks, config.jobs)


def calc_invariant(x, y, dy, m, i=1, j=-1):
    """Calculate invariant cross section and associated momentum domain.  The
    `i` and `j` indices are used to downselect to a preferred region in the
    domain, which was done in the original LAQGSM suite where some extreme
    energies were ignored.  Note that in some cases `i` and `i-1` are needed to
    specify the range because of bin-edge versus bin-width off-by-one indexing
    to ensure that vectors are a consistent length."""

    # Calculate average energy and energy bin width for each bin.
    e_avg = 0.5 * (x[:-1] + x[1:])
    de = np.diff(x)[i - 1 : j]

    x = np.sqrt((e_avg + m) ** 2 - m ** 2)[i - 1 : j]
    y = y[i:j] / (x * de)
    dy = y * dy[i:j]

    return x, y, dy


def post_calc(calc_name):
    """Postprocess an already executed calculation."""

    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]

    for b in benchmarks:
        output = b.get_file("outputs", "mctal")

        code, vers, date = mcnpvnv.get_code_version_from_mctal(output)
        b.info["calculation_info"] = {
            "code": code,
            "version": vers,
            "date": date,
        }

        # Because different types of experiments are considered, their
        # processing is controlled here for those different types, as designated
        # by their "experiment_type" in the accompanying JSON file.
        if (
            b.info["general_info"]["experiment_type"]
            == "double-differential cross-section measurement"
        ):
            bins, val, err = mcnpvnv.get_tally_from_mctal(
                output,
                1,
                abscissa_id=(
                    "facet",
                    "flag",
                    "user",
                    "seg",
                    "mult",
                    "cosine",
                    "energy",
                    "time",
                ),
            )
            angles = b.info["general_info"]["angles"]
            b.info["calculation_data"] = {}
            for k, v in angles.items():
                b.info["calculation_data"][k] = {}
                b.info["calculation_data"][k]["Energy"] = {
                    "Values": bins[6],
                    "Units": "MeV",
                }
                s = v["tally_segment"]
                values = val[0, 0, 0, s, 0, 0, :, 0]
                errors = err[0, 0, 0, s, 0, 0, :, 0]
                uncertainties = values * errors
                b.info["calculation_data"][k]["Cross Section"] = {
                    "Values": values.tolist(),
                    "Uncertainty": uncertainties.tolist(),
                }

        # For this type of calculation, the domain (energy) needs to be
        # converted to momentum, which is then used to normalize the result.
        elif (
            b.info["general_info"]["experiment_type"]
            == "invariant cross-section measurement"
        ):
            bins, val, err = mcnpvnv.get_tally_from_mctal(
                output,
                1,
                abscissa_id=(
                    "facet",
                    "flag",
                    "user",
                    "seg",
                    "mult",
                    "cosine",
                    "energy",
                    "time",
                ),
            )
            angles = b.info["general_info"]["angles"]
            b.info["calculation_data"] = {}
            for k, v in angles.items():
                e_bins = np.array(bins[6])
                s = v["tally_segment"]
                values = np.array(val[0, 0, 0, s, 0, 0, :, 0])
                errors = np.array(err[0, 0, 0, s, 0, 0, :, 0])

                # Convert domain from energy to momentum and range from
                # double-differential cross section to invariant.
                m_d = b.info["general_info"]["projectile_mass"]
                e_bins, values, uncertainties = calc_invariant(
                    e_bins, values, errors, m_d
                )

                b.info["calculation_data"][k] = {}
                b.info["calculation_data"][k]["Energy"] = {
                    "Values": e_bins.tolist(),
                    "Units": "MeV",
                }
                b.info["calculation_data"][k]["Cross Section"] = {
                    "Values": values.tolist(),
                    "Uncertainty": uncertainties.tolist(),
                }

        b.write_description_info()


def __apply_plot_params(myplot, plot_params):
    """Apply matplotlib plotting parameters to a plot axis within the myplot
    object, if so defined in the `description.json` file.  This is particularly
    useful for the LAQGSM suite because of x axes that do not span the entire
    range of available data."""
    for k, v in plot_params.items():
        if k == "xlim":
            myplot.ax.set_xlim(**v)
        elif k == "ylim":
            myplot.ax.set_ylim(**v)
        else:
            raise ValueError(f"Unexpected plot parameter entry: {k}.")
    return myplot


def doc_calc(calc_name, compare_calcs, plot_alt_code_results=False):
    """Document an already postprocessed calculation.  Generates txt, LaTeX, and
    PDF plots.  Because the LAQGSM data are too voluminous to be written to
    tables in a meaningful way, only graphics are currently produced."""

    if len(compare_calcs) > 0:
        sys.stdout.write(
            "\nWarning: calculation comparison capability unavailable at this time.\n"
        )

    doc_path = vnv.plotndoc.setup_benchmark_suite_docs_directory(
        DOCUMENTS_PATH, calc_name
    )
    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [mcnpvnv.MCNPBenchmark(calc_path, name) for name in bench_names]

    plots_to_document = {}
    for b in benchmarks:
        logging.debug(f"Plotting {b.name}...")
        angles = b.info["general_info"]["angles"]
        myplot = vnv.plotndoc.ResultPlot((8.5 / 1.62, 8.5), use_latex=True)
        plots_to_document[b.name] = b.info["general_info"]
        for angle, v in angles.items():
            logging.debug(f"  for angle {angle} degrees...")
            calc_label = LatexString("Calc. +/- 1-sigma", "Calc. $\\pm1\\sigma$")
            exp_label = LatexString(
                f"{angle} deg.",
                f"{angle}$^{{\\circ}}$ ($\\times10^{{{np.log10(v['multiplier']):.0f}}}$)",
            )

            # Read experimental values.
            exp_x = np.array(b.info["experiment_data"][angle]["Energy"]["Values"])
            exp_dx = np.array(b.info["experiment_data"][angle]["Energy"]["Uncertainty"])
            exp_y = np.array(
                b.info["experiment_data"][angle]["Cross Section"]["Values"]
            )
            exp_dy = np.array(
                b.info["experiment_data"][angle]["Cross Section"]["Uncertainty"]
            )

            # Read calculation data.
            calc_x = np.array(b.info["calculation_data"][angle]["Energy"]["Values"])
            calc_y = np.array(
                b.info["calculation_data"][angle]["Cross Section"]["Values"]
            )
            calc_dy = np.array(
                b.info["calculation_data"][angle]["Cross Section"]["Uncertainty"]
            )

            # Manipulate data to be distinguishable.
            exp_y *= v["multiplier"]
            exp_dy *= v["multiplier"]
            calc_y *= v["multiplier"]
            calc_dy *= v["multiplier"]

            # Normalize calculated data by energy-bin width.
            if (
                b.info["general_info"]["experiment_type"]
                == "double-differential cross-section measurement"
            ):
                calc_x, calc_y, calc_dy = normalize_by_energy(calc_x, calc_y, calc_dy)

            # Apply scalar to convert units, if needed.
            if (
                b.info["general_info"]["experiment_type"]
                == "invariant cross-section measurement"
                and b.info["experiment_data"][angle]["Cross Section"]["Units"]
                == "mb/GeV^2/sr"
            ):
                calc_y *= 1e6
                calc_dy *= 1e6

            myplot.plot_discrete(
                exp_x, exp_y, indep_err=exp_dx, dep_err=exp_dy, label=exp_label,
            )

            # Only label one data series for the calculation.
            myplot.plot_step(calc_x, calc_y, dep_err=calc_dy, color="#000000")

            # Plot alternative code data.
            code_line_colors = [
                "#1b9e77",
                "#d95f02",
                "#7570b3",
                "#e7298a",
                "#66a61e",
                "#e6ab02",
                "#a6761d",
                "#666666",
            ]
            if plot_alt_code_results and b.info.get("alt_code_data", False):
                for code_name, angles in b.info["alt_code_data"].items():
                    linecolor = code_line_colors.pop()
                    alt_code_x = np.array(
                        b.info["alt_code_data"][code_name][angle]["Energy"]["Values"]
                    )
                    alt_code_y = np.array(
                        b.info["alt_code_data"][code_name][angle]["Cross Section"][
                            "Values"
                        ]
                    )

                    # Incorporate scaling multiplier.
                    alt_code_y *= v["multiplier"]

                    # Perform energy unit conversions, as necessary.
                    if (
                        b.info["alt_code_data"][code_name][angle]["Energy"]["Units"]
                        == "GeV"
                    ):
                        alt_code_x *= 1000.0
                    if (
                        b.info["alt_code_data"][code_name][angle]["Cross Section"][
                            "Units"
                        ]
                        == "mb/GeV/sr"
                    ):
                        alt_code_y /= 1000.0

                    # Only label one data series for the calculation.
                    label = code_name if angle == sorted(angles.keys())[-1] else None
                    myplot.plot_step(
                        alt_code_x, alt_code_y, ls="--", color=linecolor, label=label
                    )

        # Replot the last calculated series to force a (single) legend entry.
        myplot.plot_step(
            calc_x, calc_y, dep_err=calc_dy, color="#000000", label=calc_label
        )

        # Remove edges from uncertainty bands made with fill_between.
        for pc in myplot.ax.findobj(match=PolyCollection):
            pc.set(color="#000000", edgecolor="none", linewidth=0)

        # Add final plot components.
        xlabel = LatexString(
            b.info["general_info"]["xlabel_latex"],
            b.info["general_info"]["xlabel_plain"],
        )
        ylabel = LatexString(
            b.info["general_info"]["ylabel_latex"],
            b.info["general_info"]["ylabel_plain"],
        )
        myplot.ax.set_xlabel(xlabel)
        myplot.ax.set_ylabel(ylabel)
        myplot.ax.set_yscale("log")
        myplot.ax.set_xscale("log")
        plot_params = b.info["general_info"].get("plot_params", False)
        if plot_params:
            myplot = __apply_plot_params(myplot, plot_params)
        myplot.save(os.path.join(doc_path, f"{b.name}.pdf"))

    doc_calc_laqgsm(plots_to_document, doc_path)


def clean_calc(calc_name):
    """Cleaning up a specific calculation or the entire calculations directory."""

    if os.path.exists(os.path.join(CALCULATIONS_PATH, calc_name)):
        vnv.clean(CALCULATIONS_PATH, calc_name)
    else:
        vnv.clean(CALCULATIONS_PATH)


# ==================================================================================================
# Local laqgsm VnV-specific functions


def normalize_by_energy(x, y, dy, start=1, end=-5):
    """Normalize a response by energy-bin width with some truncation at low and high energies."""
    y = y[start:end] / np.diff(x)[start - 1 : end]
    dy = dy[start:end] / np.diff(x)[start - 1 : end]
    x = x[start - 1 : end - 1]
    return x, y, dy


def doc_calc_laqgsm(plots_to_document, doc_path):
    r"""Document the LAQGSM suite results.  A minimal functional container
    LaTeX file is:

    \documentclass{article}
    \usepackage{booktabs}
    \usepackage{embedfile}
    \usepackage[margin=1in]{geometry}
    \usepackage{graphicx}
    \usepackage{hyperref}
    \usepackage{listings}
    \begin{document}
    \input{.../results.tex}
    \end{document}
    """

    outfilename = os.path.join(doc_path, "results.tex")
    logging.info("Writing documentation file...")
    f = open(outfilename, "w")
    f.write("\\providecommand\\includepath{.}\n")

    for name, general_info in plots_to_document.items():
        title = general_info["name_section"]
        label = f"fig:{name}"

        logging.debug(f"Making remarks for {name}")
        f.write(f"\n\\subsubsection{{{title}}}\n\n")
        f.write(
            f"This experiment is a {general_info['experiment_type']}. Historically, calculated and experimental results were compared visually, and that is the approach provided here such that no additional measures of agreement are provided.  The results are shown in Fig.~\\ref{{{label}}}.\n\n"
        )

        logging.debug(f"Incorporating figure {name}")
        infilename = f"{{{name}}}.pdf"
        f.write("\\begin{figure}[p]\n")
        f.write("  \\begin{center}\n")
        f.write(f"    \\includegraphics{{\\includepath/{infilename}}}\n")
        f.write(f"    \\caption{{{title}\\label{{{label}}}}}\n")
        f.write("  \\end{center}\n")
        f.write("\\end{figure}\n")

        f.write("\\clearpage\n")
        f.write("\n")

    f.close()


# ===============================================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    parser, command_args = vnv.commandline.build_command_line_parser(ALL_TESTS)
    args = vnv.commandline.parse_and_check_args(parser, ALL_TESTS)

    if args.command == "list":
        list_tests(ALL_TESTS)

    if args.command == "setup":
        setup_calc(args.calcdir_name, args.tests)

    if args.command == "execute_slurm":
        exec_slurm(args)

    if args.command == "execute":
        exec_calc(args)

    if args.command == "postprocess":
        post_calc(args.calcdir_name)

    if args.command == "document":
        doc_calc(args.calcdir_name, args.compare)

    if args.command == "clean":
        clean_calc(args.calcdir_name)
