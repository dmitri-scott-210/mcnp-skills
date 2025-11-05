Verification, Validation, and Statistical Testing Framework
===========================================================

The `vnvstats` collection of Python scripts provides a consistent framework and set of capabilities that can be used to setup, execute, post-process, and document verification and validation (V&V) test suites.  The final product of this package includes individual suite plain text (TXT), TeX, PDF, and PNG files to be used in V&V test results reporting.

System Requirements
-------------------

Component                                      | Latest Version Tested | Notes
-----------------------------------------------|-----------------------|------
[Python](https://www.python.org/)              | 3.9.7                 | Minimum version 3.2.
[Matplotlib](https://matplotlib.org/)          | 3.6.2                 |
[NumPy](https://numpy.org/)                    | 1.23.5                |
[Pandas](https://pandas.pydata.org/)           | 1.5.2                 | The latest release issues a `FutureWarning` message indicating some features of the Pandas API may change in the future.
[pytest](https://docs.pytest.org/)             | 7.2.0                 | Optional.
[MCNPTools](https://github.com/lanl/mcnptools) | 5.3.1                 | Minimum version 3.8.0.
[LaTeX](https://www.latex-project.org/)        | TeX Live 2021         | Optional.

Installation
------------

This collection of scripts is not installed in a typical Pythonic manner (e.g,. using `pip`) rather individual scripts are executed in place.

Usage
-----

Before using the utility, the directory structure is important to understand.  The incomplete directory and file layout is:

```
+ vnvstats
|   LICENSE
|   README.md
+-- support
|     mcnpvnv.py
+---- vnv
+------ tests
+-- validation
+---- criticality
|       VnV.py
+------ experiments
+------ references
+---- crit_expanded
+---- laqgsm
+---- lockwood
+---- pulsed_spheres
+---- rossi
+-- verification
+---- keff
|       VnV.py
+------ problems
+------ references
+---- kobayashi
```

The `support` directory includes all of the general (within the `vnv` directory) and MCNP-specific (`mcnpvnv.py`) V&V functionality that handles the majority of the setup, execution, post-processing, and documentation steps.

A `VnV.py` Python script is included within each `validation` and `verification` suite.  This script is executed for each individual suite and includes suite-specific functionality.

For the `validation` suites, an `experiments` directory contains each of the individual benchmarks with input files and a `description.json` file that includes benchmark-specific information, execution instructions, and the experimental results.  For the `verification` suites, a `problems` directory contains each of the individual benchmarks with input files and a `description.json` file that includes benchmark-specific information, execution instructions, and the analytical results.

All the `validation` and `verification` suites include a `references` directory.  Calculational results from different versions of the code are stored for archiving and comparison purposes.

Using the `criticality` suite as an example, the general approach to running a single suite of benchmarks is:
```bash
cd validation/criticality
python3 VnV.py setup --calcdir_name EXAMPLE
python3 VnV.py execute --calcdir_name EXAMPLE
python3 VnV.py postprocess --calcdir_name EXAMPLE
python3 VnV.py document --calcdir_name EXAMPLE
```

The above commands will, in order:
1. Change directory into the `validation/criticality` folder.
2. Setup a copy of the contents of the `experiments` directory into a new relative directory named `calculations/EXAMPLE`.
3. Execute all of the benchmarks contained in the `calculations/EXAMPLE` directory.
4. Post-process all of the benchmark outputs contained in the `calculations/EXAMPLE` directory.  Each of the individual benchmark problem `description.json` files are updated with the calculational results.
5. Retrieve the `calculations/EXAMPLE` benchmark problem `description.json` files and gathers the experimental and calculational results.  The results are used in generating plots and tables of information useful in creating a V&V report.

Because some of the test suites require significant computational time, the framework supports [Slurm Workload Manager](https://slurm.schedmd.com/) computing cluster submission capabilities.  To use the Slurm capabilities to submit to a cluster backend, the `execute` option is replaced by `execute_slurm` such that step #3 is now:

```bash
python3 VnV.py execute_slurm --calcdir_name EXAMPLE
```

This will generate and submit a Slurm sbatch script that includes a similar `python3 VnV.py execute --calcdir_name EXAMPLE` command that is executed on the node when the allocation is granted and the job begins.  Of course, this requires that Slurm is installed on the system where the submission is taking place.

Documentation
-------------

Further documentation on the usage of each of the `VnV.py` scripts within the `validation` and `verification` suites is found through the help options.  For example,

```bash
python3 VnV.py --help
```

provides helpful information about the main execution modes available: `list`, `setup`, `execute`, `execute_slurm`, `postprocess`, `document`, and `clean`.  Each mode contains its own help functionality, e.g.,

```bash
python3 VnV.py execute --help
```

reports all of the options and flags relevant to executing the benchmarks, including how to specify the executable, run in parallel, etc.

For the release of MCNP6.3.0, the experimental and calculated contents (e.g., plots and tables) of the [V&V testing report](http://permalink.lanl.gov/object/tr?what=info:lanl-repo/lareport/LA-UR-22-32951) were generated using the `vnvstats` package.  All of the MCNP6.3.0 calculated results are stored within the `references/MCNP630*` directory for each test suite.
