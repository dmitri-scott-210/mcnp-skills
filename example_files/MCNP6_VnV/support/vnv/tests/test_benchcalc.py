from context import vnv

import vnv.benchcalc as BC

import os
import pytest


path = os.path.split(os.path.realpath(__file__))[0]

benchA_description = {
    "general_info": {
        "name": "A",
        "misc": {"material": "PU", "number": "1"},
        "description": "some descriptor for benchmark A",
    },
    "execution_info": {
        "arguments": {"bench": "A"},
        "options": ["hello"],
        "outputs": {"output": "A.output"},
    },
    "benchmark_result": {"detector": {"val": 1.000, "std": 0.002}},
}

benchB_description = {
    "general_info": {
        "name": "B",
        "misc": {"material": "U", "number": "1"},
        "description": "some descriptor for benchmark B",
    },
    "execution_info": {
        "arguments": {"bench": "B"},
        "options": ["world"],
        "outputs": {"output": "B.output"},
    },
    "benchmark_result": {"detector": {"val": 1.001, "std": 0.004}},
}


def test_list_mock_bench():

    bench_path = os.path.join(path, "mock_bench")
    tests = ["benchA", "benchB"]

    dir_list = vnv.build_dir_list(bench_path)
    for test in tests:
        assert os.path.join(bench_path, test) in dir_list

    dir_list = vnv.build_dir_list(bench_path, name_only=True)
    for test in tests:
        assert test in dir_list

    with pytest.raises(SystemExit):
        bench_path = os.path.join(path, "MACK_BUNCH")
        dir_list = vnv.build_dir_list(bench_path)


def test_setup_benchmark_suite_calc_directory():

    from_path = os.path.join(path, "mock_bench")
    to_path = os.path.join(path, "mock_calc")
    name1 = "calc1"
    name2 = "calc2"
    tests = ["benchA", "benchB"]

    BC.setup_benchmark_suite_calc_directory(from_path, to_path, name1, tests)
    assert os.path.exists(os.path.join(to_path, name1))
    assert os.path.exists(os.path.join(to_path, name1, tests[0]))
    assert os.path.exists(os.path.join(to_path, name1, tests[1]))

    BC.setup_benchmark_suite_calc_directory(from_path, to_path, name2, tests)
    assert os.path.exists(os.path.join(to_path, name2))
    assert os.path.exists(os.path.join(to_path, name2, tests[0]))
    assert os.path.exists(os.path.join(to_path, name2, tests[1]))

    with pytest.raises(SystemExit):
        BC.setup_benchmark_suite_calc_directory(from_path, to_path, name1, tests)

    vnv.clean(to_path, name1)
    assert os.path.exists(os.path.join(to_path, name2))
    assert not os.path.exists(os.path.join(to_path, name1))

    vnv.clean(to_path)
    assert not os.path.exists(os.path.join(to_path, name2))


def test_read_write_benchmark_json():

    from_path = os.path.join(path, "mock_bench")
    to_path = os.path.join(path, "mock_calc")
    name = "calc"
    tests = ["benchA", "benchB"]
    exe = "echo"

    # test read
    benchmarks = [BC.Benchmark(from_path, test, exe) for test in tests]
    assert benchmarks[0].name == tests[0]
    assert benchmarks[0].info["general_info"] == benchA_description["general_info"]
    assert benchmarks[0].info["execution_info"] == benchA_description["execution_info"]
    assert (
        benchmarks[0].info["benchmark_result"] == benchA_description["benchmark_result"]
    )
    assert benchmarks[1].name == tests[1]
    assert benchmarks[1].info["general_info"] == benchB_description["general_info"]
    assert benchmarks[1].info["execution_info"] == benchB_description["execution_info"]
    assert (
        benchmarks[1].info["benchmark_result"] == benchB_description["benchmark_result"]
    )

    # test write
    BC.setup_benchmark_suite_calc_directory(from_path, to_path, name, tests)
    calc_path = os.path.join(to_path, name)
    benchmarkA = BC.Benchmark(calc_path, tests[0], exe)
    benchmarkA.name = tests[1]
    benchmarkA.write_description_info()
    benchmarkB = BC.Benchmark(calc_path, tests[1], exe)
    assert benchmarkA.name == benchmarkB.name
    assert benchmarkA.info["general_info"] == benchmarkB.info["general_info"]
    assert benchmarkA.info["execution_info"] == benchmarkB.info["execution_info"]
    assert benchmarkA.info["benchmark_result"] == benchmarkB.info["benchmark_result"]

    vnv.clean(to_path)


def test_build_benchmark_commands():

    bench_path = os.path.join(path, "mock_bench")
    test = "benchA"

    benchmark = BC.Benchmark(bench_path, test, "echo")

    aout = benchmark.get_file("outputs", "output")
    assert (
        os.path.split(aout)[1]
        == benchA_description["execution_info"]["outputs"]["output"]
    )

    run = benchmark.execute()
    val = run.wait()

    assert val == 0

    with pytest.raises(SystemExit):
        aout = benchmark.get_file("outputs", "out")

    test = "benchB"
    benchmark = BC.Benchmark(bench_path, test, "echo")
    with pytest.raises(SystemExit):
        bout = benchmark.get_file("outputs", "output")
