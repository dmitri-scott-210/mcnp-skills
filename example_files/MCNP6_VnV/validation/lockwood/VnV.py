#!/usr/bin/env python
# ==================================================================================================
"""Script to setup, run, postprocess and analyze Lockwood validation test problems"""


# ==================================================================================================
# Load standard python modules
import logging
import os
import shutil
import sys
import textwrap

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(1, os.path.join(FILE_PATH, "..", "..", "support"))


# ==================================================================================================
# Load local python modules
import mcnpvnv
import vnv


# ==================================================================================================
# Module-level variables
PATH = os.getcwd()
NAME = "validation lockwood"
BENCHMARKS_DIR = "experiments"
CALCULATIONS_DIR = "calculations"
DOCUMENTS_DIR = "documents"
BENCHMARKS_PATH = os.path.join(FILE_PATH, BENCHMARKS_DIR)
CALCULATIONS_PATH = os.path.join(PATH, CALCULATIONS_DIR)
DOCUMENTS_PATH = os.path.join(PATH, DOCUMENTS_DIR)
ALL_TESTS = vnv.build_dir_list(BENCHMARKS_PATH, name_only=True)

# ==================================================================================================
# Local Lockwood VnV-specific functions
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


def post_calc(calc_name):
    """Postprocess an already executed calculation."""

    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]

    for b in benchmarks:
        output = b.get_file("outputs", "mctal")
        _, val, err = mcnpvnv.get_tally_from_mctal(output, 8)
        code, vers, date = mcnpvnv.get_code_version_from_mctal(output)
        b.info["calculation_info"] = {
            "code": code,
            "version": vers,
            "date": date,
        }
        b.info["calculation_data"] = {"tally": {"val": val[0], "err": err[0]}}
        b.write_description_info()


def doc_calc(calc_name, compare_calcs):
    """Document an already postprocessed calculation.  Generates txt, LaTeX, and PDF plots."""

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

    e_data, e_map = collect_benchmark_results(benchmarks, "experiment_data", "Exp.")
    c_data, c_map = collect_benchmark_results(benchmarks, "calculation_data", "Calc.")

    cbdata = vnv.plotndoc.CalcBenchData(
        "All",
        bench_names,
        data=[e_data, c_data],
        vumap=[e_map, c_map],
        sort_by="Material",
    )

    cbdata.to_string(output_file=os.path.join(doc_path, "results.txt"))

    doc_calc_lockwood(cbdata, doc_path, calc_path)


def clean_calc(calc_name):
    """Cleaning up a specific calculation or the entire calculations directory."""

    if os.path.exists(os.path.join(CALCULATIONS_PATH, calc_name)):
        vnv.clean(CALCULATIONS_PATH, calc_name)
    else:
        vnv.clean(CALCULATIONS_PATH)


# ==================================================================================================
# Local Lockwood VnV-specific functions


def make_plot_lockwood(df, outfilename):
    """Create plots of each Lockwood case broken down by benchmark,
    condensed-history, and single-event results."""

    boolch = df["Type"] == "Condensed History"
    boolse = df["Type"] == "Single Event"
    x = df[boolch]["FMR"].values
    exp = df[boolch]["Exp. Val."].values
    experr = df[boolch]["Exp. Unc."].values

    ch = df[boolch]["Calc. Val."].values
    cherr = df[boolch]["Calc. Unc."].values
    se = df[boolse]["Calc. Val."].values
    seerr = df[boolse]["Calc. Unc."].values

    _, ax = plt.subplots(1, 1, figsize=(6.5, 6.5 / 1.61))
    plt.plot(
        x, exp, color="#000000", marker=".", ls="-", label="Exp. $\\pm$ $1\\sigma$"
    )
    plt.fill_between(
        x, exp * (1 - experr), exp * (1 + experr), color="#000000", alpha=0.2
    )

    plt.plot(
        x,
        ch,
        color="#ff0000",
        marker="3",
        ls="--",
        label="Cond. Hist. $\\pm$ $1\\sigma$",
    )
    plt.fill_between(x, ch * (1 - cherr), ch * (1 + cherr), color="#ff0000", alpha=0.2)

    plt.plot(
        x,
        se,
        color="#0000ff",
        marker="4",
        ls=":",
        label="Single Event $\\pm$ $1\\sigma$",
    )
    plt.fill_between(x, se * (1 - seerr), se * (1 + seerr), color="#0000ff", alpha=0.2)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Fraction of a Mean Range (FMR)")
    plt.ylabel("Energy Deposition [MeV]")
    plt.grid(color="#cccccc", ls=":")
    plt.legend(loc="best")
    plt.savefig(outfilename, bbox_inches="tight", dpi=300)
    plt.close()


# Create LaTeX output.
def make_lockwood_results_remarks(mdf, material):
    """Generate brief text summarizing results comparison for a particular material."""

    # Get number of angle and energy cases.
    d = mdf.Angle.unique()
    nd = len(d)
    sd = "1 angle" if nd == 1 else f"{nd} angles"
    e = mdf.Energy.unique()
    ne = len(e)
    ne = 1
    se = "1 energy" if nd == 1 else f"{ne} energies"

    # Recreate table labels.
    tabch = f"tab:{material}_Condensed_History_Results"
    tabse = f"tab:{material}_Single_Event_Results"

    # Create list of figures.
    lof = []
    for d, ddf in sorted(mdf.groupby("Angle")):
        for e, edf in sorted(ddf.groupby("Energy")):
            title = f"{material} {d}-degree {e} MeV Results"
            label = "fig:" + title.replace(" ", "_")
            lof.append(label)

    # Create general text for material results.
    if len(lof) == 1:
        figure_word = "Figure"
        figure_range = f"\\ref{{{lof[0]}}}"
    else:
        figure_word = "Figures"
        figure_range = f"\\ref{{{lof[0]}}}--\\ref{{{lof[-1]}}}"
    s = f"""
    The {material} cases break down into {sd} and {se}. The
    condensed-history results are given in Table~\\ref{{{tabch}}} and the
    single-event results are given in Table~\\ref{{{tabse}}}.  For each
    energy and direction, plots of results versus measured values are given
    in {figure_word}~{figure_range}.\n"""
    s = textwrap.dedent(s)

    # Collect text on specific results.
    sr = ""
    for e, edf in mdf.groupby("Energy"):
        for d, ddf in edf.groupby("Angle"):
            val_ch = np.mean(ddf[ddf.Type == "Condensed History"]["Calc./Bench."])
            err_ch = np.sqrt(
                sum(x ** 2 for x in ddf[ddf.Type == "Condensed History"]["Calc. Unc."])
            ) / len(ddf[ddf.Type == "Condensed History"]["Calc. Unc."])
            val_se = np.mean(ddf[ddf.Type == "Single Event"]["Calc./Bench."])
            err_se = np.sqrt(
                sum(x ** 2 for x in ddf[ddf.Type == "Single Event"]["Calc. Unc."])
            ) / len(ddf[ddf.Type == "Single Event"]["Calc. Unc."])
            sr += f"""
            For the {e} MeV case at {d} degrees, the condensed-history
            results have an average calculated-over-measured value of
            ${val_ch:.3f}\\pm{err_ch*100:.3f}$\\% (overall average standard
            deviation) and the single-event results have an average
            calculated-over-measured value of
            ${val_se:.3f}\\pm{err_se*100:.3f}$\\% (overall average standard
            deviation).\n"""

    sr = textwrap.dedent(sr)

    return s + sr


def doc_calc_lockwood(cbdata, doc_path, calc_path):
    r""" Document the Lockwood suite results.  A minimal functional container
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
    \input{.../appendix_results.tex}
    \end{document}
    """

    # Merge experimental and calculated dataframes to generate results report.
    df = pd.merge(left=cbdata.df[0], right=cbdata.df[1])

    # Style columns for typesetting.
    df["Angle, Typeset"] = df["Angle"].map("{:}$^{{\circ}}$".format)
    df["Energy, Typeset"] = df["Energy"].map("{:} MeV".format)
    df["Exp. with Unc."] = (
        df["Exp. Val."].map("{:,.5f}".format)
        + r"$\pm$"
        + df["Exp. Unc."].multiply(100).map("{:,.1f}\%".format)
    )
    df["Calc. with Unc."] = (
        df["Calc. Val."].map("{:,.5f}".format)
        + r"$\pm$"
        + df["Calc. Unc."].multiply(100).map("{:,.1f}\%".format)
    )
    df["Calc./Bench."] = df["Calc. Val."] / df["Exp. Val."]
    df["Calc./Bench., Typeset"] = df["Calc./Bench."].map("{:.2f}".format)

    # Create include directory for tables, figures, embedded input files
    include_dir = "include"
    include_path = os.path.relpath(os.path.join(doc_path, include_dir))
    if os.path.exists(include_path):
        shutil.rmtree(include_path)
    os.mkdir(include_path)

    def create_plots(df):
        """Create plots for Lockwood."""
        logging.info("Creating plots...")
        for m, mdf in df.groupby("Material"):
            for d, ddf in mdf.groupby("Angle"):
                for e, edf in ddf.groupby("Energy"):
                    plotdf = edf.sort_values(by="FMR Index")
                    title = f"{m} {d}-degree {e} MeV Results"
                    outfilename = os.path.join(
                        include_path, title.replace(" ", "_") + ".pdf"
                    )
                    logging.debug(f"Creating plot {outfilename}")
                    make_plot_lockwood(plotdf, outfilename)

    def create_tables(df):
        """Create tables for Lockwood."""
        logging.info("Creating tables...")
        for m, mdf in df.groupby("Material"):
            for t, tdf in mdf.groupby("Type"):
                tabledf = tdf.sort_values(by=["Angle", "Energy", "FMR Index"])
                title = f"{m} {t} Results"
                outfilename = os.path.join(
                    include_path, title.replace(" ", "_") + ".tex"
                )
                logging.debug(f"Creating table {outfilename}")
                tabledf.to_latex(
                    buf=outfilename,
                    columns=[
                        "Angle, Typeset",
                        "Energy, Typeset",
                        "FMR",
                        "Exp. with Unc.",
                        "Calc. with Unc.",
                        "Calc./Bench., Typeset",
                    ],
                    header=["~", "~", "FMR", "Exp. [MeV]", "Calc. [MeV]", "C/E",],
                    index=False,
                    escape=False,
                )

    create_plots(df)
    create_tables(df)

    outfilename = os.path.join(doc_path, "results.tex")
    logging.info("Writing documentation file...")
    f = open(outfilename, "w")
    f.write("\\providecommand\\includepath{.}\n")
    for m, mdf in df.groupby("Material"):
        logging.debug(f"Making remarks for {m}")
        f.write(f"\n\\subsubsection{{{m}}}\n")
        f.write(make_lockwood_results_remarks(mdf, m))

    for m, mdf in df.groupby("Material"):
        for t, _ in sorted(mdf.groupby("Type")):
            title = f"{m} {t} Results"
            label = "tab:" + title.replace(" ", "_")
            logging.debug(f"Incorporating table {label}")
            infilename = os.path.join(include_dir, title.replace(" ", "_") + ".tex")
            f.write("\\begin{table}[p]\n")
            f.write("  \\begin{center}\n")
            f.write(f"    \\caption{{{title}\\label{{{label}}}}}\n")
            f.write(f"    \\input{{\\includepath/{infilename}}}\n")
            f.write("  \\end{center}\n")
            f.write("\\end{table}\n")

        for d, ddf in sorted(mdf.groupby("Angle")):
            for e, _ in sorted(ddf.groupby("Energy")):
                title = f"{m} {d}-degree {e} MeV Results"
                label = "fig:" + title.replace(" ", "_")
                logging.debug(f"Incorporating figure {label}")
                infilename = "{" + os.path.join(
                    include_dir, title.replace(" ", "_") + "}.pdf"
                )
                f.write("\\begin{figure}[p]\n")
                f.write("  \\begin{center}\n")
                f.write(f"    \\includegraphics{{\\includepath/{infilename}}}\n")
                f.write(f"    \\caption{{{title}\\label{{{label}}}}}\n")
                f.write("  \\end{center}\n")
                f.write("\\end{figure}\n")

        f.write("\\clearpage\n")
        f.write("\n")

    f.close()

    # Copy and include inputs as electronically attached files via the `embed` LaTeX package.
    outfilename = os.path.join(doc_path, "appendix_results.tex")
    f = open(outfilename, "w")
    f.write("\n\\subsection{Input files}\n")
    f.write(
        textwrap.dedent(
            """
    This section provides a collection of MCNP input files suitable for running
    a variety of materials, angles, energies, and thicknesses for both
    condensed-history and single-event transport algorithms.  For convenience,
    these files are also electronically attached to this PDF.\n\n"""
        )
    )

    inputdf = df.sort_values(["Material", "Angle", "Energy", "FMR Index"])

    for _, r in inputdf.iterrows():
        # Copy in inputs.
        src = os.path.join(calc_path, r["Name"], r["Name"] + "_")
        infilename = "lockwood_" + r["Name"] + ".mcnp.inp.txt"
        dst = os.path.join(include_path, infilename)
        shutil.copy(src, dst)

        title = f"{r['Material']} {r['Angle']}-degree {r['Energy']} MeV Results, FMR {r['FMR']}, {r['Type']} MCNP Input File"
        label = "lst:" + title.replace(" ", "_")
        infilename = f"{include_dir}/{infilename}"
        logging.debug(f"Incorporating listing of {infilename}")
        f.write(
            f"\\lstinputlisting[caption={{{title}}},label={{{label}}}]{{\\includepath/{infilename}}}\n"
        )
        f.write(f"\\embedfile{{\\includepath/{infilename}}}\n")

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
