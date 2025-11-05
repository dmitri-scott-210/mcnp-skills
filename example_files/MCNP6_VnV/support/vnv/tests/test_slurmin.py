from context import vnv

import vnv.slurmin as SL

import filecmp
import os
import shutil


def test_slurm_manager():
    """Generates a file, compares against reference."""

    pre_cmds = ["mkdir test", "cd test"]
    post_cmds = ["cd ..", "rm -rf test"]

    manager = SL.SlurmManager(
        "slurm_test",
        "mcnp6.mpi",
        "path_to_vnv",
        "calculations",
        10,
        2,
        4,
        20,
        "openmpi",
        30,
        40,
        50,
        pre_cmds,
        post_cmds,
        None
    )

    pwd = os.getcwd()

    path = os.path.join("calculations", "slurm_test")

    os.makedirs(path, exist_ok=True)

    ref = """#!/bin/bash
#SBATCH --nodes=40
#SBATCH --time=50
#SBATCH --chdir="{}"
#SBATCH --job-name=slurm_test
#SBATCH --array=0-9:4
#SBATCH --output="calculations/slurm_test/slurm_test.%A_%a.out"
#SBATCH --error="calculations/slurm_test/slurm_test.%A_%a.error"

mkdir test
cd test

"path_to_vnv/VnV.py" execute --calcdir_name=slurm_test --ntrd=20 --nmpi=30 --nodes=40 --run_index=$SLURM_ARRAY_TASK_ID --jobs=2 --stride=4 --mpi_provider=openmpi --executable_name=mcnp6.mpi

cd ..
rm -rf test
""".format(
        pwd
    )

    try:
        manager.generate_sbatch()
        with open(os.path.join(path, "slurm_test.sbatch"), "r") as file:
            data = file.read()
        assert data == ref
    finally:
        shutil.rmtree("calculations", ignore_errors=True)
