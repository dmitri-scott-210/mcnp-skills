#!/usr/bin/env python3
# ==================================================================================================
""" V&V Suite Formatting Library
Provides format styles useful for output and clean table layout.
"""


# ==================================================================================================
import numpy as np

# ==================================================================================================


class FixedPoint:
    """Fixed point handler, generates 'p' zeros past the decimal.

    Parameters
    ----------
    p : int
        The number of digits past the decimal to always print.
    """

    def __init__(self, p):
        self.p = p

    def python_formatter(self):
        """Generates a fixed point python formatter lambda.

        Returns
        -------
        function
            A function of the form `string = fun(float)`
        """
        return f"{{:0.{self.p}f}}".format

    def siunitx_formatter(self, data):
        """Generates a fixed point siunitx Latex table formatter.

        Parameters
        ----------
        data : array_like
            The data to be formatted.

        Returns
        -------
        string
            The siunitx formatter statement.
        """

        data_copy = np.abs(data[data != 0.0])
        leading_digits = max(int(np.max(np.log10(data_copy))) + 1, 1)
        if any(data < 0.0):
            leading_digits += 1

        return f"S[table-format={leading_digits}.{self.p}]"


class FixedPrecision:
    """Fixed precision handler. Will maintain p significant figures.

    Significant zeros are always printed.

    Parameters
    ----------
    p : int
        The number of significant figures to maintain.
    scientific : bool, optional
        If True, always use scientific notation regardless of exponent magnitude.
        If False, follow the Python `g` formatting rules.
    """

    def __init__(self, p, scientific=False):
        self.p = p
        self.scientific = scientific

    def python_formatter(self):
        """Generates a fixed precision Python formatter lambda.

        Returns
        -------
        function
            A function of the form `string = fun(float)`
        """
        if self.scientific:
            return f"{{:0.{self.p}e}}".format
        return f"{{:#0.{self.p + 1}g}}".format

    def siunitx_formatter(self, data):
        """Generates a fixed precision siunitx LaTeX table formatter.

        Parameters
        ----------
        data : array_like
            The data to be formatted.

        Returns
        -------
        string
            The siunitx formatter statement.
        """

        # Scan table for digits in highest power
        x = np.array(data)
        x[x == 0.0] = 1
        log10_data = np.log10(np.abs(x))
        mag_pow = int(np.max(np.abs(log10_data)))
        if mag_pow == 0:
            pow_count = 0
        else:
            pow_count = int(np.floor(np.log10(mag_pow))) + 1
        if np.min(log10_data) < 0:
            pow_count += 1

        exponent_term = ""
        if self.scientific:
            leading_digits = 1
            trailing_digits = self.p
            if pow_count > 0:
                exponent_term = f"e{pow_count}"
        else:
            # Find if we need an exponent for the default 'g' behavior.
            above_p = log10_data >= (self.p + 1)
            below_4 = log10_data < -4

            need_exp = np.any(above_p) or np.any(below_4)
            log10_data[above_p] = 0.0
            log10_data[below_4] = 0.0

            max_pow = int(np.floor(np.max(log10_data)))
            min_pow = int(np.floor(np.min(log10_data)))

            leading_digits = max(1, max_pow + 1)
            trailing_digits = max(self.p - min_pow, 0)
            if need_exp:
                exponent_term = f"e{pow_count}"

        if np.any(data < 0.0):
            # Add space for leading minus sign
            leading_digits += 1

        return f"S[table-format={leading_digits}.{trailing_digits}{exponent_term}]"


DEFAULT_FLOAT_FORMAT = FixedPrecision(6)
