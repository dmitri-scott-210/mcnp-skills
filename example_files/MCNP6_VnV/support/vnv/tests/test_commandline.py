from context import vnv

import vnv.benchcalc as BC
import vnv.commandline as CL

import os
import shutil
import sys
import pytest


def test_command_line_parser():

    sys.argv = ["test", "list"]
    tests = [""]
    parser, _ = CL.build_command_line_parser(tests)
    args = CL.parse_and_check_args(parser, tests)

    assert args.command

    sys.argv = ["test", "setup", "A"]
    tests = ["A", "B"]
    parser, _ = CL.build_command_line_parser(tests)
    args = CL.parse_and_check_args(parser, tests)

    assert args.command
    for test in args.tests:
        assert test in tests

    sys.argv = ["test", "setup", "C"]
    tests = ["A", "B"]
    parser, _ = CL.build_command_line_parser(tests)
    with pytest.raises(SystemExit):
        args = CL.parse_and_check_args(parser, tests)


def test_command():
    path = os.getcwd()

    # Test simple execution
    cmd = CL.Command("pwd", path)
    run = cmd.execute(delay_output=True)
    stdout, stderr = run.communicate()

    assert stdout.decode().replace("\n", "") == str(path)

    # Test exe not in path
    with pytest.raises(Exception):
        cmd = CL.Command("random_garbled_text_TPCpTa5FCr", path)

    # Test append
    cmd = CL.Command("echo", path)
    cmd.append(["tasks", "8"])

    assert cmd.args == ["echo", "tasks", "8"]

    cmd.append("I=input.inp")

    assert cmd.args == ["echo", "tasks", "8", "I=input.inp"]

    # Test exe with complex path
    ls_path = shutil.which("ls")
    head, tail = os.path.split(ls_path)

    cmd = CL.Command("echo", path, path=head)

    # Test prepend
    cmd = CL.Command("echo", path)
    cmd.prepend(["mpiexec", "-np", "8"])

    assert cmd.args == ["mpiexec", "-np", "8", "echo"]

    cmd.prepend("executable")

    assert cmd.args == ["executable", "mpiexec", "-np", "8", "echo"]

    # Test basic MPI
    cmd = CL.Command("echo", path)
    cmd.prepend_mpirun(4, 8, 4, provider="default")

    assert cmd.args == ["mpirun", "-np", "8", "echo"]

    # Test openmpi MPI
    cmd = CL.Command("echo", path)
    cmd.prepend_mpirun(4, 8, 4, provider="openmpi")

    assert cmd.args == ["mpirun", "--map-by", "ppr:2:node:pe=4", "echo"]

    with pytest.raises(SystemExit):
        cmd = CL.Command("echo", path)
        cmd.prepend_mpirun(5, 8, 4, provider="openmpi")
