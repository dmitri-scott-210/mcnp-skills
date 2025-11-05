"""MCNP Verification, Validation and Statistical Testing

This library provides the infrastructure necessary for automated V&V testing of MCNP.
"""

import os
import shutil

from .commandline import *
from .benchcalc import *
from .compare import *
from .formatters import *
from .slurmin import *
from .plotndoc import *


# ==================================================================================================
nuclear_data_label = {
    "endf66": "ENDF/B-VI",
    "endf70": "ENDF/B-VII.0",
    "endf71": "ENDF/B-VII.1",
    "endf80": "ENDF/B-VIII.0",
    "jeff33": "JEFF-3.3",
}


# ==================================================================================================
def build_dir_list(path, name_only=False):
    """
    Build a directory listing.  If name_only, provide list of directories
    in path, otherwise provide list of full paths to directories.
    """

    if os.path.isdir(path):
        with os.scandir(path) as directories:
            if name_only:
                dir_list = [
                    entry.name
                    for entry in directories
                    if not entry.name.startswith(".") and entry.is_dir()
                ]
            else:
                dir_list = [
                    os.path.join(path, entry.name)
                    for entry in directories
                    if not entry.name.startswith(".") and entry.is_dir()
                ]
    else:
        sys.exit("\nError: {} path does not exist.\n".format(path))

    dir_list.sort()

    return dir_list


# ==================================================================================================
def clean(path, name=None):
    """
    Clean path of all directories.  If name is provided, only removes this directory in path.
    """

    if name is None:
        dir_list = build_dir_list(path)
    else:
        dir_list = [os.path.join(path, name)]

    for directory in dir_list:
        shutil.rmtree(directory)
