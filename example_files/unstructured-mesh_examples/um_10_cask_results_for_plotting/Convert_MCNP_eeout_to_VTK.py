#!/usr/bin/env python
#
# Execute as: Convert_MCNP_eeout_to_VTK.py <file.eeout>
#
# Code:     Convert_MCNP_eeout_to_VTK, version 1.2.0
#
# Authors:  Joel A. Kulesza (jkulesza@lanl.gov)
#           Tucker C. McClanahan (tcmcclan@lanl.gov) 
#           Monte Carlo Methods, Codes & Applications
#           X Computational Physics Division
#           Los Alamos National Laboratory
#
# Copyright (c) 2019 Triad National Security, LLC.  All rights reserved.
#
# This material was produced under U.S. Government contract 89233218NCA000001
# for Los Alamos National Laboratory, which is operated by Triad National
# Security, LLC for the U.S. Department of Energy.  The Government is granted
# for itself and others acting on its behalf a paid-up, nonexclusive,
# irrevocable worldwide license in this material to reproduce, prepare
# derivative works, and perform publicly and display publicly.  Beginning five
# (5) years after February 14, 2018, subject to additional five-year worldwide
# renewals, the Government is granted for itself and others acting on its behalf
# a paid-up, nonexclusive, irrevocable worldwide license in this material to
# reproduce, prepare derivative works, distribute copies to the public, perform
# publicly and display publicly, and to permit others to do so.  NEITHER THE
# UNITED STATES NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR TRIAD NATIONAL
# SECURITY, LLC, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR
# IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY,
# COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR PROCESS
# DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED
# RIGHTS.

import os
import re
import sys

# Find the start and end positions for the first matching sublist in a list.
def find_sublist( sl, l ):
    sll=len( sl )
    for ind in ( i for i,e in enumerate( l ) if e == sl[ 0 ] ):
        if( l[ ind:ind+sll ] == sl ):
            return ind,ind+sll-1

# Extract a certain number of entries (length) following a sublist (sublist) for
# a given input list (inlist).
def extract_sublist_entries( sublist, length, inlist ):
    lp1 = find_sublist( sublist, inlist )[ 1 ] + 1
    lp2 = lp1 + length
    return inlist[ lp1:lp2 ]

# Calculate the connected nodes for various element types.
def calculate_connectivity_list_length( e_types ):
    connectivity_list_length = []
    for e in e_types:
        if( e == '4' ):
            connectivity_list_length.append( 4 )
        elif( e == '5' ):
            connectivity_list_length.append( 6 )
        elif( e == '6' ):
            connectivity_list_length.append( 8 )
        elif( e == '14' ):
            connectivity_list_length.append( 10 )
        elif( e == '15' ):
            connectivity_list_length.append( 15 )
        elif( e == '16' ):
            connectivity_list_length.append( 20 )
    return connectivity_list_length

# Convert eeout element types to VTK element types.
def calculate_vtk_e_types( e_types ):
    vtk_e_types = []
    for e in e_types:
        if( e == '4'):
            vtk_e_types.append( '10' )
        elif( e == '5' ):
            vtk_e_types.append( '13' )
        elif( e == '6' ):
            vtk_e_types.append( '12' )
        elif( e == '14' ):
            vtk_e_types.append( '24' )
        elif( e == '15' ):
            vtk_e_types.append( '26' )
        elif( e == '16' ):
            vtk_e_types.append( '25' )
    return vtk_e_types

# Create flat list of 3D vertices from individual coordinate lists.
def create_vertices( xs, ys, zs ):
    v = []
    for n,x in enumerate( xs ):
        v.append( xs[ n ] )
        v.append( ys[ n ] )
        v.append( zs[ n ] )
    return(v)

# Reformat list to print its elements nicely within the XML file.
def pretty_print_list( indent, cols, colwidths, inlist ):
    pretty_list_string = indent * ' '
    for n,i in enumerate( inlist ):
        pretty_list_string += str( i ).rjust( colwidths ) + ' '
        if( n % cols == cols - 1 ):
            pretty_list_string += '\n' + indent * ' '
    pretty_list_string += '\n'
    return pretty_list_string

# Perform various sanity checks on edit results.
def perform_edit_checks( edit_values, total_elements, check_gap = True ):
    found_negative = False
    found_nan = False
    max_val = -1e308
    min_nz_val = 1e308
    min_val = 1e308

    # Custom float conversion for Fortran-formatted numbers missing an "e" and
    # with three digits in the exponent.
    def floatf( x ):
        try:
            rv = float( x )
        except:
            rv = float( x[0:-4] + 'e' + x[-4:] )
        return rv

    edit_values = [ floatf(i) for i in edit_values ]

    if( len( edit_values ) == total_elements + 1 ):
        gap_value = edit_values[ 0 ]
        if( gap_value > 0 and check_gap ):
            print( 'WARNING: gap value: {:}'.format( gap_value ) )
    else:
        print( 'ERROR: Unexpected edit length, exiting' )
        exit()

    # The first edit entry is for gaps --- discard for plotting.
    edit_values = edit_values[ 1: ]
    for ev in edit_values:
        if( ev < 0 and found_negative == False ):
            print( 'WARNING: Negative edit entry found.' )
            found_negative = True
        if( ev != ev and found_nan == False ):
            print( 'WARNING: NaN edit entry found.  Setting to 1e308.' )
            found_nan = True
        if( ev < min_nz_val and ev > 0.0 ): min_nz_val = ev
        if( ev < min_val ): min_val = ev
        if( ev > max_val ): max_val = ev

    if( found_nan == True ):
        edit_values = [ 1e308 if ev != ev else ev for ev in edit_values  ]

    print( '    Maximum          value: {:.5e}'.format( max_val ) )
    print( '    Minimum positive value: {:.5e}'.format( min_nz_val ) )
    print( '    Minimum          value: {:.5e}'.format( min_val ) )

    edit_values = [ '{:.5e}'.format( i ) for i in edit_values ]

    return edit_values

# Separate into list and parse into results and relative uncertainties, if
# appropriate.
def get_results( edit_values, edit_number, total_elements ):
    edit_results = []
    tmp = edit_values.split('DATA SETS')[1:]
    edit_sets = [tmp[i] for i in range(len(tmp)) if 'RESULT SQR TIME BIN' not in tmp[i]]
    sublists = [ ['RESULT', 'TIME'] if 'RESULT TIME' in edit_sets[i] else ['REL', 'ERROR', 'TIME'] for i in range(len(edit_sets))]
    count = -1
    for s in sublists:
        count += 1
        edit_data = extract_sublist_entries( s, total_elements + 1 + 26, edit_sets[count].split() )
        # Get supplemental edit-identifying information.
        time_bin   = edit_data[2]
        time_value = edit_data[7]
        erg_bin    = edit_data[16]
        erg_value  = edit_data[21]

        # Construct unique name.
        edit_name = 'EDIT_{:}_{:}_TIME_BIN_{:}_MAX_TIME_{:}_ENERGY_BIN_{:}_MAX_ENERGY_{:}'.format( \
            edit_number, s[-2], time_bin, time_value, erg_bin, erg_value )

        # Extract only edit data values and validate.
        edit_data = edit_data[26:]
        print( '    Processing & Validating {:}...'.format( edit_name ) )
        check_gap = (not 'ERROR' in s ) # Don't check gap for error arrays.
        edit_data = perform_edit_checks( edit_data, total_elements, check_gap )
        edit_results.append( [ edit_name, edit_data ] )

    return edit_results

################################################################################

import __main__ as main
if(__name__ == '__main__' and hasattr(main, '__file__')):

    # Validate command line arguments.
    if( len( sys.argv ) != 2 ):
        print( 'ERROR: Incorrect number of command line arguments provided ('
            + str( len( sys.argv ) ) + '); those provided:' )
        print( sys.argv )
        exit()

    if( not os.path.isfile( sys.argv[ 1 ] ) ):
        print( 'ERROR: MCNP EEOUT file not found.' )
        exit()

    infilename = sys.argv[1]

    print( 'Processing {:}...'.format( infilename ) )

    with open ( infilename, 'r' ) as myfile:
        eeout = myfile.read()

    # Determine number of nodes and cells.
    nodes  = int( re.search( r'NUMBER OF NODES\s*:\s+(\d+)',     eeout ).group( 1 ) )
    tets1  = int( re.search( r'NUMBER OF 1st TETS\s*:\s+(\d+)',  eeout ).group( 1 ) )
    pents1 = int( re.search( r'NUMBER OF 1st PENTS\s*:\s+(\d+)', eeout ).group( 1 ) )
    hexs1  = int( re.search( r'NUMBER OF 1st HEXS\s*:\s+(\d+)',  eeout ).group( 1 ) )
    tets2  = int( re.search( r'NUMBER OF 2nd TETS\s*:\s+(\d+)',  eeout ).group( 1 ) )
    pents2 = int( re.search( r'NUMBER OF 2nd PENTS\s*:\s+(\d+)', eeout ).group( 1 ) )
    hexs2  = int( re.search( r'NUMBER OF 2nd HEXS\s*:\s+(\d+)',  eeout ).group( 1 ) )
    total_elements = tets1 + pents1 + hexs1 + tets2 + pents2 + hexs2

    # Retrieve edit information.
    edit_list = re.findall( r'(DATA OUTPUT PARTICLE.*?)\n', eeout, re.S )

    print( '  Found {:} edit(s).'.format( len( edit_list ) ) )

    # Capture edit data for use later.
    eeout_edits = re.search( r'(DATA OUTPUT.*?)CENTROIDS', eeout, re.S ).group( 1 )

    # Capture header information.
    eeout_header = re.search( r'(.*?)NODES X', eeout, re.S ).group( 1 )
    eeout_header = re.sub( r'\s+\n', '\n', eeout_header )
    eeout_header = re.sub( r'\n+', '\n', eeout_header )
    eeout_header = re.sub( r'^', '#  ', eeout_header )
    eeout_header = re.sub( r'\n', '\n#  ', eeout_header )

    # Reformat eeout to list to permit easy reading of list data.
    eeout = eeout.replace( '\n', '' )
    eeout = eeout.split( ' ' )
    eeout = list( filter( None, eeout ) )

    # Remove head of file to make matching easier.
    eeout = eeout[ find_sublist( [ 'NODES', 'X', '(cm)' ], eeout )[ 0 ]: ]

    # Find the list positions for the first and last nodes.
    x_coords    = extract_sublist_entries( ['NODES', 'X', '(cm)'], nodes, eeout )
    y_coords    = extract_sublist_entries( ['NODES', 'Y', '(cm)'], nodes, eeout )
    z_coords    = extract_sublist_entries( ['NODES', 'Z', '(cm)'], nodes, eeout )
    e_types     = extract_sublist_entries( ['ELEMENT', 'TYPE'], total_elements, eeout )
    e_materials = extract_sublist_entries( ['ELEMENT', 'MATERIAL'], total_elements, eeout )

    # Process connectivity list.
    connectivity_list_elements = calculate_connectivity_list_length( e_types )
    connectivities = []
    if( '4' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '1ST', 'ORDER', 'TETS', 'ELEMENT', 'ORDERED' ],
            4 * e_types.count( '4' ), eeout )
    if( '5' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '1ST', 'ORDER', 'PENTS', 'ELEMENT', 'ORDERED' ],
            6 * e_types.count( '5' ), eeout )
    if( '6' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '1ST', 'ORDER', 'HEXS', 'ELEMENT', 'ORDERED' ],
            8 * e_types.count( '6' ), eeout )
    if( '14' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '2ND', 'ORDER', 'TETS', 'ELEMENT', 'ORDERED' ],
            10 * e_types.count( '14' ), eeout )
    if( '15' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '2ND', 'ORDER', 'PENTS', 'ELEMENT', 'ORDERED' ],
            15 * e_types.count( '15' ), eeout )
    if( '16' in e_types ):
        connectivities += extract_sublist_entries(
            [ 'CONNECTIVITY', 'DATA', '2ND', 'ORDER', 'HEXS', 'ELEMENT', 'ORDERED' ],
            20 * e_types.count( '16' ), eeout )

    densities = extract_sublist_entries(
        [ 'DENSITY', '(gm/cm^3)' ],
        total_elements, eeout )

    volumes = extract_sublist_entries(
        [ 'VOLUMES', '(cm^3)' ],
        total_elements, eeout )

    # Create list of vertices from individual coordinate lists.
    vertices = create_vertices( x_coords, y_coords, z_coords )

    # Subtract one from all vertex IDs in the connectivity list (to make
    # zero-indexed).
    connectivities = [ str( int( x ) - 1 ) for x in connectivities ]

    # Accumulate offset list. Reproduce np.cumsum to avoid NumPy dependency.
    def cumsum( inlist ):
        cumlist = [ 0 ]
        for n,i in enumerate( inlist ):
            cumlist.append( cumlist[n] + inlist[n] )
        return cumlist[1:]
    offsets = cumsum( connectivity_list_elements )
    offsets = [ str( x ) for x in offsets ]

    # Convert eeout element types to VTK element types.
    vtk_e_types = calculate_vtk_e_types( e_types )

    # Open up output vtu (unstructured mesh VTK) file.
    f = open( infilename + '.vtu', 'w' )

    # Write header comments (but a long header does not work), default: off.
    if( False ):
        [ f.write( '<!-- ' + l + ' -->\n' ) for l in eeout_header.split( '\n' ) ]
        f.write( '<!--' + '\n' )
        f.write( 80 * '#' + '\n' )
        f.write( '# EEOUT Header Follows' + '\n' )
        f.write( 80 * '#' + '\n' )
        f.write( eeout_header + '\n' )
        f.write( 80 * '#' + '\n' )
        f.write( '-->' + '\n' )

    f.write( '<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">' + '\n' )
    f.write( '  <UnstructuredGrid>' + '\n' )
    f.write( '    <Piece NumberOfPoints="' + str( nodes ) + '" NumberOfCells="' + str( total_elements ) + '">' + '\n' )
    f.write( '      <CellData Scalars="scalars">' + '\n' )
    f.write( '        <DataArray type="Int32" Name="material" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 10, 5, e_materials ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '        <DataArray type="Float64" Name="density" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 5, 13, densities ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '        <DataArray type="Float64" Name="volume" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 5, 13, volumes ) )
    f.write( '        </DataArray>' + '\n' )

    # Output edit information.  Edits may have corresponding relative
    # uncertainties.  Edits may be binned by energy and/or time.
    if( len( edit_list ) > 0 ):
        for e in edit_list:
            particle_type = re.search( r'PARTICLE : (\d+)', e ).group( 1 )
            edit_type = re.search( r'TYPE : (.*?)$', e ).group( 1 )
            edit_number = re.search( r'TYPE : .*?_(\d+)$', e ).group( 1 )
            print( '  Processing {:} edit...'.format( edit_type ) )
            myregex = '({:}.*?)(:?DATA OUTPUT PARTICLE|$)'.format( e )
            edit_data = re.search( myregex, eeout_edits, re.S ).group( 1 )
            edit_results = get_results( edit_data, edit_number, total_elements )
            for er in edit_results:
                f.write( '        <DataArray type="Float64" Name="' + er[0]+ '" format="ascii">' + '\n' )
                f.write( pretty_print_list( 10, 5, 13, er[1] ) )
                f.write( '        </DataArray>' + '\n' )

    f.write( '      </CellData>' + '\n' )
    f.write( '      <Points>' + '\n' )
    f.write( '        <DataArray type="Float64" NumberOfComponents="3" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 3, 13, vertices ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '      </Points>' + '\n' )
    f.write( '      <Cells>' + '\n' )
    f.write( '        <DataArray type="Int32" Name="connectivity" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 8, 5, connectivities ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '        <DataArray type="Int32" Name="offsets" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 10, 5, offsets ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '        <DataArray type="UInt8" Name="types" format="ascii">' + '\n' )
    f.write( pretty_print_list( 10, 20, 2, vtk_e_types ) )
    f.write( '        </DataArray>' + '\n' )
    f.write( '      </Cells>' + '\n' )
    f.write( '    </Piece>' + '\n' )
    f.write( '  </UnstructuredGrid>' + '\n' )
    f.write( '</VTKFile>' + '\n' )

    f.close()
