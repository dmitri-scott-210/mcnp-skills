#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite Command Line Stuff
    + General parser and parser checks
    + CommandArgument < Command < CommandLine classes
    + Exists method for Command and CommandLine
    + Execution of Command & CommandLine objects
"""

# ==================================================================================================
import datetime
import argparse
import os
import sys
import shutil
import subprocess
import time
from collections import OrderedDict


# ==================================================================================================
def build_command_line_parser(available_tests, executable=""):
    """
    Returns general (un-parsed) command line parser
    """

    main_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""V&V Suite Command Line Tool.
This tool automates the process of running and examining the results of our V&V suites.

The general workflow is setup -> execute -> postprocess -> document.""",
    )

    # Arguments used by all functionality
    verbose_arg = argparse.ArgumentParser(add_help=False)

    verbose_arg.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Provide verbose output to stdout and log.",
    )

    # Arguments used by all but list
    path_arg = argparse.ArgumentParser(add_help=False)

    path_arg.add_argument(
        "-N",
        "--calcdir_name",
        default=datetime.datetime.now().isoformat(),
        help="Unique name for current calculation directory",
    )

    # Arguments used by run and slurm
    execute_args = argparse.ArgumentParser(add_help=False)

    execute_args.add_argument(
        "-X",
        "--executable_name",
        default=executable,
        help="Name of executable for current calculation",
    )

    execute_args.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="Execute current calculations concurrently.",
    )

    execute_args.add_argument(
        "--mpi_provider",
        choices=["basic", "openmpi"],
        default="basic",
        help="""MPI implementation.  "basic" uses "mpirun -np".  "openmpi" uses "mpirun --map-by".""",
    )

    execute_args.add_argument(
        "-m",
        "--nmpi",
        type=int,
        default=1,
        help="Set number of MPI ranks. Must be evenly divisible by --nodes.",
    )

    execute_args.add_argument(
        "-t",
        "--ntrd",
        type=int,
        default=1,
        help="Setup current calculations to be run using threading.",
    )

    execute_args.add_argument(
        "--nodes",
        type=int,
        default=1,
        help="Number of nodes V&V will run across, default 1 node",
    )

    execute_args.add_argument(
        "--stride",
        type=int,
        default=None,
        help="How many runs per SBatch job.  Defaults to 1 for execute, all for execute_slurm.",
    )

    execute_args.add_argument(
        "--clopts",
        type=str,
        default=None,
        help="""Additional command line options to be used in the MCNP execution. For example, "--clopts 'xsdir=xsdir_jeff33'" if JEFF 3.3 nuclear data are available in the DATAPATH with the corresponding cross-section directory file, "xsdir_jeff33".""",
    )

    commands = main_parser.add_subparsers(
        title="commands", dest="command", required=True
    )

    command_args = {}

    command_args["list"] = commands.add_parser(
        "list",
        parents=[verbose_arg],
        description="List all available tests.",
        help="List all available tests.",
    )

    command_args["setup"] = commands.add_parser(
        "setup",
        parents=[path_arg, verbose_arg],
        description="Preprocess and setup current calculations.",
        help="Preprocess and setup current calculations.",
    )

    command_args["execute"] = commands.add_parser(
        "execute",
        parents=[path_arg, verbose_arg, execute_args],
        description="Run EXECUTABLE for current calculation.",
        help="Run EXECUTABLE for current calculation.",
    )

    command_args["execute_slurm"] = commands.add_parser(
        "execute_slurm",
        parents=[path_arg, verbose_arg, execute_args],
        description="Generate and run an sbatch script for current calculation.",
        help="Generate and run an sbatch script for current calculation.",
    )

    command_args["postprocess"] = commands.add_parser(
        "postprocess",
        parents=[path_arg, verbose_arg],
        description="Postprocess all results",
        help="Postprocess all results",
    )

    command_args["document"] = commands.add_parser(
        "document",
        parents=[path_arg, verbose_arg],
        description="Collect, summarize and document results.",
        help="Collect, summarize and document results.",
    )

    command_args["clean"] = commands.add_parser(
        "clean",
        parents=[path_arg, verbose_arg],
        description="Clean temporary calculation and document directories.",
        help="Clean temporary calculation and document directories.",
    )

    # Setup specific
    command_args["setup"].add_argument(
        "tests",
        nargs="*",
        default=available_tests,
        help="List of tests to setup",
    )

    # Run specific
    command_args["execute"].add_argument(
        "--run_index",
        type=int,
        default=None,
        help="Enumerated run to execute (used internally)",
    )

    # Slurm specific
    command_args["execute_slurm"].add_argument(
        "--wait",
        action="store_true",
        help="""Wait for slurm to finish executing before continuing.
                Polling rate is limited to once every 10 minutes to minimize load.""",
    )

    command_args["execute_slurm"].add_argument(
        "--time",
        default=60,
        help="Number of minutes for slurm allocation, default 60 minutes",
    )

    command_args["execute_slurm"].add_argument(
        "--pre_cmd",
        action="append",
        default=list(),
        help="Sbatch script commands executed before calculations",
    )

    command_args["execute_slurm"].add_argument(
        "--post_cmd",
        action="append",
        default=list(),
        help="Sbatch script commands executed after calculations",
    )

    # Documentation specific
    command_args["document"].add_argument(
        "--latex_plots",
        action="store_true",
        help="""Render plots using LaTeX.
                Requires Matplotlib have access to a working LaTeX.""",
    )

    command_args["document"].add_argument(
        "--compare",
        action="append",
        default=list(),
        help="""List of paths to executed and postprocessed calculations to compare results.
                Example use: ./VnV.py document --calcdir_name MCNP630 --compare references/MCNP620""",
    )

    return main_parser, command_args


# ==================================================================================================
def parse_and_check_args(parser, available_tests):
    """
    Checks that the arguments make sense
      1) tests if the args.tests exist in available_tests
      2) checks that jobs, nmpi, ntrd, and nodes are greater than or equal to 1
    """

    args = parser.parse_args()
    if args.command == "setup":
        for test in args.tests:
            if test not in available_tests:
                sys.exit(
                    """
Error: {} not in list of available tests. Try list option to see available tests.
""".format(
                        test
                    )
                )

    if args.command == "execute" or args.command == "execute_slurm":
        if args.jobs < 1:
            sys.exit("Error: -j, --jobs needs to be greater than or equal to 1.")
        if args.nmpi < 1:
            sys.exit("Error: -m, --nmpi needs to be greater than or equal to 1.")
        if args.ntrd < 1:
            sys.exit("Error: -t, --ntrd needs to be greater than or equal to 1.")
    if args.command == "execute_slurm":
        if args.nodes < 1:
            sys.exit("Error: -n, --nodes needs to be greater than or equal to 1.")

    # Handle different strides depending on command.
    if args.command == "execute" and not args.stride:
        args.stride = 1
    if args.command == "execute_slurm" and not args.stride:
        args.stride = len(available_tests)

    return args


# ===========================
class Command:
    def __init__(self, exe, cwd, path=""):
        """
        Initializes a Command object and sets the path to and the name
        of the exe.

        Command arguments are set by assigning members to the object
        argument dictionary.  This is done through the add_arg member
        function.  The key, value pairs are then read from the object
        dictionary when printing and executing the command.  Command
        arguments are set to an empty dictionary upon construction.

        Checks the command object at the end of construction for
        existence of the exe.
        """

        self.cwd = cwd

        self.args = [os.path.join(path, exe)]
        if not os.path.isfile(self.args[0]) and not shutil.which(exe):
            raise Exception(
                "Unable to find executable at {} or {}".format(self.args[0], exe)
            )

    def append(self, new_args):
        """Add argument in the command."""

        if isinstance(new_args, list):
            for argument in new_args:
                self.args.append(argument)
        else:
            self.args.append(new_args)

    def prepend(self, new_args):
        """Prepend components to command."""

        if isinstance(new_args, list):
            for i in range(len(new_args)):
                self.args.insert(i, new_args[i])
        else:
            self.args.insert(0, new_args)

    def prepend_mpirun(self, n_nodes, n_processes, n_threads, provider="default"):
        """Prepend mpirun."""

        if n_processes % n_nodes != 0:
            sys.exit(
                "Error: number of processes not evenly divisible by number of nodes."
            )

        if provider == "openmpi":
            map_by = "ppr:{}:node:pe={}".format(int(n_processes / n_nodes), n_threads)
            prepend_val = ["mpirun", "--map-by", map_by]
        else:
            prepend_val = ["mpirun", "-np", str(n_processes)]

        self.prepend(prepend_val)

    def execute(self, delay_output=False):
        """Run this command and return the execution handle."""
        if delay_output:
            proc = subprocess.Popen(
                self.args,
                cwd=str(self.cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            proc = subprocess.Popen(self.args, cwd=str(self.cwd))
        return proc


# ==================================================================================================
def execute(command_list, n_jobs):
    """Execute the command list. Run n_jobs runs at the same time"""
    started = 0
    complete = 0
    in_flight = dict()
    n_commands = len(command_list)
    # Delayed output can stall runs on Windows
    delay_output = n_jobs > 1 and not os.name == "nt"

    while complete != n_commands:
        # Maintain n_jobs
        while len(in_flight) != n_jobs and started != n_commands:
            print("Started Simulation {}".format(command_list[started].name))

            in_flight[command_list[started].name] = command_list[started].execute(
                delay_output=delay_output
            )
            started += 1

        # Don't busy-wait
        time.sleep(1)

        # Check if any simulations have finished, and output if so
        remove_list = []
        for key, process in in_flight.items():
            if isinstance(process.poll(), int):
                if delay_output:
                    outs, errs = process.communicate()
                    print("Output of Simulation {}:".format(key))
                    print(outs.decode())
                    print(errs.decode())
                remove_list.append(key)
                complete += 1

        # Clear subprocess handles
        for item in remove_list:
            in_flight.pop(item)


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    pass
