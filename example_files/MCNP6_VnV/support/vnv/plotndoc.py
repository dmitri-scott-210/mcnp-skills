#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite Documentation and Plotting Functions
    + Create pandas dataframe of calculation and benchmark data
    + Print pandas dataframe and some metrics to stdout
"""


# ==================================================================================================
import os
import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

from .formatters import DEFAULT_FLOAT_FORMAT

# ==================================================================================================
def setup_benchmark_suite_docs_directory(to_path, calc_name):
    """
    Setup documentation to_path/calc_name directory.
    """

    os.makedirs(to_path, exist_ok=True)

    docs_path = os.path.join(to_path, calc_name)
    try:
        os.mkdir(docs_path)
    except FileExistsError:
        sys.stdout.write(
            "\nWarning: {} directory already exists. Overwrite possible.\n".format(
                docs_path
            )
        )

    return docs_path


# ==================================================================================================
def latex_figure(file_name, caption=None, scaling=1.0):
    """Generate a Latex figure encapsulating file_name, with caption."""
    string = "\n"
    string += "\\begin{figure}\n"
    string += "  \\centering\n"
    string += "  \\includegraphics[scale={}]{{\\includepath/{}}}\n".format(
        scaling, file_name
    )
    if caption is not None:
        string += "  \\caption{{{}}}\n".format(caption)
    string += "\\end{figure}\n"
    string += "\n"

    return string


# ==================================================================================================
def latex_table(table, do_resizebox, caption=None, formatting=None):
    """Generate a Latex table using the contents from table.

    Parameters
    ----------

    table: pandas.DataFrame
        Dataframe containing the measured/analytic and simulated values and
        corresponding uncertainties.
    do_resizebox: bool
        Apply resizebox to force the overall LaTeX table width equal to the
        text width.
    caption: str
        Title for the LaTeX table.
    formatting: dict
        Dictionary of format specifier pairs. The keys are column format
        specifiers (e.g. how wide to make the column) and the values are number
        format specifies (e.g. represent the column data with 4 decimal places).
    """
    
    n_rows, n_columns = table.shape
    longtable = n_rows > 40

    column_names = list(table)

    column_format = "l"
    number_format = []
    for col in table:
        if formatting:
            format = formatting[col]
        else:
            format = DEFAULT_FLOAT_FORMAT

        column_format += format.siunitx_formatter(table[col].to_numpy())
        number_format.append(format.python_formatter())

    table_col = table.rename(columns=lambda x: "{" + x + "}")

    table_str = table_col.to_latex(
        escape=False,
        longtable=longtable,
        caption=caption,
        column_format=column_format,
        formatters=number_format,
    )

    string = "\n"
    if longtable:
        string += "\\begin{centering}\n"
        string += table_str
        string += "\\end{centering}\n"
    else:
        string += table_str
    string += "\n"

    # Scales the table to fit within the page margins. `\resizebox` doesn't
    # work with `\longtable`, so only apply it to `\tabular`.
    if do_resizebox and not longtable:
        return apply_resizebox(
            string,
            delimiters=(r"\\begin{tabular}", r"\\end{tabular}"),
            width=r"\\textwidth",
        )
    else:
        return string


def apply_resizebox(
    instr: str, delimiters: Tuple[str] = None, width: str = None, height: str = None
) -> str:
    """Wrap a region of text with given starting and ending delimiters in a call
    to resize box.  This is particularly useful for ensuring that overwidth
    tables fit within page margins.

    Parameters
    ----------
    instr : str
        The input string that will have `resizebox` applied.  If the
        `delimiters` are set to `None`, then the entire input string is wrapped
        by `resizebox`.  If not, then two regular-expression find-replace
        operations are used to insert the `resizebox` behavior.
    delimiters : Tuple[str], optional
        Length-two tuple (or none) that specifies the beginning and ending
        string delimiters to wrap a `resizebox` call outside of (where the
        entire input string is wrapped if this is None), by default None
    width : str, optional
        The `resizebox` width (first) argument, which is set to `!` if None, by
        default None
    height : str, optional
        The `resizebox` height (second) argument, which is set to `!` if None,
        by default None

    Returns
    -------
    str
        Modified `instr` that includes the `resizebox` call.
    """

    # Ensure that at least width or height is specified (both being specified
    # simultaneously is valid).
    assert width is not None or height is not None
    if width is None:
        width = "!"
    if height is None:
        height = "!"
    resizebox = r"\\resizebox{" + width + "}{" + height + "}{\n"

    # Ensure that the delimiters are either None or of the proper length and
    # type.
    assert delimiters is None or (
        len(delimiters) == 2 and all([isinstance(i, str) for i in delimiters])
    )

    if delimiters is None:
        return resizebox + instr + "\n}"
    else:
        import re

        # Prepend `resizebox`.
        instr = re.sub(delimiters[0], f"{resizebox}" + delimiters[0], instr, re.S)
        # Append `resizebox`.
        instr = re.sub(delimiters[1], delimiters[1] + "\n}", instr, re.S)
        return instr


# ==================================================================================================


def escape_latex(string):
    """Generate Latex-friendly strings from the argument."""
    substitution_dict = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    merged_regex = "|".join([re.escape(key) for key in substitution_dict])
    regex = re.compile(merged_regex)
    return regex.sub(lambda x: substitution_dict[x.group()], string)


class LatexString:
    """Contains a LaTeX string and its equivalent non-LaTeX representation.
    Lexigraphic sorting is based on the non-LaTeX string."""

    def __init__(self, base_string, latex_string=None):

        self.base_string = base_string
        if latex_string:
            self.latex_string = latex_string
        else:
            self.latex_string = escape_latex(base_string)

    def __str__(self):
        return self.base_string

    def __lt__(self, other):
        if isinstance(other, LatexString):
            return self.base_string < other.base_string
        else:
            return self.base_string < other


def get_base_string(str_object):
    """Extracts the base string from either a string or LatexString"""
    if isinstance(str_object, LatexString):
        return str_object.base_string

    return str_object


def get_latex_string(str_object):
    """Extracts the latex string from either a string or LatexString"""

    if isinstance(str_object, LatexString):
        return str_object.latex_string
    elif isinstance(str_object, str):
        return escape_latex(str_object)

    return str_object


# ==================================================================================================


DEFAULT_RC_PARAMS = {"font.size": 10, "savefig.dpi": 300}

LATEX_RC_PARAMS = {
    "font.family": "serif",
    "font.monospace": [],
    "font.sans-serif": [],
    "font.serif": [],  # Blank entries should cause plots to inherit fonts from the document.
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": r"""\usepackage[utf8x]{inputenc}
\usepackage[T1]{fontenc}
\renewcommand{\vec}[1]{\mathbf{#1}}
\renewcommand{\hat}[1]{\mathbf{#1}}""",  # Plots will be generated using this preamble
    "text.usetex": True,  # Use LaTeX to write all text.
}

DISCRETE_MARKERS = ["1", "2", "3", "4", "x", "o", "v", "^", "<", ">", "s"]


class ResultPlot:
    """Generate a plot using a common formatting.

    Provides utility functions for common Monte Carlo plots as well."""

    def __init__(self, figsize, transpose=False, use_latex=False):
        self.transpose = transpose
        self.legend = False
        self.zebrastripe = False
        self.use_latex = use_latex

        if use_latex:
            self.rc_params = {**DEFAULT_RC_PARAMS, **LATEX_RC_PARAMS}
        else:
            self.rc_params = DEFAULT_RC_PARAMS

        with plt.rc_context(self.rc_params):
            self.fig, self.ax = plt.subplots(figsize=figsize)

        # Set coordinates
        if self.transpose:
            self.dep_tick_ax = self.ax.get_xaxis()
            self.indep_tick_ax = self.ax.get_yaxis()

            self.dep_var = "x"
            self.dep_err = "xerr"
            self.indep_var = "y"
            self.indep_err = "yerr"
        else:
            self.dep_tick_ax = self.ax.get_yaxis()
            self.indep_tick_ax = self.ax.get_xaxis()

            self.dep_var = "y"
            self.dep_err = "yerr"
            self.indep_var = "x"
            self.indep_err = "xerr"

        self.discrete_index = 0

    def set_independent_label(self, label):
        """Set the label on the independent axis."""
        if self.use_latex:
            esc_label = get_latex_string(label)
        else:
            esc_label = get_base_string(label)

        with plt.rc_context(self.rc_params):
            if self.transpose:
                self.ax.set_ylabel(esc_label)
            else:
                self.ax.set_xlabel(esc_label)

    def set_dependent_label(self, label):
        """Set the label on the dependent axis."""
        if self.use_latex:
            esc_label = get_latex_string(label)
        else:
            esc_label = get_base_string(label)

        with plt.rc_context(self.rc_params):
            if self.transpose:
                self.ax.set_xlabel(esc_label)
            else:
                self.ax.set_ylabel(esc_label)

    def set_independent_tick_labels(self, tick_labels, tick_angle):
        """Set the tick labels on the independent axis.
        Must be used with an independent-axis of the form [1, 2, 3, ...]"""
        if self.use_latex:
            esc_tick_labels = [get_latex_string(label) for label in tick_labels]
        else:
            esc_tick_labels = [get_base_string(label) for label in tick_labels]

        if self.transpose:
            tick_angle -= 90

        with plt.rc_context(self.rc_params):
            self.indep_tick_ax.set_ticks(range(len(esc_tick_labels)))
            self.indep_tick_ax.set_ticklabels(esc_tick_labels, rotation=tick_angle)

    def set_dependent_tick_labels(self, tick_labels, tick_angle):
        """Set the tick labels on the dependent axis.
        Must be used with a dependent-axis of the form [1, 2, 3, ...]"""
        if self.use_latex:
            esc_tick_labels = [get_latex_string(label) for label in tick_labels]
        else:
            esc_tick_labels = [get_base_string(label) for label in tick_labels]

        if self.transpose:
            tick_angle -= 90

        with plt.rc_context(self.rc_params):
            self.dep_tick_ax.set_ticks(range(len(esc_tick_labels)))
            self.dep_tick_ax.set_ticklabels(esc_tick_labels, rotation=tick_angle)

    def _plot_basic(self, indep_dat, dep_dat, indep_err=None, dep_err=None, label=None):
        """Generate a basic plot command with no additional frills."""
        if label:
            self.legend = True

        plt_command = {
            self.indep_var: indep_dat,
            self.indep_err: indep_err,
            self.dep_var: dep_dat,
            self.dep_err: dep_err,
        }

        if self.use_latex and label:
            plt_command["label"] = get_latex_string(label)
        else:
            plt_command["label"] = get_base_string(label)

        return plt_command

    def plot_discrete(
        self, indep_dat, dep_dat, indep_err=None, dep_err=None, label=None, **kwargs
    ):
        """Plot a discrete data distribution

        Discrete data is not continuous and has either no or a loose relationship
        with its neighbors."""
        indep_dat = np.array(indep_dat)
        plt_command = self._plot_basic(indep_dat, dep_dat, indep_err, dep_err, label)

        # Special effects for discrete:
        plt_command["marker"] = DISCRETE_MARKERS[self.discrete_index % len(DISCRETE_MARKERS)]
        self.discrete_index += 1

        plt_command["linestyle"] = "None"
        plt_command["linewidth"] = 1
        plt_command["capsize"] = 2

        for k, v in kwargs.items():
            plt_command[k] = v

        with plt.rc_context(self.rc_params):
            self.ax.errorbar(**plt_command)

    def plot_continuous(
        self, indep_dat, dep_dat, indep_err=None, dep_err=None, label=None, **kwargs
    ):
        """Plot data that is nominally continuous in each dimension."""
        indep_dat = np.array(indep_dat)
        plt_command = self._plot_basic(indep_dat, dep_dat, indep_err, None, label)

        # Special effects for continuous:
        plt_command["linewidth"] = 1

        for k, v in kwargs.items():
            plt_command[k] = v

        with plt.rc_context(self.rc_params):
            self.ax.errorbar(**plt_command)
            if dep_err is not None:
                y1 = dep_dat - dep_err
                y2 = dep_dat + dep_err
                if self.transpose:
                    self.ax.fill_betweenx(indep_dat, y1, y2, alpha=0.3)
                else:
                    self.ax.fill_between(indep_dat, y1, y2, alpha=0.3)

    def plot_step(self, indep_dat, dep_dat, dep_err=None, label=None, **kwargs):
        """Plot data that is represented by piecewise continuous data.

        The independent axis is bin edges.  If plotting with `where="post"` (as
        done here), the final point must be duplicated to represent typical
        stairstep behavior."""

        indep_dat = np.array(indep_dat)
        indep_dat = np.append(indep_dat, indep_dat[-1])
        dep_dat_adjusted = np.append(dep_dat, dep_dat[-1])
        plt_command = self._plot_basic(indep_dat, dep_dat_adjusted, None, None, label)

        # Special effects for continuous:
        plt_command["linewidth"] = 1

        for k, v in kwargs.items():
            plt_command[k] = v

        with plt.rc_context(self.rc_params):
            plt_command["drawstyle"] = "steps-post"
            self.ax.errorbar(**plt_command)
            if dep_err is not None:
                dep_err_adjusted = np.append(dep_err, dep_err[-1])
                y_l = dep_dat_adjusted - dep_err_adjusted
                y_h = dep_dat_adjusted + dep_err_adjusted
                if self.transpose:
                    self.ax.fill_betweenx(indep_dat, y_l, y_h, alpha=0.3, step="post")
                else:
                    self.ax.fill_between(indep_dat, y_l, y_h, alpha=0.3, step="post")

    def add_zebrastripe(self):
        """Add zebrastriping to discrete data.
        Useful for high density independent axes."""
        self.zebrastripe = True

    def add_grid(self, dep_grid=True, indep_grid=False):
        """Add a grid to the problem, on either the dependent, independent, or both axes."""
        if dep_grid and indep_grid:
            axis = "both"
        elif dep_grid:
            axis = self.dep_var
        else:
            axis = self.indep_var

        with plt.rc_context(self.rc_params):
            self.ax.grid(lw=1.0, ls="dashed", axis=axis)

    def save(self, output_file, legend_ncol=3):
        """Finalize the plot and save to disk."""
        with plt.rc_context(self.rc_params):
            if self.zebrastripe:
                zebrastripe_color = "#00000010"

                if self.transpose:
                    xlim = self.ax.get_xlim()
                    dep_ticks = self.ax.get_yticks()
                    bar_height = np.ones_like(dep_ticks) * xlim[1] * 1.1
                    bar_height[1::2] = 0
                    self.ax.barh(
                        range(len(dep_ticks)), bar_height, color=zebrastripe_color
                    )
                    self.ax.set_xlim(xlim)
                else:
                    ylim = self.ax.get_ylim()
                    dep_ticks = self.ax.get_xticks()
                    bar_height = np.ones_like(dep_ticks) * ylim[1] * 1.1
                    bar_height[1::2] = 0
                    self.ax.bar(
                        range(len(dep_ticks)), bar_height, color=zebrastripe_color
                    )
                    self.ax.set_ylim(ylim)

            if self.transpose:
                self.ax.invert_yaxis()

            if self.legend:
                self.ax.legend(
                    bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=legend_ncol
                )

            self.fig.tight_layout()

            self.fig.savefig(output_file, bbox_inches="tight")


# ==================================================================================================
class CalcBenchData:
    """
    Calculation and benchmark data class used for holding and manipulating results
    Used for writing tabulated results and plotting results

    Parameters
    ----------
    name : str
        The name of the dataset.
    index : list
        A list of row names of interest in this dataset.
    data : list[dict{str_like, array_like}]
        A list of dictionaries of arrays. The arrays are indexed by `index`.
        The columns are merged together using `vumap`
    vumap : list[dict{str : str_like}]
        Each dictionary gives a mapping between ["val", "unc"] and the output
        column names.
    sort_by: str, optional
        What column to sort the data by.
    formatting: dict{str : formatter}, optional
        For each column name in `data`, provides a formatter object to handle
        Python and siunitx formatting in output.
    """

    def __init__(self, name, index, data, vumap, sort_by=None, formatting=None):
        """
        Initialize data frame to hold data
        """

        self.name = name

        if not isinstance(data, list):
            data = [data]
        self.df = [pd.DataFrame(d, index=index) for d in data]

        if not isinstance(vumap, list):
            vumap = [vumap]
        self.vumap = vumap

        self.formatting = formatting

        self.sort_by = sort_by
        if sort_by is not None:
            for df in self.df:
                df.sort_values(by=[sort_by], inplace=True, kind="mergesort")

        self.default_columns = list()
        for vu in vumap:
            self.default_columns += vu.values()

    def to_string(self, output_file=None, full_table=False):
        """Convert the list of dataframes to a string.

        Parameters
        ----------
        output_file : path-like, optional
            Where to output this LaTeX segment, if necessary.
        full_table : bool, optional
            Should all columns be printed or only those with data?

        Returns
        -------
        string
            The table as a string.
        """

        df = self.df[0]
        for d, vu in zip(self.df[1:], self.vumap[1:]):
            df = pd.concat([df, d[[vu["val"], vu["unc"]]]], axis=1)

        # Convert string text to non-Latex versions
        df = df.applymap(lambda x: get_base_string(x))
        df.rename(columns=lambda x: get_base_string(x), inplace=True)
        default_columns = [get_base_string(column) for column in self.default_columns]
        if self.formatting:
            formatters = {
                get_base_string(column): self.formatting[column].python_formatter()
                for column in self.default_columns
            }
        else:
            formatters = None

        string = "\n{} Calculation Benchmark Results\n".format(self.name)
        string += "\n"
        if full_table:
            segment = df
        else:
            segment = df[default_columns]
        string += segment.to_string(formatters=formatters)

        if self.sort_by is not None:
            sorts = sorted(set(df[self.sort_by]))
            for comparison in sorts:
                string += "\n\n{} Calculation Benchmark Results\n".format(comparison)
                string += "\n"
                if full_table:
                    segment = df[df[self.sort_by] == comparison]
                else:
                    segment = df[df[self.sort_by] == comparison][default_columns]
                string += segment.to_string(formatters=formatters)

        if output_file is not None:
            with open(output_file, "w") as file:
                file.write(string)

        return string

    def to_latex(
        self, output_file=None, full_table=False, include_plots=None, plot_scaling=None, do_resizebox=False
    ):
        """Generate LaTeX representation of results.

        Parameters
        ----------
        output_file : path-like, optional
            Where to output this LaTeX segment, if necessary.
        full_table : bool, optional
            Should all columns be printed or only those with data?
        include_plots : list[path-like], optional
            A list of plot file names to add to the output.
        plot_scaling : list[float], optional
            A corresponding list of scaling arguments for the plots.
        do_resizebox : bool, optional
            Apply resizebox to force the overall LaTeX table width equal to the
            text width.

        Returns
        -------
        string
            The LaTeX as a string.
        """

        df = self.df[0]
        for d, vu in zip(self.df[1:], self.vumap[1:]):
            df = pd.concat([df, d[[vu["val"], vu["unc"]]]], axis=1)

        # Convert string text to Latex versions
        df = df.applymap(lambda x: get_latex_string(x))
        df.rename(columns=lambda x: get_latex_string(x), inplace=True)
        default_columns = [get_latex_string(column) for column in self.default_columns]
        if self.formatting:
            formatting = {
                get_latex_string(column): self.formatting[column]
                for column in self.default_columns
            }
        else:
            formatting = None

        title = "{} Calculation Benchmark Results".format(self.name)
        caption = title
        string = r"\providecommand\includepath{.}"
        string += "\n\n\\clearpage\n\\paragraph{{{}}}\n\n".format(title)
        if include_plots is not None:
            if plot_scaling is None:
                plot_scaling = [1.0 for plot in include_plots]
            string += latex_figure(include_plots[0], caption, plot_scaling[0])

        if full_table:
            segment = df
        else:
            segment = df[default_columns]
        string += latex_table(segment, do_resizebox, caption, formatting)

        if self.sort_by is not None:
            sorts = set(df[self.sort_by])
            for i, comparison in enumerate(sorts):
                title = "{} Calculation Benchmark Results".format(comparison)
                caption = title
                string += "\n\\clearpage\n\\paragraph{{{}}}\n\n".format(title)
                if include_plots is not None:
                    string += latex_figure(
                        include_plots[i + 1], caption, plot_scaling[i + 1]
                    )

                if full_table:
                    segment = df[df[self.sort_by] == comparison]
                else:
                    segment = df[df[self.sort_by] == comparison][default_columns]

                string += latex_table(segment, do_resizebox, caption, formatting)

        if output_file is not None:
            with open(output_file, "w") as file:
                file.write(string)

        return string


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    pass
