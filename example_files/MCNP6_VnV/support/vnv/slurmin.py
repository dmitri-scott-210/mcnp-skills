#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite SLURM support
    + Minimal sbatch support (create file and sbatch command)
"""


# ==================================================================================================
import os
import subprocess
import time

from . import commandline


def get_array(problem_count, stride):
    """ Returns sbatch --array input for the problem."""
    if stride <= 1:
        return "0-{}".format(problem_count - 1)
    return "0-{}:{}".format(problem_count - 1, stride)


# ==================================================================================================
class SlurmManager:
    """ Generates and executes slurm sbatch scripts"""

    def __init__(
        self,
        job_name,
        executable,
        script_path,
        working_directory,
        problem_count,
        jobs,
        stride,
        ntrd,
        mpi_provider,
        nmpi,
        nodes,
        time,
        pre_cmds,
        post_cmds,
        clopts,
    ):
        self.job_name = job_name
        self.executable = executable
        self.script_path = script_path
        self.working_directory = working_directory
        self.problem_count = problem_count
        self.jobs = jobs
        self.stride = stride
        self.ntrd = ntrd
        self.mpi_provider = mpi_provider
        self.nmpi = nmpi
        self.nodes = nodes
        self.time = time

        self.pre_cmds = pre_cmds
        self.post_cmds = post_cmds

        self.clopts = clopts

        self.filename = os.path.join(
            self.working_directory, job_name, "{}.sbatch".format(job_name)
        )

        self.slurm_id = 0

    def generate_sbatch(self):
        """Generate an sbatch script using batch syntax"""
        sbatch_str = ""

        output_path = os.path.join(self.working_directory, self.job_name)

        # Create header
        sbatch_str += "#!/bin/bash\n"
        sbatch_str += "#SBATCH --nodes={}\n".format(self.nodes)
        sbatch_str += "#SBATCH --time={}\n".format(self.time)
        sbatch_str += '#SBATCH --chdir="{}"\n'.format(os.getcwd())
        sbatch_str += "#SBATCH --job-name={}\n".format(self.job_name)
        sbatch_str += "#SBATCH --array={}\n".format(
            get_array(self.problem_count, self.stride)
        )
        sbatch_str += '#SBATCH --output="{}/{}.%A_%a.out"\n'.format(
            output_path, self.job_name
        )
        sbatch_str += '#SBATCH --error="{}/{}.%A_%a.error"\n\n'.format(
            output_path, self.job_name
        )

        # Allow users to add setup commands
        if isinstance(self.pre_cmds, list):
            for command in self.pre_cmds:
                sbatch_str += "{}\n".format(command)
        else:
            sbatch_str += "{}\n".format(commands)

        sbatch_str += "\n"

        vnv_path = os.path.join(self.script_path, "VnV.py")

        # Set up execution
        sbatch_str += '"{}" execute --calcdir_name={} --ntrd={} --nmpi={} --nodes={} --run_index=$SLURM_ARRAY_TASK_ID --jobs={} --stride={}'.format(
            vnv_path,
            self.job_name,
            self.ntrd,
            self.nmpi,
            self.nodes,
            self.jobs,
            self.stride,
        )

        if self.mpi_provider:
            sbatch_str += " --mpi_provider={}".format(self.mpi_provider)

        if self.executable:
            sbatch_str += " --executable_name={}".format(self.executable)
        
        if self.clopts is not None:
            sbatch_str += f" --clopts {self.clopts}"

        sbatch_str += "\n\n"

        # # Allow users to add close commands
        if isinstance(self.post_cmds, list):
            for command in self.post_cmds:
                sbatch_str += "{}\n".format(command)
        else:
            sbatch_str += "{}\n".format(commands)

        with open(self.filename, "w") as file:
            file.write(sbatch_str)

    def execute(self):
        """Executes the sbatch function."""
        sbatch = subprocess.run(
            ["sbatch", "--parsable", self.filename], stdout=subprocess.PIPE
        )

        self.slurm_id = sbatch.stdout.decode()

    def wait(self):
        """ Check job status every 10 minutes. """
        done = False
        while not done:
            time.sleep(600)
            process = subprocess.run(
                ["squeue", "-j", "-h", self.slurm_id], stdout=subprocess.PIPE
            )
            if not process.stdout or process.returncode != 0:
                # Process is either done, or something malfunctioned
                done = True


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    pass
