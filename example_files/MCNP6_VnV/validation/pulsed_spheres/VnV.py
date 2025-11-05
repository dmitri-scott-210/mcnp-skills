#!/usr/bin/env python3
# ==================================================================================================
"""Script to setup, run, postprocess and analyze pulsed sphere validation test problems"""


# ==================================================================================================
# Load standard python modules
import copy
import os
import re
import shutil
import sys
import textwrap


FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(1, os.path.join(FILE_PATH, "..", "..", "support"))


# ==================================================================================================
# Load local python modules
import mcnpvnv
import vnv


# ==================================================================================================
# Module-level variables
PATH = os.getcwd()
NAME = "validation pulsed sphere"
BENCHMARKS_DIR = "experiments"
CALCULATIONS_DIR = "calculations"
DOCUMENTS_DIR = "documents"
BENCHMARKS_PATH = os.path.join(FILE_PATH, BENCHMARKS_DIR)
CALCULATIONS_PATH = os.path.join(PATH, CALCULATIONS_DIR)
DOCUMENTS_PATH = os.path.join(PATH, DOCUMENTS_DIR)
ALL_TESTS = vnv.build_dir_list(BENCHMARKS_PATH, name_only=True)


# ==================================================================================================
# Local pulsed sphere VnV-specific functions
def collect_benchmark_results(benchmarks, results, label):
    """Unique information and data retrieval from the benchmarks dictionaries (JSON).
    Returns a general data object along with a value/uncertainty map.
    """

    abscissa = label + " abscissa"
    val = label + " val."
    unc = label + " unc."

    data = {
        "Name": [benchmark.info["general_info"]["name"] for benchmark in benchmarks],
        "CSG Model": [
            benchmark.info["general_info"]["details"]["CSG_model"]
            for benchmark in benchmarks
        ],
        "Material": [
            benchmark.info["general_info"]["details"]["sphere_material"]
            for benchmark in benchmarks
        ],
        "Thickness": [
            benchmark.info["general_info"]["details"]["sphere_thickness"]
            + " "
            + benchmark.info["general_info"]["details"]["units_sphere_thickness"]
            for benchmark in benchmarks
        ],
        "Flight Distance": [
            benchmark.info["general_info"]["details"]["flight_distance"]
            + " "
            + benchmark.info["general_info"]["details"]["units_flight_distance"]
            for benchmark in benchmarks
        ],
        "Degrees Off Axis": [
            benchmark.info["general_info"]["details"]["degrees_off_axis"]
            for benchmark in benchmarks
        ],
        abscissa: [
            benchmark.info[results]["neutron_time-of-flight"]["abscissa"]
            for benchmark in benchmarks
        ],
        val: [
            benchmark.info[results]["neutron_time-of-flight"]["val"]
            for benchmark in benchmarks
        ],
        unc: [
            benchmark.info[results]["neutron_time-of-flight"]["rel_std"]
            for benchmark in benchmarks
        ],
    }

    vumap = {"val": val, "unc": unc}

    return data, vumap


# Helper function to produce a plot of the neutron time of flight spectra for
# each a sphere material with detailed CSG, legacy CSG, and experimental
# results plotted together
# Returns two strings, the name of the file produced and an appropriate caption
def plot_pulsed_sphere(bench_dicts, mat, plot_path):

    from matplotlib import pyplot as plt

    # Adds a step plot with errorbars to the axes with data from the dictionary
    # Corresponding keys of the dictionary are mapped to fixed values with the
    # key_map
    def plot_step_errorbar(axes, bench_dict, key_map):
        if key_map["data"] == "exp":
            x_vals = list(map(lambda x: x * 10, bench_dict[key_map["x"]][:-1]))
        else:
            x_raw_vals = list(map(lambda x: x * 10, bench_dict[key_map["x"]]))
            x_step = (x_raw_vals[1] - x_raw_vals[0]) / 2
            x_vals = [x_raw_vals[i] + x_step for i in range(len(x_raw_vals) - 1)]
        y_vals = bench_dict[key_map["y"]][1:]
        y_err_vals = bench_dict[key_map["err"]][1:]

        axes.step(
            x_vals,
            y_vals,
            where="mid",
            label=key_map["label"],
            color=key_map["color"],
            lw=0.5,
        )
        axes.errorbar(
            x_vals,
            y_vals,
            fmt="none",
            ecolor=key_map["color"],
            capthick=0.5,
            capsize=1,
            elinewidth=0.5,
            yerr=[y_err_vals[i] * y_vals[i] for i in range(len(y_vals))],
        )
        return axes

    # Plot benchmark calc and exp results
    detailed, simple, exp = bench_dicts
    name = f"{mat}_results.pdf"
    outfilename = os.path.join(plot_path, name)
    _, ax = plt.subplots(1, 1, figsize=(6.5, 6.5 / 1.618))
    ax.set_yscale("log")
    ax.set_xlabel("Neutron Flight Time [ns]")
    ax.set_ylabel("Normalized Count Rate\n[counts / ns / total unshielded counts]")
    caption = textwrap.dedent(
        f"""
    Comparison of the measured and calculated normalized count rate
    of neutrons escaping from a {detailed["Thickness"]}
    thick sphere of {detailed["Material"]} plotted against flight time."""
    )
    ax = plot_step_errorbar(
        ax,
        detailed,
        {
            "x": "Calc. abscissa",
            "y": "Calc. val.",
            "err": "Calc. unc.",
            "color": "r",
            "label": "Detailed CSG Calc.",
            "data": "calc",
        },
    )
    ax = plot_step_errorbar(
        ax,
        simple,
        {
            "x": "Calc. abscissa",
            "y": "Calc. val.",
            "err": "Calc. unc.",
            "color": "b",
            "label": "Legacy CSG Calc.",
            "data": "calc",
        },
    )
    ax = plot_step_errorbar(
        ax,
        exp,
        {
            "x": "Exp. abscissa",
            "y": "Exp. val.",
            "err": "Exp. unc.",
            "color": "k",
            "label": "Experiment",
            "data": "exp",
        },
    )
    ax.legend()
    plt.savefig(outfilename, bbox_inches="tight", dpi=300)
    plt.close()
    return name, caption


def doc_calc_pulsed_spheres(names, data, maps, nuc_data, docs_path):

    import numpy as np

    # Unpack data and maps
    e_data, c_data = data
    e_map, c_map = maps

    # Copy of benchmark to be modified to calc / exp values and tabulated
    ce_data = copy.copy(c_data)
    ce_data.pop(c_map["val"])
    ce_data.pop(c_map["unc"])
    ce_data.pop("Calc. abscissa")
    ce_map = {"val": "C/E Val.", "unc": "C/E Unc. [%]"}

    # Form data structure for calc and exp data
    cbdata = vnv.plotndoc.CalcBenchData(
        "All", names, data=[e_data, c_data], vumap=[e_map, c_map], sort_by="Material",
    )

    # Form data structure for processed calc and exp data
    ce_ratio_data = vnv.plotndoc.CalcBenchData(
        "All", names, data=[ce_data], vumap=[ce_map], sort_by="Material"
    )
    # Add Calc./Exp. val. and unc. columns
    ce_ratio_data.df[0] = ce_ratio_data.df[0].reindex(
        [*list(ce_ratio_data.df[0].columns), *[ce_map["val"], ce_map["unc"]]], axis=1
    )

    # Create include directory for tables and plots
    include_dir = "include"
    include_path = os.path.relpath(os.path.join(docs_path, include_dir))
    if os.path.exists(include_path):
        shutil.rmtree(include_path)
    os.mkdir(include_path)

    # Creates a dictionary with dataframe columns as keys for a single
    # benchmark specified by the material and csg model
    def unpack_bench(all_bench_df, mat, csg):
        bench_df = all_bench_df.loc[
            (all_bench_df["Material"] == mat) & (all_bench_df["CSG Model"] == csg)
        ]
        # Enforce that one benchmark is uniquely identified
        if len(bench_df.index) != 1:
            sys.exit("Benchmark not uniquely identified by material and CSG model")
        bench_dict = {}
        for col in bench_df.columns:
            bench_dict[col] = bench_df[col][0]
        return bench_dict

    # Calculates the average ratio of calculation to benchmark values and
    # associated error
    def calc_ratio(calc_dict, exp_dict):
        ratio, err, _ = vnv.c_over_b(
            calc_dict["Calc. val."],
            list(np.array(calc_dict["Calc. val."]) * np.array(calc_dict["Calc. unc."])),
            exp_dict["Exp. val."],
            list(np.array(exp_dict["Exp. val."]) * np.array(exp_dict["Exp. unc."])),
        )
        return np.mean(ratio), 100 * np.sqrt(np.mean(np.square(err)))

    # Loop over all materials and process both CSG representations
    mats = set(cbdata.df[0]["Material"])
    plot_name_cap = {}
    for mat in mats:
        # Get benchmark data
        detailed = unpack_bench(cbdata.df[1], mat, "detailed")
        simple = unpack_bench(cbdata.df[1], mat, "simple")
        exp = unpack_bench(cbdata.df[0], mat, "simple")
        # Plot benchmark
        plot_name_cap[mat] = plot_pulsed_sphere(
            [detailed, simple, exp], mat, include_path
        )
        # Add average calculation over experiment ratio and error
        ce_ratio_data.df[0].loc[
            (ce_ratio_data.df[0]["Material"] == mat)
            & (ce_ratio_data.df[0]["CSG Model"] == "detailed"),
            [ce_map["val"], ce_map["unc"]],
        ] = calc_ratio(detailed, exp)
        ce_ratio_data.df[0].loc[
            (ce_ratio_data.df[0]["Material"] == mat)
            & (ce_ratio_data.df[0]["CSG Model"] == "simple"),
            [ce_map["val"], ce_map["unc"]],
        ] = calc_ratio(simple, exp)
    # Tabulate average ratio and error information into a table
    summary_table = (
        ce_ratio_data.df[0]
        .drop(["Name"], axis=1)
        .to_latex(
            index=False,
            index_names=False,
            column_format="ccccccc",
            formatters={
                ce_map["val"]: lambda x: f"{x:.4f}",
                ce_map["unc"]: lambda x: f"{x:.2f}",
            },
        )
    )
    sum_tab_name = "summary_table.tex"
    sum_tab_file = os.path.join(include_path, sum_tab_name)
    with open(sum_tab_file, "w") as f:
        f.write(summary_table)

    # Dictionary of comments on specific materials
    mat_specific_comments = {}
    mat_specific_comments["water"] = textwrap.dedent(
        f"""
    Note that the uncertainty in the average ratio of calculated to
    experimental time-of-flight results is calculated by propagating both the
    calculation result uncertainty and the experimental measurement
    uncertainty. From Fig.~\\ref{{fig:ps_water_res_{nuc_data}}} one sees more measurement
    uncertainty compared to other materials, this is the cause of the high
    average ratio uncertainty for this material.\n"""
    )

    # Write results file
    output_file = os.path.join(docs_path, "results.tex")
    with open(output_file, "w") as file:
        file.write("\\providecommand\\includepath{.}\n")

        # Opening remarks
        s = textwrap.dedent(
            f"""
        Results from neutron pulsed spheres of six different materials
        are presented. For each material, the neutron time-of-flight spectra
        calculated from both CSG models and measured experimentally are plotted
        together and the average ratio of calculation results over experimental
        results with the associated one-standard-deviation uncertainty is
        presented. Uncertainty  propagation is done with the assumption of
        normally distributed uncertainties. A summary for all sphere materials
        is given in Sec.~\\ref{{subsec:ps_summary_{nuc_data}}}.
        """
        )
        file.write(s)

        # Material specific remarks
        for mat in sorted(mats):
            # Get material specific values
            thickness = (
                ce_ratio_data.df[0]
                .loc[(ce_ratio_data.df[0]["Material"] == mat), ["Thickness"]]
                .to_numpy()[0][0]
            )
            detailed_val, detailed_err = (
                ce_ratio_data.df[0]
                .loc[
                    (ce_ratio_data.df[0]["Material"] == mat)
                    & (ce_ratio_data.df[0]["CSG Model"] == "detailed"),
                    [ce_map["val"], ce_map["unc"]],
                ]
                .to_numpy()[0]
            )
            simple_val, simple_err = (
                ce_ratio_data.df[0]
                .loc[
                    (ce_ratio_data.df[0]["Material"] == mat)
                    & (ce_ratio_data.df[0]["CSG Model"] == "simple"),
                    [ce_map["val"], ce_map["unc"]],
                ]
                .to_numpy()[0]
            )
            file.write(f"\n\\paragraph{{{mat.capitalize()}}}\n")
            mat_comment = textwrap.dedent(
                f"""
            The time-of-flight spectra for a {thickness} thick {mat} pulsed
            sphere modeled with legacy and detailed CSG is given in
Fig.~\\ref{{fig:ps_{mat}_res_{nuc_data}}}.
            The legacy model has an average ratio of calculation to measured
            results of ${simple_val:.4f}\\pm{simple_err:.2f}\\%$ and the
            detailed model has an average ratio of ${detailed_val:.4f}\\pm{detailed_err:.2f}\\%$.\n"""
            )
            if mat in mat_specific_comments:
                mat_comment += mat_specific_comments[mat]
            file.write(mat_comment)
            # Add time-of-flight spectra plot
            plot_name = os.path.join(include_dir, plot_name_cap[mat][0])
            file.write("\n\\begin{figure}[p]\n")
            file.write("  \\begin{center}\n")
            file.write(f"\\includegraphics{{\\includepath/{plot_name}}}\n")
            file.write(
                f"    \\caption{{{plot_name_cap[mat][1]}"
                + f"\\label{{fig:ps_{mat}_res_{nuc_data}}}}}\n"
            )
            file.write("  \\end{center}\n")
            file.write("\\end{figure}\n")

        file.write(f"\n\\paragraph{{Summary\\label{{subsec:ps_summary_{nuc_data}}}}}\n")
        summary = textwrap.dedent(
            f"""
        A summary of the experiment characteristics and the averaged
        calculation to experiment ratio is given for each benchmark in
        Table~\\ref{{tab:ps_sum_{nuc_data}}}.
        """
        )
        file.write(summary)
        # Write table with description of calculations
        sum_tab_rel_path = os.path.join(include_dir, sum_tab_name)
        file.write("\n\\begin{landscape}\n")
        file.write("  \\begin{table}[p]\n")
        file.write("    \\begin{center}\n")
        file.write(
            "      \\caption{{Characteristics and Calculation (C) to Experimental"
            + f" (E) Ratios of All Benchmarks\\label{{tab:ps_sum_{nuc_data}}}}}}}\n"
        )
        file.write(f"      \\input{{\\includepath/{sum_tab_rel_path}}}\n")
        file.write("    \\end{center}\n")
        file.write("  \\end{table}\n")
        file.write("\\end{landscape}")


# ==================================================================================================
# Local general functions
def list_tests(tests=ALL_TESTS):
    """List all available tests in benchmark suite."""

    print(f"All available tests in {NAME}:")
    for test in tests:
        print(f"  {test}")


def setup_calc(calc_name, tests, nuc_data):
    """Setup unique calculation directory with selected tests within the benchmark suite."""

    rewrite = [
        (
            re.compile("read(\s*)file=m-cards-endf71"),
            "read file=m-cards-{}".format(nuc_data),
        )
    ]

    calc_path = vnv.benchcalc.setup_benchmark_suite_calc_directory(
        BENCHMARKS_PATH, CALCULATIONS_PATH, calc_name, tests
    )

    bench_names = vnv.build_dir_list(calc_path, name_only=True)
    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]
    for benchmark in benchmarks:
        benchmark.rewrite_file("inputs", "inp", rewrite)
        benchmark.info["calculation_info"] = {"data": vnv.nuclear_data_label[nuc_data]}
        benchmark.write_description_info()


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
                f"""
Error: run_index ({config.run_index}) is greater than the index of the last
problem ({len(bench_names) - 1})
"""
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


def post_calc(calc_name):
    """Postprocess an already executed calculation."""

    import re

    # Removes a data point from concrete tally results because it is dropped
    # in the experimental data
    def prune_tally_results(time, val, err, bench_name):
        bench_to_prune = re.compile(".*conc")
        if bench_to_prune.match(bench_name) and 31.4 in time:
            idx_to_remove = time.index(31.4)
            time.pop(idx_to_remove)
            val.pop(idx_to_remove)
            err.pop(idx_to_remove)
        return time, val, err

    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]

    for benchmark in benchmarks:
        output = benchmark.get_file("outputs", "mctal")

        time, val, err = mcnpvnv.get_tally_from_mctal(output, 205, "time")
        time, val, err = prune_tally_results(time, val, err, benchmark.name)
        benchmark.info["calculation_data"] = {
            "neutron_time-of-flight": {
                "tally_id": 205,
                "abscissa_label": "Time [shakes]",
                "val_label": "Normalized Count Rate [counts / ns / total unshielded counts]",
                "abscissa": time,
                "val": val,
                "rel_std": err,
            }
        }

        code, version, date = mcnpvnv.get_code_version_from_mctal(output)
        code_version_date_dict = {"code": code, "version": version, "date": date}
        if "calculation_info" in benchmark.info:
            benchmark.info["calculation_info"].update(code_version_date_dict)
        else:
            benchmark.info["calculation_info"] = code_version_date_dict

        benchmark.write_description_info()


def doc_calc(calc_name, compare_calcs):
    """Document an already postprocessed calculation.  Generates txt, LaTeX, and png plots."""

    if len(compare_calcs) > 0:
        sys.stdout.write(
            "\nWarning: calculation comparison capability unavailable at this time.\n"
        )

    docs_path = vnv.plotndoc.setup_benchmark_suite_docs_directory(
        DOCUMENTS_PATH, calc_name
    )
    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]

    e_data, e_map = collect_benchmark_results(benchmarks, "experiment_data", "Exp.")
    c_data, c_map = collect_benchmark_results(benchmarks, "calculation_data", "Calc.")

    doc_calc_pulsed_spheres(
        bench_names,
        [e_data, c_data],
        [e_map, c_map],
        benchmarks[0].info["calculation_info"]["data"],
        docs_path,
    )


def clean_calc(calc_name):
    """Cleaning up a specific calculation or the entire calculations directory."""

    if os.path.exists(os.path.join(CALCULATIONS_PATH, calc_name)):
        vnv.clean(CALCULATIONS_PATH, calc_name)
    else:
        vnv.clean(CALCULATIONS_PATH)


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    parser, command_args = vnv.commandline.build_command_line_parser(ALL_TESTS)

    command_args["setup"].add_argument(
        "--data",
        type=str,
        choices=["endf66", "endf70", "endf71", "endf80"],
        default="endf71",
        help="Data library to use, default endf71",
    )

    args = vnv.commandline.parse_and_check_args(parser, ALL_TESTS)

    if args.command == "list":
        list_tests(ALL_TESTS)

    if args.command == "setup":
        setup_calc(args.calcdir_name, args.tests, args.data)

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
