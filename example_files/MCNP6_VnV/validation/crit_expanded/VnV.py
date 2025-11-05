#!/usr/bin/env python3
# ==================================================================================================
"""Script to setup, run, postprocess and analyze criticality validation test problems"""


# ==================================================================================================
# Load standard python modules
import os
import re
import sys

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(1, os.path.join(FILE_PATH, "..", "..", "support"))


# ==================================================================================================
# Load local python modules
import mcnpvnv
import vnv
from vnv.plotndoc import LatexString
from vnv.formatters import FixedPoint, FixedPrecision


# ==================================================================================================
# Module-level variables
PATH = os.getcwd()
NAME = "validation criticality expanded"
BENCHMARKS_DIR = "experiments"
CALCULATIONS_DIR = "calculations"
DOCUMENTS_DIR = "documents"
BENCHMARKS_PATH = os.path.join(FILE_PATH, BENCHMARKS_DIR)
CALCULATIONS_PATH = os.path.join(PATH, CALCULATIONS_DIR)
DOCUMENTS_PATH = os.path.join(PATH, DOCUMENTS_DIR)
ALL_TESTS = vnv.build_dir_list(BENCHMARKS_PATH, name_only=True)


# ==================================================================================================
# Local criticality VnV-specific functions
def collect_benchmark_results(benchmarks, results, label):
    """Unique information and data retrieval from the benchmarks dictionaries (JSON).
    Returns a general data object along with a value/uncertainty map.
    """

    val = LatexString(label + " k-eff", label + r" $k_{\textrm{eff}}$")
    unc = label + " unc."

    data = {
        "Material": [
            benchmark.info["general_info"]["icsbep_name"]["material"]
            for benchmark in benchmarks
        ],
        "Form": [
            benchmark.info["general_info"]["icsbep_name"]["form"]
            for benchmark in benchmarks
        ],
        "Spectrum": [
            benchmark.info["general_info"]["icsbep_name"]["spectrum"]
            for benchmark in benchmarks
        ],
        val: [benchmark.info[results]["k-eff"]["val"] for benchmark in benchmarks],
        unc: [benchmark.info[results]["k-eff"]["std"] for benchmark in benchmarks],
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

    for benchmark in benchmarks:
        output = benchmark.get_file("outputs", "mctal")

        keff, kstd = mcnpvnv.get_keff_from_mctal(output)
        benchmark.info["calculation_data"] = {"k-eff": {"val": keff, "std": kstd}}

        code, version, date = mcnpvnv.get_code_version_from_mctal(output)
        code_version_date_dict = {"code": code, "version": version, "date": date}
        if "calculation_info" in benchmark.info:
            benchmark.info["calculation_info"].update(code_version_date_dict)
        else:
            benchmark.info["calculation_info"] = code_version_date_dict

        benchmark.write_description_info()


def doc_calc(calc_name, use_latex, compare_calcs):
    """Document an already postprocessed calculation.  Generates txt, LaTeX, and png plots."""

    docs_path = vnv.plotndoc.setup_benchmark_suite_docs_directory(
        DOCUMENTS_PATH, calc_name
    )
    calc_path = os.path.join(CALCULATIONS_PATH, calc_name)
    bench_names = vnv.build_dir_list(calc_path, name_only=True)

    benchmarks = [
        mcnpvnv.MCNPBenchmark(calc_path, bench_name) for bench_name in bench_names
    ]

    e_data, e_map = collect_benchmark_results(benchmarks, "experiment_data", "Exp.")
    formatting = {
        e_map["val"]: FixedPoint(4),
        e_map["unc"]: FixedPoint(4),
    }

    # Iterate over primary calculation (calc_name) and any comparison calculations (compare_calcs)
    # to obtain a full list of calculation date to instantiate the dataframe
    calc_paths = [calc_path] + [
        os.path.normpath(compare_calc) for compare_calc in compare_calcs
    ]
    c_data = list()
    c_map = list()
    for c_path in calc_paths:
        calc_name = (
            os.path.split(c_path)[-1].replace("_", " ")
            if len(compare_calcs) > 0
            else ""
        )
        benchmarks = [
            mcnpvnv.MCNPBenchmark(c_path, bench_name) for bench_name in bench_names
        ]

        data, map = collect_benchmark_results(
            benchmarks, "calculation_data", calc_name + " Calc."
        )
        c_data.append(data)
        c_map.append(map)

        formatting[map["val"]] = FixedPrecision(5)
        formatting[map["unc"]] = FixedPoint(6)

    cbdata = vnv.plotndoc.CalcBenchData(
        "All",
        bench_names,
        data=[e_data] + c_data,
        vumap=[e_map] + c_map,
        sort_by="Material",
        formatting=formatting,
    )

    plot_files = ["all_results.pdf"]
    plot_scaling = [0.55]
    all_plot = vnv.plotndoc.ResultPlot((10, 16.2), use_latex=use_latex, transpose=True)

    indep_label = cbdata.df[0].index.array

    for data, map in zip(cbdata.df, cbdata.vumap):
        dep_data = data[map["val"]].to_numpy()
        dep_err = data[map["unc"]].to_numpy()
        indep_data = range(len(data.index))

        all_plot.plot_discrete(indep_data, dep_data, dep_err=dep_err, label=map["val"])

    all_plot.set_independent_label("Benchmarks")
    all_plot.set_dependent_label(
        LatexString("k-effective +/- 1σ", r"$k_{\textrm{eff}} \pm 1\sigma$")
    )
    all_plot.set_independent_tick_labels(indep_label, 90)
    all_plot.add_zebrastripe()
    all_plot.add_grid(dep_grid=True, indep_grid=False)
    all_plot.save(os.path.join(docs_path, plot_files[0]), legend_ncol=2)

    mats = set(cbdata.df[0]["Material"])
    for mat in mats:
        mat_df = [df[df["Material"] == mat] for df in cbdata.df]
        plot_files.append("{}_results.pdf".format(mat))
        plot_scaling.append(1.0)
        mat_plot = vnv.plotndoc.ResultPlot(
            (6.5, 6.5), use_latex=use_latex, transpose=True
        )

        indep_label = mat_df[0].index.array

        for data, map in zip(mat_df, cbdata.vumap):
            dep_data = data[map["val"]].to_numpy()
            dep_err = data[map["unc"]].to_numpy()
            indep_data = range(len(data.index))

            mat_plot.plot_discrete(
                indep_data, dep_data, dep_err=dep_err, label=map["val"]
            )

        mat_plot.set_independent_label("Benchmarks")
        mat_plot.set_dependent_label(
            LatexString("k-effective +/- 1σ", r"$k_{\textrm{eff}} \pm 1\sigma$")
        )
        mat_plot.set_independent_tick_labels(indep_label, 90)
        mat_plot.add_zebrastripe()
        mat_plot.add_grid(dep_grid=True, indep_grid=False)
        mat_plot.save(os.path.join(docs_path, plot_files[-1]), legend_ncol=1)

    cbdata.to_string(output_file=os.path.join(docs_path, "results.txt"))
    cbdata.to_latex(
        output_file=os.path.join(docs_path, "results.tex"),
        include_plots=plot_files,
        plot_scaling=plot_scaling,
        do_resizebox=True,
    )
    with open(os.path.join(docs_path, "report.tex"), "w") as latex_file:
        latex_file.write("\n\\input{results.tex}\n")


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
        choices=["endf70", "endf71", "endf80"],
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
        doc_calc(args.calcdir_name, args.latex_plots, args.compare)

    if args.command == "clean":
        clean_calc(args.calcdir_name)
