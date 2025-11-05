vnv - a suite of general verification and validation tools
===

Used to support general setup, execution, post processing, and documentation of multiple suites of integrated verification and validation test problems.

# System Requirements

[Python 3](https://www.python.org/)

# Using vnv tools

## Intended application

* Listing of tests / test suites
* Setup a suite of tests to run
* Execute a suite of tests
* Post process tests to retrieve results
* Document and plot results
* Clean temporary calculation/document directories

## Example usage

```python
import vnv

bench_path  = 'experiments'
bench_names = vnv.build_dir_list(bench_path,name_only=True)

parser = vnv.commandline.build_command_line_parser(bench_names)
args   = vnv.commandline.parse_and_check_args(parser,bench_names)

calc_dir  = 'calculations'
calc_name = 'release-X.Y.Z'
calc_path = vnv.benchcalc.setup_benchmark_suite_calc_directory(bench_path,calc_dir,calc_name,bench_names)

benchmarks = [vnv.benchcalc.Benchmark(calc_path,name,args.executable)  for name in bench_names]

vnv.commandline.execute(benchmarks, args.jobs)

outputs = [b.get_output_file('output')  for b in benchmarks]
# Now things may be very specific to the code that produced the results
for o in outputs:
    # Process this output file to collect results
```

## Example test suite structure

Each benchmark or test problem will be contained within a single directory.  This is where everything about the test is located, including

1. Input file(s)
2. Material file(s)
3. Auxilary documents
4. JSON description file

The contents of the benchmark directories will be copied during a calculation setup.

An example JSON description file is shown below:

```json
{
  "general_info": {
    "name": "JEZPU",
    "icsbep_name": {
      "material": "PU",
      "form": "MET",
      "spectrum": "FAST",
      "number": "001",
      "case": ""
    },
    "description": "Bare sphere of plutonium"
  },
  "execution_info": {
    "arguments": {
      "i": "JEZPU",
      "n": "JEZPU"
    },
    "outputs": {
      "outp": "JEZPUo",
      "mctal": "JEZPUm"
    },
    "inputs": {
      "inp": "JEZPU"
    }
  },
  "experiment_data": {
    "k-eff": {
      "val": 1.0,
      "std": 0.002
    }
  }
}
```

At a minimum, the tests within a single benchmark suite shall be described in a consistent fashion, i.e. "general\_info" should be consistently laid out across the benchmarks.  The "execution\_info" object determines how the benchmark calculation is setup, executed, and what outputs to expect.

# Testing vnv tools

Executing `pytest` in the `tests` directory runs all unit tests.  A `mock_bench` test suite is provided in the `tests` directory.
