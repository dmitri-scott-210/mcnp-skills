#!/usr/bin/env python3
# ==================================================================================================
"""Script to setup, run, postprocess and analyze Kobayashi verification test problems"""


# ==================================================================================================
# Load standard python modules
import copy
import os
import re
import sys
import numpy as np
import pandas as pd

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(1, os.path.join(FILE_PATH, "..", "..", "support"))


# ==================================================================================================
# Load local python modules
import mcnpvnv
import vnv
from vnv.plotndoc import LatexString, apply_resizebox
from vnv.formatters import FixedPoint, FixedPrecision


# ==================================================================================================
# Module-level variables
PATH = os.getcwd()
NAME = "verification Kobayashi"
BENCHMARKS_DIR = os.path.join("problems", "CSG", "Importance_Splitting")
CALCULATIONS_DIR = "calculations"
DOCUMENTS_DIR = "documents"
BENCHMARKS_PATH = os.path.join(FILE_PATH, BENCHMARKS_DIR)
CALCULATIONS_PATH = os.path.join(PATH, CALCULATIONS_DIR)
DOCUMENTS_PATH = os.path.join(PATH, DOCUMENTS_DIR)
ALL_TESTS = vnv.build_dir_list(BENCHMARKS_PATH, name_only=True)


# ==================================================================================================


class CalcBenchDataTable(vnv.plotndoc.CalcBenchData):

    """Inherits from vnv.plotndoc.CalcBenchData but adds a new method, `add_table_df`, that creates
    new pandas dataframes, indexed by problem name, for the benchmark and calculated data sets."""

    def __init__(
        self, name, index, data, vumap, sort_by=None, formatting=None, cb_dict=None
    ):
        def add_table_df(self):
            """Private method of __init__ to create new pandas dataframes indexed by problem name.

            Parameters
            ----------
            table_df : list of pandas.DataFrame
                Benchmark and calculated dataframes indexed by problem name.
            cb_dict : dict, keyed by benchmark name
                Contains the C/E values and uncertainties and corresponding
                coordinates."""

            # List to hold the benchmark and calculated dataframes.
            table_df = []

            # Iterate over the benchmark and calculated dataframes and their
            # column-name mapping.
            for df, vumap in zip(self.df, self.vumap):

                # Create an empty dataframe to which several pandas series will be
                # appended.
                table_df_elem = pd.DataFrame()

                # Iterate over the problem names (which are the indices in the
                # original data frame).
                for prob_name in df.index:

                    # For each row in the original data frame, each column entry
                    # had a list of values. This loop iterates over the values in
                    # those lists.
                    for coord, flux, unc in zip(
                        df.at[prob_name, "coordinates"],
                        df.at[prob_name, vumap["val"]],
                        df.at[prob_name, vumap["unc"]],
                    ):

                        # Create a panda series object for the individual list
                        # values instead of for the whole list.
                        pd_series = pd.Series(
                            data=[
                                prob_name,
                                df.at[prob_name, "Problem Type"],
                                coord,
                                flux,
                                unc,
                            ],
                            index=[
                                "Problem Name",
                                "Problem Type",
                                "coordinates",
                                vumap["val"],
                                vumap["unc"],
                            ],
                        )

                        # Append the pandas series object to the new data frame.
                        table_df_elem = table_df_elem.append(
                            pd_series, ignore_index=True
                        )

                # Append the completed new data frame to the list of data frames
                # (benchmark and calculated).
                table_df.append(table_df_elem)

            # Having iterated over the benchmark and calculated data, append
            # the C/E data, if requested.
            if cb_dict is not None:

                # Append C/E mapping to the existing list of maps. This function
                # will use cb_map, but other functions will need the list of
                # data frames and maps to be the same.
                cb_map = {
                    "val": LatexString("C/E values", r"$C/E$"),
                    "unc": LatexString("C/E uncertainties", r"$C/E$ unc."),
                }
                self.vumap.append(cb_map)

                # Add entries to the formatting dictionary.
                self.formatting[cb_map["val"]] = FixedPrecision(4, scientific=True)
                self.formatting[cb_map["unc"]] = FixedPrecision(4, scientific=True)

                # Since the formatting dictionary got updated, need to
                # regenerate the default_columns attribute.
                self.default_columns = list()
                for vu in self.vumap:
                    self.default_columns += vu.values()

                # Create an empty dataframe to which several pandas series will
                # be appended.
                table_df_elem = pd.DataFrame()

                # Iterate over the problem names.
                for prob_name in cb_dict.keys():
                    cb_entries = cb_dict[prob_name]
                    coordinates = cb_entries["coordinates"]
                    cb_vals = cb_entries["values"]
                    cb_uncs = cb_entries["uncertainties"]
                    for coord, val, unc in zip(coordinates, cb_vals, cb_uncs):

                        # Create a panda series object for the individual list
                        # values instead of for the whole list.
                        pd_series = pd.Series(
                            data=[prob_name, coord, val, unc,],
                            index=[
                                "Problem Name",
                                "coordinates",
                                cb_map["val"],
                                cb_map["unc"],
                            ],
                        )

                        # Append the pandas series object to the new data frame.
                        table_df_elem = table_df_elem.append(
                            pd_series, ignore_index=True
                        )

                # Append the completed new data frame to the list of data frames
                # (benchmark and calculated).
                table_df.append(table_df_elem)

            # This class inherits from vnv.plotndoc.CalcBenchData and adds this
            # new attribute.
            self.table_df = table_df

            return

        # Preserve the vnv.plotndoc.CalcBenchData __init__ function.
        super().__init__(
            name, index, data, vumap, sort_by=sort_by, formatting=formatting
        )

        # Add the differently formatted data frame as an attribute.
        add_table_df(self)

    def to_latex(
        self,
        output_file=None,
        filemode="w",
        bench_name=None,
        full_table=False,
        include_plot=None,
        plot_scaling=None,
        do_resizebox=False,
    ):

        """Modified copy of vnv.plotndoc.CalcBenchData that writes a subset of the `table_df` attribute to a
        latex-formatted table.

        Parameters
        ----------

        filemode : str, optional
            Indicates whether a new file should be written ('w') or an existing file should
            be appended to ('a').
        bench_name : str, optional
            Used to choose a subset of the main pandas dataframe and to label the latex table entry."""

        table_df = self.table_df
        vumap = self.vumap

        # The parent class sets this attribute once, but this method needs to set it at each call.
        self.name = bench_name

        # Data frame to hold the values and uncertainties.
        df = pd.DataFrame()

        # Loop through the benchmark and calculation data frames to get both
        # sets of values and uncertainties.

        for tdf, vmap in zip(table_df, vumap):

            # Choose a row subset of the entire table (making a table for one problem at a time).
            tdf_subset = tdf.loc[tdf["Problem Name"] == bench_name]
            entries = tdf_subset[[vmap["val"], vmap["unc"]]]

            df = pd.concat([df, entries], axis=1)

        # Index the table by the detector coordinates.
        df.set_index(keys=tdf_subset["coordinates"], inplace=True)

        # The index header is set below the column headers, which is
        # undesirable. The workaround here is the set the columns name (None)
        # to the index name (coordinates) and to remove the index name (set it
        # to None). Since this column name appears in the latex table, it is
        # capitalized.
        df.columns.name = df.index.name.capitalize()
        df.index.name = None

        # Convert string text to Latex versions
        df = df.applymap(lambda x: vnv.plotndoc.get_latex_string(x))
        df.rename(columns=lambda x: vnv.plotndoc.get_latex_string(x), inplace=True)
        default_columns = [
            vnv.plotndoc.get_latex_string(column) for column in self.default_columns
        ]
        if self.formatting:
            formatting = {
                vnv.plotndoc.get_latex_string(column): self.formatting[column]
                for column in self.default_columns
            }
        else:
            formatting = None

        title = "{} Calculation Benchmark Results".format(
            vnv.plotndoc.escape_latex(self.name)
        )
        caption = title
        string = r"\providecommand\includepath{.}" if filemode == "w" else ""
        fig_table_desc = vnv.plotndoc.escape_latex(
            " ".join(
                [
                    "\nThe following figures and tables are results from the Kobayashi analytic benchmarks.",
                    "The plots display C/E values and their uncertainties.",
                    "The tables provide the benchmark and calculated values and uncertainties as well as their C/E values and uncertainties.",
                    "This problem set contains 6 benchmarks that were designed to test how 3D discrete ordinates codes deal with ray effects in problems with void and combination of void, purely absorbing, and mixed absorbing/scattering regions.",
                    "The figures and tables for the purely absorbing problems are identified with an ``i'' in their moniker (``p1i_ce'', ``p2i_ce'', and ``p3i_ce''), ",
                    "while figures and tables for the mixed absorbing/scattering problems are identified with an ``ii'' in their moniker (``p1ii_ce'', ``p2ii_ce'', and ``p3ii_ce'').\n",
                ]
            )
        )
        string += fig_table_desc if filemode == "w" else ""
        string += "\n\n\\clearpage\n\\begin{{landscape}}\n\\paragraph{{{}}}\n\n".format(
            title
        )
        if include_plot is not None:
            if plot_scaling is None:
                plot_scaling = 1.0
            string += vnv.plotndoc.latex_figure(include_plot, caption, plot_scaling)
        string += "\\end{landscape}\n"

        if full_table:
            segment = df
        else:
            segment = df[default_columns]

        table = vnv.plotndoc.latex_table(segment, do_resizebox, caption, formatting)
        string += table

        if self.sort_by is not None:
            sorts = set(df[self.sort_by])
            for i, comparison in enumerate(sorts):
                title = "{} Calculation Benchmark Results".format(comparison)
                caption = title
                string += "\n\\clearpage\n\\paragraph{{{}}}\n\n".format(title)
                if include_plot is not None:
                    string += vnv.plotndoc.latex_figure(
                        include_plot[i + 1], caption, plot_scaling[i + 1]
                    )

                if full_table:
                    segment = df[df[self.sort_by] == comparison]
                else:
                    segment = df[df[self.sort_by] == comparison][default_columns]

                string += vnv.plotndoc.latex_table(
                    segment, do_resizebox, caption, formatting
                )

        if output_file is not None:
            with open(output_file, filemode) as file:
                file.write(string)

        return string


def collect_benchmark_results(benchmarks, results, label, get_uncertainty=True):
    """Unique information and data retrieval from the benchmarks dictionaries (JSON).
    Returns a general data object along with a value/uncertainty map.
    """

    def convert_rel_abs_unc(vals, rel_stds):

        return [val * rel_std for val, rel_std in zip(vals, rel_stds)]

    val = LatexString(label + " total flux", label + r" $\phi_t$")
    unc = label + " unc."

    data = {
        "Problem Type": [
            benchmark.info["general_info"]["problem_type"] for benchmark in benchmarks
        ],
        val: [benchmark.info[results]["total_flux"]["val"] for benchmark in benchmarks],
        "coordinates": [
            benchmark.info[results]["total_flux"]["coordinates"]
            for benchmark in benchmarks
        ],
    }

    if get_uncertainty:

        # Grab the relative standard deviations, if present. If not, put all
        # zeros. Doing a for loop instead of a list comprehension so that the
        # try-except happens for each benchmark.
        rel_std_lists = []
        for benchmark in benchmarks:
            try:
                rel_std_list = benchmark.info[results]["total_flux"]["rel_std"]
            except KeyError:
                rel_std_list = [0.0] * len(benchmark.info[results]["total_flux"]["val"])
            rel_std_lists.append(rel_std_list)

        # Convert relative to absolute standard deviation.
        abs_stds = [
            convert_rel_abs_unc(benchmark.info[results]["total_flux"]["val"], rel_stds)
            for benchmark, rel_stds in zip(benchmarks, rel_std_lists)
        ]

        data[unc] = [abs_std for abs_std in abs_stds]

        vumap = {"val": val, "unc": unc}
    else:
        vumap = {"val": val}

    return data, vumap


# ==================================================================================================
# Local general functions
def list_tests(tests=ALL_TESTS):
    """List all available tests in benchmark suite."""

    print("All available tests in {}:".format(NAME))
    for test in tests:
        print("  {}".format(test))


def setup_calc(calc_name, tests):
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

    for benchmark in benchmarks:

        # Each Kobayashi input has a different number of tallies, so grab the
        # tally IDs (and the corresponding coordinates entries) from the
        # description.json file. They are listed under either the analytic or
        # GMVP data entry.

        description_dict = benchmark.info

        tally_ids = description_dict["benchmark_data"]["total_flux"]["tally_id"]
        coordinates = description_dict["benchmark_data"]["total_flux"]["coordinates"]

        vals_list = []
        errs_list = []

        output = benchmark.get_file("outputs", "mctal")
        code, vers, date = mcnpvnv.get_code_version_from_mctal(output)

        for tally_id in tally_ids:

            bins, vals, errs = mcnpvnv.get_tally_from_mctal(output, tally_id)

            # get_tally_from_mctal returns a list with a single entry, so just
            # append the value to the list.
            val = vals[0]
            err = errs[0]

            # Append values to the list that gets written to the descriptions
            # file.
            vals_list.append(val)
            errs_list.append(err)

        benchmark.info["calculation_data"] = {
            "total_flux": {
                "tally_id": tally_ids,
                "coordinates": coordinates,
                "val": vals_list,
                "rel_std": errs_list,
            }
        }
        benchmark.info["calculation_info"] = {
            "code": code,
            "version": vers,
            "date": date,
        }
        benchmark.write_description_info()


def doc_calc(calc_name, use_latex, compare_calcs):
    """Document an already postprocessed calculation.  Generates txt, LaTeX, and pdf plots."""

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

    e_data, e_map = collect_benchmark_results(
        benchmarks, "benchmark_data", "Benchmark", get_uncertainty=True
    )
    c_data, c_map = collect_benchmark_results(
        benchmarks, "calculation_data", "Calc.", get_uncertainty=True
    )

    formatting = {
        e_map["val"]: FixedPrecision(4, scientific=True),
        e_map["unc"]: FixedPrecision(4, scientific=True),
        c_map["val"]: FixedPrecision(4, scientific=True),
        c_map["unc"]: FixedPrecision(4, scientific=True),
    }

    ce_data = vnv.plotndoc.CalcBenchData(
        "All",
        bench_names,
        data=[c_data, e_data],
        vumap=[c_map, e_map],
        sort_by="Problem Type",
    )

    plot_files = []
    plot_scaling = 0.65

    c_df, e_df = ce_data.df
    c_vumap, e_vumap = ce_data.vumap

    # Dictionary for holding the C/E values and uncertainties and corresponding
    # coordinates, keyed by benchmark.
    cb_dict = {}

    for index in c_df["Problem Type"].index:

        plot_files.append("{}_results.pdf".format(index))
        type_plot = vnv.plotndoc.ResultPlot(
            (14, 7), use_latex=use_latex, transpose=True
        )

        c_dep_data = c_df[c_vumap["val"]].loc[index]
        c_dep_err = c_df[c_vumap["unc"]].loc[index]

        e_dep_data = e_df[e_vumap["val"]].loc[index]
        e_dep_err = e_df[e_vumap["unc"]].loc[index]

        indep_data = range(len(c_dep_data))

        # These are used as tick labels for the independent data.
        coordinates = c_df["coordinates"].loc[index]

        # More useful to plot C/E values rather than the values themselves.
        cb_data, cb_err, _ = vnv.c_over_b(c_dep_data, c_dep_err, e_dep_data, e_dep_err)

        # Put these in a dictionary together with the coordinates to add to the
        # latex table later on.
        cb_dict[index] = {
            "coordinates": coordinates,
            "values": cb_data,
            "uncertainties": cb_err,
        }

        type_plot.plot_discrete(indep_data, cb_data, dep_err=cb_err)

        type_plot.set_independent_label("Detector position (cm)")
        type_plot.set_independent_tick_labels(tick_labels=coordinates, tick_angle=90)

        type_plot.set_dependent_label(
            LatexString(
                "Total flux C/E +/- 1σ", r"$\phi_{\textrm{total}} $ $ C/E \pm 1\sigma$"
            )
        )

        type_plot.add_zebrastripe()
        type_plot.add_grid(dep_grid=True, indep_grid=False)
        type_plot.save(os.path.join(docs_path, plot_files[-1]))

    # Create a dataframe with data from all of the problems using the child CalcBenchDataTable class.
    cbdata = CalcBenchDataTable(
        "All",
        bench_names,
        data=[e_data, c_data],
        vumap=[e_map, c_map],
        sort_by=None,
        formatting=formatting,
        cb_dict=cb_dict,
    )

    # Write a separate table for each problem's data. Counter is used to decide if a new file
    # should be written (counter==0) or if an existing file should be appended to (counter!= 0)
    for counter, bench_name in enumerate(bench_names):

        cbdata.to_latex(
            output_file=os.path.join(docs_path, "results.tex"),
            filemode="w" if counter == 0 else "a",
            bench_name=bench_name,
            include_plot=plot_files[counter],
            plot_scaling=plot_scaling,
            full_table=True,
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
        doc_calc(args.calcdir_name, args.latex_plots, args.compare)

    if args.command == "clean":
        clean_calc(args.calcdir_name)
