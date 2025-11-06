#!/usr/bin/env python
"""
HDF5 Directory Tree Generator

Purpose: Generate hierarchical tree visualization of HDF5 file structure
Source: MCNP6.3.1 Theory & User Manual, Appendix D.8
Usage: python h5_dirtree.py <h5filename> [--group /path/to/group]

This script traverses an HDF5 file and generates a LaTeX dirtree representation
of its structure, including groups, datasets, and attributes.

Example:
    python h5_dirtree.py runtpe.h5
    python h5_dirtree.py runtpe.h5 --group /results
"""

import argparse
import h5py
import os
import sys
import textwrap


class H5dirtree:
    """Generate LaTeX dirtree representation of HDF5 structure"""

    def __init__(self, basename="/", offset=0):
        """
        Initialize H5dirtree generator

        Parameters:
            basename (str): Root group name for display
            offset (int): Indentation offset for nested structures
        """
        self.basename = basename
        self.offset = offset
        self.items = []

    def __call__(self, h5name, h5obj):
        """
        Callback for h5py visititems - processes each HDF5 object

        Parameters:
            h5name (str): Relative path of object in HDF5 file
            h5obj: h5py Group or Dataset object
        """
        # Nesting depth
        d = h5name.count("/") + self.offset
        n = os.path.basename(h5name)
        separator = "{\\color{lightgray}\\dotfill}"

        # Determine object type
        label = (
            "{\\color[HTML]{1b9e77}(dataset)}"
            if isinstance(h5obj, h5py.Dataset)
            else "{\\color[HTML]{d95f02}(group)}"
        )

        # Add item line
        self.items.append(d * " " + ".{:} {:}{:}{:}".format(d, n, separator, label))

        # Add attributes
        e = d + 1
        separator = "{\\color{lightgray}\\dotfill}"
        label = "{\\color[HTML]{7570b3}(attribute)}"
        for k, v in h5obj.attrs.items():
            self.items.append(
                e * " " + ".{:} {:}{:}{:}".format(e, k, separator, label)
            )

    def make_dirtree(self):
        """Generate LaTeX dirtree string from collected items"""
        s = "\\dirtree{%\n"
        s += ".1 {:}.\n".format(self.basename)
        for i in self.items:
            s += "{:}.\n".format(i.replace("_", r"\_"))
        s += "}"
        self.dirtree = s


def main():
    """Main entry point for command-line usage"""
    description = textwrap.dedent(
        """
        This script is used to traverse HDF5 files and collect the hierarchy to be
        printed in a tree-like way.

        The output is in LaTeX dirtree format for documentation purposes.
        """
    )

    epilog = textwrap.dedent(
        """
        Typical command line calls might look like:

        > python """
        + os.path.basename(__file__)
        + """ <h5filename> -g results
        """
        + "\u2063"
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog,
    )

    # Required positional argument(s)
    parser.add_argument("h5filename", type=str, help="HDF5 file to parse")

    # Optional named argument(s)
    parser.add_argument(
        "--group",
        "-g",
        type=str,
        default="/",
        help="parser start point (i.e., assumed root level)",
    )

    args = parser.parse_args()

    # Open HDF5 file
    try:
        f = h5py.File(args.h5filename, "r")
    except Exception as e:
        print("Couldn't process {:}".format(args.h5filename))
        print("Error: {}".format(e))
        sys.exit(1)

    # Get group
    try:
        r = f.get(args.group)
    except Exception as e:
        print("Couldn't get group {:}".format(args.group))
        print("Error: {}".format(e))
        sys.exit(1)

    if r is None:
        print("Group '{}' not found in {}".format(args.group, args.h5filename))
        sys.exit(1)

    # Generate tree
    h5dt = H5dirtree(basename=args.group, offset=2)
    r.visititems(h5dt)
    h5dt.make_dirtree()
    print(h5dt.dirtree)

    f.close()


if __name__ == "__main__":
    main()
