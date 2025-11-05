import numpy as np

from context import vnv

from vnv.formatters import FixedPoint, FixedPrecision


def test_fixed_point():
    x = FixedPoint(1)
    data = np.array([0.001, 0.12345, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["0.0", "0.1", "1.2", "10.0"]
    assert x.siunitx_formatter(data) == "S[table-format=2.1]"

    data = np.array([0.001, 0.12345, 1.16, 1.0])
    assert x.siunitx_formatter(data) == "S[table-format=1.1]"

    data = np.array([0.001, 0.12345, 1.16, -1.0])
    assert x.siunitx_formatter(data) == "S[table-format=2.1]"

    x = FixedPoint(3)
    data = np.array([0.001, 0.12345, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["0.001", "0.123", "1.160", "10.000"]
    assert x.siunitx_formatter(data) == "S[table-format=2.3]"

    data = np.array([0.001, 0.001, 0.001, 0.001])
    assert x.siunitx_formatter(data) == "S[table-format=1.3]"


def test_fixed_precision():
    x = FixedPrecision(1)
    data = np.array([0.001, 0.12346, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["0.0010", "0.12", "1.2", "10."]
    assert x.siunitx_formatter(data) == "S[table-format=2.4]"

    data = np.array([0.001, 0.12346, 1.16, 1.0])
    assert x.siunitx_formatter(data) == "S[table-format=1.4]"

    data = np.array([0.001, 0.12346, 1.16, -1.0])
    assert x.siunitx_formatter(data) == "S[table-format=2.4]"

    x = FixedPrecision(3)
    data = np.array([0.001, 0.12346, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["0.001000", "0.1235", "1.160", "10.00"]
    assert x.siunitx_formatter(data) == "S[table-format=2.6]"

    data = np.array([0.001, 0.001, 0.001, 0.001])
    assert x.siunitx_formatter(data) == "S[table-format=1.6]"

    data = np.array([1.001, 0.9999])
    assert x.siunitx_formatter(data) == "S[table-format=1.4]"

    data = np.array([-1001.0])
    result = [formatter(val) for val in data]
    assert result == ["-1001."]
    assert x.siunitx_formatter(data) == "S[table-format=5.0]"

    data = np.array([-10000.0])
    result = [formatter(val) for val in data]
    assert result == ["-1.000e+04"]
    assert x.siunitx_formatter(data) == "S[table-format=2.3e1]"


def test_fixed_precision_scientific():
    x = FixedPrecision(1, scientific=True)
    data = np.array([0.001, 0.12346, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["1.0e-03", "1.2e-01", "1.2e+00", "1.0e+01"]
    assert x.siunitx_formatter(data) == "S[table-format=1.1e2]"

    data = np.array([0.001, 0.12346, 1.16, 1.0])
    assert x.siunitx_formatter(data) == "S[table-format=1.1e2]"

    data = np.array([0.001, 0.12346, 1.16, -1.0])
    assert x.siunitx_formatter(data) == "S[table-format=2.1e2]"

    x = FixedPrecision(3, scientific=True)
    data = np.array([0.001, 0.12346, 1.16, 10.0])
    formatter = x.python_formatter()
    result = [formatter(val) for val in data]

    assert result == ["1.000e-03", "1.235e-01", "1.160e+00", "1.000e+01"]
    assert x.siunitx_formatter(data) == "S[table-format=1.3e2]"

    data = np.array([0.001, 0.001, 0.001, 0.001])
    assert x.siunitx_formatter(data) == "S[table-format=1.3e2]"
