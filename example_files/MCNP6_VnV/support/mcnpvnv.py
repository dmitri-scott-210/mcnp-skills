#!/usr/bin/env python3
# ==================================================================================================
"MCNP specific V&V helper functions"

# ==================================================================================================
import itertools
import sys

import numpy as np

import vnv
import datetime


# ==================================================================================================
def build_mcnp_benchmark(
    path,
    name,
    executable=None,
    mpi_provider=None,
    nodes=1,
    nmpi=1,
    ntrd=1,
    clopts=None,
):
    """
    MCNPBenchmark builder with specific call signature including nmpi and ntrd.
    """

    if not executable:
        if nmpi != 1:
            executable = "mcnp6.mpi"
        else:
            executable = "mcnp6"

    benchmark = MCNPBenchmark(path, name, executable, clopts)
    benchmark.build_mcnp_command(
        mpi_provider=mpi_provider, nodes=nodes, nmpi=nmpi, ntrd=ntrd,
    )

    return benchmark


# ==================================================================================================
class MCNPBenchmark(vnv.benchcalc.Benchmark):
    """
    Derived class of the general vnv.benchcalc.Benchmark class
    Specialization where the mcnp exe command may be built with threads
    """

    def __init__(self, path, name, executable=None, clopts=None):
        """
        Initialize and read benchmark info description.json file
        """
        self.exe_cmd = None

        super().__init__(path, name, executable, clopts)

    def build_mcnp_command(
        self, mpi_provider=None, nodes=1, nmpi=1, ntrd=1,
    ):
        """
        Add MCNP-specific options needed for the mcnp execution command for this benchmark.
        """

        if nmpi > 1:
            self.exe_cmd.prepend_mpirun(nodes, nmpi, ntrd, provider=mpi_provider)
        if ntrd > 1:
            self.exe_cmd.append(["tasks", str(ntrd)])


# ==================================================================================================
def format_code_version_date(code_name, version, probid):
    """Returns consistently formatted code, version and date"""

    code = code_name.upper()
    vers = version
    try:
        date = datetime.datetime.strptime(probid, "%m/%d/%y %H:%M:%S").strftime("%Y-%m-%d")
    except ValueError:
        date = ""

    return code, vers, date


# ==================================================================================================
def get_code_version_from_mctal(mctal_file):
    """Return mctal header information"""

    from mcnptools import Mctal

    mctal = Mctal(mctal_file)
    code = mctal.GetCode()
    vers = mctal.GetVersion()
    prob = mctal.GetProbid()

    return format_code_version_date(code, vers, prob)


# ==================================================================================================
def get_code_version_from_outp(outp_file):
    """Return output file information"""

    code = ""
    vers = ""
    prob = ""

    with open(outp_file, "r") as file:
        for line in file:
            if line.startswith("1mcnp"):
                split_line = line.split()
                if len(split_line) > 0:
                    code = split_line[0][1:]
                    if len(split_line) > 2:
                        vers = split_line[2]
                    if len(split_line) > 5:
                        prob = " ".join(split_line[4:6])
                    break

    return format_code_version_date(code, vers, prob)


# ==================================================================================================
def get_keff_from_mctal(mctal_file):
    """Return mctal cumulative col/abs/trk-len keff value and standard deviation"""

    from mcnptools import Mctal, MctalKcode

    mctal = Mctal(mctal_file)
    kcode = mctal.GetKcode()

    keff = kcode.GetValue(MctalKcode.AVG_COMBINED_KEFF)
    kstd = kcode.GetValue(MctalKcode.AVG_COMBINED_KEFF_STD)

    return keff, kstd


# ==================================================================================================
def get_tally_from_mctal(mctal_file, tally_id, abscissa_id=None):
    """Return mctal tally bins, values, and standard deviations"""

    from mcnptools import Mctal, MctalTally

    tfc = MctalTally.TFC
    mctal = Mctal(mctal_file)
    try:
        tally = mctal.GetTally(tally_id)
    except RuntimeError:
        sys.exit(
            "\nError: Either mctal_file {} or tally_id {} does not exist\n".format(
                mctal_file, tally_id
            )
        )

    abscissa_ids = {
        "facet": {"pos": 0, "getter": tally.GetFBins},
        "flag": {"pos": 1, "getter": tally.GetDBins},
        "user": {"pos": 2, "getter": tally.GetUBins},
        "seg": {"pos": 3, "getter": tally.GetSBins},
        "mult": {"pos": 4, "getter": tally.GetMBins},
        "cosine": {"pos": 5, "getter": tally.GetCBins},
        "energy": {"pos": 6, "getter": tally.GetEBins},
        "time": {"pos": 7, "getter": tally.GetTBins},
    }

    bins = None
    vals = list()
    errs = list()
    arg = [tfc, tfc, tfc, tfc, tfc, tfc, tfc, tfc]

    # Process a tally with a single value/error result (most likely case).
    if abscissa_id is None:
        vals.append(tally.GetValue(*arg))
        errs.append(tally.GetError(*arg))

        return bins, vals, errs

    def validate_abscissa_id(abscissa_id):
        """Validate that the user-specified abscissa is available."""
        if abscissa_id not in abscissa_ids:
            sys.exit(
                "\nError: {} abscissa_id not in {}\n".format(
                    abscissa_id, abscissa_ids.keys()
                )
            )

    # Process a single-requested abscissa_id (second most likely case).
    if isinstance(abscissa_id, str):
        validate_abscissa_id(abscissa_id)

        bins_getter = abscissa_ids[abscissa_id]["getter"]
        bins = list(bins_getter())

        for i in range(len(bins)):
            arg[abscissa_ids[abscissa_id]["pos"]] = i
            vals.append(tally.GetValue(*arg))
            errs.append(tally.GetError(*arg))

    # Process **all** tally values and return as a simple NumPy object to behave
    # my "Pythonically" by avoiding returning an MCNPTools object.  In the
    # future, handling select dimensions (e.g., just energy and time) can be
    # incorporated.
    elif isinstance(abscissa_id, tuple):
        try:
            assert abscissa_id == (
                "facet",
                "flag",
                "user",
                "seg",
                "mult",
                "cosine",
                "energy",
                "time",
            )
        except AssertionError as err:
            # This approach is taken to permit transition to logging and raised
            # exceptions.
            sys.exit(f"\nError: Subselected abscissae with tuple not yet supported\n")
            raise err

        # Capture bin upper boundaries and compute number of each sets of bins.
        bins = list()
        for a_id in abscissa_id:
            bins_getter = abscissa_ids[a_id]["getter"]
            bins.append(list(bins_getter()))
        num_bins = tuple(len(b) for b in bins)

        # Capture results into a pre-allocated numpy container with bogus
        # initial values to check for before returning.
        vals = np.inf * np.ones(num_bins)
        errs = np.inf * np.ones(num_bins)

        dim_ranges = [range(len(abscissa_ids[key]["getter"]())) for key in abscissa_id]
        for arg in itertools.product(*dim_ranges):
            vals[arg] = tally.GetValue(*arg)
            errs[arg] = tally.GetError(*arg)

        # Ensure all placeholders have been overwritten with reasonable values.
        assert np.all(np.isfinite(vals))
        assert np.all(np.isfinite(errs))

        return bins, vals, errs

    else:
        sys.exit(f"\nError: {abscissa_id} is not a string or tuple of strings\n")

    return bins, vals, errs
