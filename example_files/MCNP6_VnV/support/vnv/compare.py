#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite Result Comparison Functions
    + Compute the c/b (calculation/benchmark) values
    + Compute chi-squared and root mean square metrics
"""


# ==================================================================================================


# ==================================================================================================
def c_over_b(calc_val, calc_std, bench_val, bench_std=None):
    """
    Returns lists of c/b, SD(c/b), (c/b-1)/SD(c/b)
    Function to calculate ratio of calculation values to benchmark values.

    Assumes calculation contains an uncertainty
    Benchmark uncertainty is optional
    """

    if not isinstance(calc_val, list):
        calc_val = [calc_val]
    if not isinstance(calc_std, list):
        calc_std = [calc_std]
    if not isinstance(bench_val, list):
        bench_val = [bench_val]
    if bench_std:
        if not isinstance(bench_std, list):
            bench_std = [bench_std]

    cb = [cv / bv if bv else 0 for cv, bv in zip(calc_val, bench_val)]
    if not bench_std:
        cb_std = [
            cv / bv * (cs / cv) if cv and bv else 0
            for cv, cs, bv in zip(calc_val, calc_std, bench_val)
        ]
    else:
        cb_std = [
            cv / bv * ((cs / cv) ** 2 + (bs / bv) ** 2) ** 0.5 if cv and bv else 0
            for cv, cs, bv, bs in zip(calc_val, calc_std, bench_val, bench_std)
        ]

    num_cb_std = [abs(v - 1) / vstd if vstd else 0 for v, vstd in zip(cb, cb_std)]

    return cb, cb_std, num_cb_std


# ==================================================================================================
def chi_squared(calc_val, calc_std, bench_val, bench_std=None):
    """
    Returns list of squared and chi-squared values
    Function to chi-squared value between calculation values and benchmark values.

    Assumes calculation contains an uncertainty
    Benchmark uncertainty is optional
    """

    if not isinstance(calc_val, list):
        calc_val = [calc_val]
    if not isinstance(calc_std, list):
        calc_std = [calc_std]
    if not isinstance(bench_val, list):
        bench_val = [bench_val]
    if bench_std:
        if not isinstance(bench_std, list):
            bench_std = [bench_std]

    sq = [(cv - bv) ** 2 for cv, bv in zip(calc_val, bench_val)]
    if not bench_std:
        chi_sq = [cbsq / (cs ** 2) if cs ** 2 else 0 for cbsq, cs in zip(sq, calc_std)]
    else:
        chi_sq = [
            cbsq / (cs ** 2 + bs ** 2) if (cs ** 2 + bs ** 2) else 0
            for cbsq, cs, bs in zip(sq, calc_std, bench_std)
        ]

    return sq, chi_sq


# ==================================================================================================
# Execute this statement if ran as executable
if __name__ == "__main__":

    pass
