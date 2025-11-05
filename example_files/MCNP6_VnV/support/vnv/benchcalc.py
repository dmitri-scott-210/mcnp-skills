#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite Benchmark Calculations
    + Setting up calculation directory
    + Read/write benchmark objects
    + Process benchmark execution into commandline objects
"""


# ==================================================================================================
import os
import re
import sys
import shutil
import json

from . import commandline


# ==================================================================================================
def setup_benchmark_suite_calc_directory(from_path, to_path, calc_name, test_names):
    """
    Copies tests in test_names from from_path to new calculations to_path/calc_name directory.
    """

    os.makedirs(to_path, exist_ok=True)

    calc_path = os.path.join(to_path, calc_name)
    try:
        os.mkdir(calc_path)
    except FileExistsError:
        sys.exit(
            "\nError: {} directory already exists, either delete or try new name\n".format(
                calc_path
            )
        )

    for test in test_names:
        test_from = os.path.join(from_path, test)
        test_to = os.path.join(calc_path, test)
        shutil.copytree(test_from, test_to)

    return calc_path


# ==================================================================================================
class Benchmark:
    """
    Benchmark class used for reading/writing of descriptions where the benchmark
    information is contained
    Can also build benchmark cd and exe commands
    """

    def __init__(self, path, name, executable, clopts=None):
        """
        Initialize and read benchmark info description.json file
        """

        self.path = path
        self.name = name

        self.read_description_info()

        self.build_exe_command(executable, clopts=clopts)

    def read_description_info(self):
        """Parse the description.json file."""

        with open(
            os.path.join(self.path, self.name, "description.json"), "r"
        ) as desc_file:
            self.info = json.load(desc_file)

    def write_description_info(self):
        """Generate the description.json file."""

        with open(
            os.path.join(self.path, self.name, "description.json"), "w"
        ) as desc_file:
            json.dump(self.info, desc_file, indent=2)

    def build_exe_command(self, executable, clopts):
        """Add a simulation command for this benchmark."""
        if not executable:
            self.exe_cmd = None
            return

        exec_info = self.info["execution_info"]

        self.exe_cmd = commandline.Command(
            executable, os.path.join(self.path, self.name)
        )

        if "arguments" in exec_info:
            for key, value in exec_info["arguments"].items():
                self.exe_cmd.append(["{}={}".format(key, value)])

        if "options" in exec_info:
            self.exe_cmd.append(exec_info["options"])
        
        if clopts is not None:
            self.exe_cmd.append([clopts])

    def execute(self, delay_output=False):
        """Returns the executed process for this benchmark."""

        if self.exe_cmd:
            return self.exe_cmd.execute(delay_output)
        else:
            raise Exception("No executable to execute.")

    def get_file(self, group, name):
        """Try to load the named simulation file under the group."""

        group_files = self.info["execution_info"][group]
        try:
            file = os.path.join(self.path, self.name, group_files[name])
        except KeyError:
            sys.exit(
                """
Error: {} : {} file is not listed in description.json file
""".format(
                    group, name
                )
            )

        if not os.path.exists(file):
            sys.exit(
                "\nError: {} file does not exist.  Either setup failed, simulation is not "
                "complete, or an error occured prior to completion\n".format(file)
            )

        return file

    def rewrite_file(self, group, name, rewrite):
        """Rewrite a specific file group/name with rewrite regex substitution."""

        file = self.get_file(group, name)
        with open(file, "r") as handle:
            file_contents = handle.read()
        for change in rewrite:
            file_contents = re.sub(change[0], change[1], file_contents)
        with open(file, "w") as handle:
            handle.write(file_contents)


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    pass
