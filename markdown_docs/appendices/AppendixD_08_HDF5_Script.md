---
title: "Appendix D.8 - Script to Generate HDF5 File Layouts"
chapter: "D.8"
source_pdf: "mcnp631_theory_user-manual/appendecies/D.8_Script_to_Generate_HDF5_File_Layouts.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## D.8 Script to Generate HDF5 File Layouts

The script used to generate some of the L A T E X dirtree listings in
this document by traversing an HDF5 file is given in Listing D.14.

```
1 #!/usr/bin/env python 2 3 4 class H5dirtree: 5 def __ init __ (self, basename="/", offset=0): 6 self.basename = basename 7 self.offset = offset 8 self.items = [] 9 10 def __ call __ (self, h5name, h5obj): 11 import os 12 13 # Nesting depth. 14 d = h5name.count("/") + self.offset 15 n = os.path.basename(h5name) 16 separator = "{\color{lightgray}\dotfill}" 17 label = ( 18 "{\color[HTML]{1b9e77}(dataset)}" 19 if isinstance(h5obj, h5py.Dataset) 20 else "{\color[HTML]{d95f02}(group)}" 21 ) 22 self.items.append(d * " " + ".{:} {:}{:}{:}".format(d, n, separator, label)) 23 e = d + 1 24 separator = "{\color{lightgray}\dotfill}" 25 label = "{\color[HTML]{7570b3}(attribute)}" 26 for k, v in h5obj.attrs.items(): 27 self.items.append( 28 e * " " + ".{:} {:}{:}{:}".format(e, k, separator, label) 29 ) 30 31 def make _ dirtree(self): 32 s = "\dirtree{%\n" 33 s += ".1 {:}.\n".format(self.basename) 34 for i in h5dt.items: 35 s += "{:}.\n".format(i.replace(" _ ", r"\ _ ")) 36 s += "}" 37 self.dirtree = s 38 39 40 import __ main __ as main 41 42 if __ name __ == " __ main __ " and hasattr(main, " __ file __ "): 43 44 import argparse 45 import h5py 46 import os 47 import textwrap 48 49 description = textwrap.dedent( 50 """ 51 This script is used to traverse HDF5 files and collect the hierarchy to be 52 printed in a tree-like way.
```

Listing D.14: HDF5 Hierarchy Printing Utility Script (print\_dirtree.py.txt)