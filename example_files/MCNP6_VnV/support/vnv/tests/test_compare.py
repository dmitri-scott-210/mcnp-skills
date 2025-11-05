from context import vnv

import vnv.compare as C


def test_c_over_b():

    ref_c_v = 2
    ref_c_s = 0.1
    ref_b_v = 1
    ref_b_s = 0.2

    ref_cb = ref_c_v / ref_b_v
    ref_cb_std = ref_cb * ((ref_c_s / ref_c_v) ** 2 + (ref_b_s / ref_b_v) ** 2) ** 0.5
    ref_num_cb_std = (ref_cb - 1) / ref_cb_std

    cb, cb_std, num_cb_std = C.c_over_b(ref_c_v, ref_c_s, ref_b_v, ref_b_s)
    assert [ref_cb] == cb
    assert [ref_cb_std] == cb_std
    assert [ref_num_cb_std] == num_cb_std

    cb, cb_std, num_cb_std = C.c_over_b([ref_c_v], [ref_c_s], [ref_b_v], [ref_b_s])
    assert [ref_cb] == cb
    assert [ref_cb_std] == cb_std
    assert [ref_num_cb_std] == num_cb_std

    ref_cb_std = ref_c_s / ref_b_v
    ref_num_cb_std = (ref_cb - 1) / ref_cb_std

    cb, cb_std, num_cb_std = C.c_over_b(ref_c_v, ref_c_s, ref_b_v)
    assert [ref_cb] == cb
    assert [ref_cb_std] == cb_std
    assert [ref_num_cb_std] == num_cb_std


def test_chi_squared():

    ref_c_v = 2
    ref_c_s = 0.1
    ref_b_v = 1
    ref_b_s = 0.2

    ref_sq = (ref_c_v - ref_b_v) ** 2
    ref_chi_sq = ref_sq / (ref_c_s ** 2 + ref_b_s ** 2)

    sq, chi_sq = C.chi_squared(ref_c_v, ref_c_s, ref_b_v, ref_b_s)
    assert [ref_sq] == sq
    assert [ref_chi_sq] == chi_sq

    sq, chi_sq = C.chi_squared([ref_c_v], [ref_c_s], [ref_b_v], [ref_b_s])
    assert [ref_sq] == sq
    assert [ref_chi_sq] == chi_sq

    ref_chi_sq = ref_sq / ref_c_s ** 2

    sq, chi_sq = C.chi_squared(ref_c_v, ref_c_s, ref_b_v)
    assert [ref_sq] == sq
    assert [ref_chi_sq] == chi_sq
