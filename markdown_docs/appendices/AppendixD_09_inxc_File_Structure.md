---
title: "Appendix D.9 - inxc File Structure"
chapter: "D.9"
source_pdf: "mcnp631_theory_user-manual/appendecies/D.9_inxc_File_Structure.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

```
53 """ 54 ) 55 56 epilog = textwrap.dedent( 57 """ 58 Typical command line calls might look like: 59 60 > python """ 61 + os.path.basename( __ file __ ) 62 + """ <h5filename> -g results 63 """ 64 + u"\u2063" 65 ) 66 67 parser = argparse.ArgumentParser( 68 formatter _ class=argparse.RawDescriptionHelpFormatter, 69 description=description, 70 epilog=epilog, 71 ) 72 73 # Required positional argument(s). 74 parser.add _ argument("h5filename", type=str, help="HDF5 file to parse") 75 76 # Optional named argument(s). 77 parser.add _ argument( 78 "--group", 79 "-g", 80 type=str, 81 default="/", 82 help="parser start point (i.e., assumed root level)", 83 ) 84 85 args = parser.parse _ args() 86 87 try: 88 f = h5py.File(args.h5filename, "r") 89 except: 90 print("Couldn't process {:}".format(args.h5filename)) 91 raise 92 93 try: 94 r = f.get(args.group) 95 except: 96 print("Couldn't get group {:}".format(args.group)) 97 raise 98 99 h5dt = H5dirtree(basename=args.group, offset=2) 100 r.visititems(h5dt) 101 h5dt.make _ dirtree() 102 print(h5dt.dirtree)
```

## D.9 inxc File Structure

The inxc input is based on a 128-column 'card' format and each requested
case may require as many as seven cards. With the exception of the
formatted title cards, all data provided in the inxc file are entered as

list-directed input. Repeat counts are allowed. A forward slash ( / )
may be used to terminate an input line; unread variables following a
slash are assigned the default value(s). A description of the seven
input cards follows:

glyph[negationslash]

| Card 1   | 80-character problem title   |                                                                                                                             |
|----------|------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Card 2   | ncase kplot l _ res          |                                                                                                                             |
|          | ncase                        | Defines the number of desired double-differential cross- section edits (DEFAULT: 0).                                        |
|          | kplot                        | If nonzero, write cross-section edits to the MCNP6 mctal file (DEFAULT: 0). Plotting is available only with the mctal file. |
|          | l _ res                      | If l _ res = 0 , no residual nuclei are calculated; if l _ res = 0 , perform a residual nuclei edit (DEFAULT: 0).           |

For each of the ncase cases, repeat the following cards 3 through 7, as
required.

| Card 3:   | 128-character case title          | 128-character case title                                                                                                                                                                                                                                                                                                           |
|-----------|-----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Card 4:   | nerg nang ntype fnorm imom iyield | nerg nang ntype fnorm imom iyield                                                                                                                                                                                                                                                                                                  |
|           | nerg                              | The number of energy (momentum) bin boundaries (DE- FAULT: 0, i.e., produce only energy-integrated values).                                                                                                                                                                                                                        |
|           | nang                              | The absolute value, | nang | , provides the number of angle bin boundaries. For nang > 0 , cosine bins are specified; for nang < 0 , degree bins are specified (DEFAULT: 0, i.e., produce only angle-integrated energy spectra values).                                                                                            |
|           | ntype                             | The number of particle types to be tallied, including elastic scattering as a special case. If ntype = 0 , all allowed particle types are included in the tally, including elastic scattering and elastic recoil (DEFAULT: 0).                                                                                                     |
|           | fnorm                             | A normalization factor for the double-differential cross- section edit (DEFAULT: 1). For example, use fnorm = 1000 . 0 to convert output to millibarns.                                                                                                                                                                            |
|           | imom                              | If nonzero, treat the input energy bins as momentum bins (MeV/ c ) rather than energy bins (MeV). The output double- differential cross-section edits will be per unit momentum (DEFAULT: 0).                                                                                                                                      |
|           | iyield                            | If nonzero, the output will be differential multiplicities or yields rather than differential cross sections. Multiplicities for nonelastic reactions are defined with respect to the nonelastic cross section; for elastic scattering, the differen- tial multiplicity is with respect to the elastic cross section (DEFAULT: 0). |

## Card 5:

Energy (momentum) bin boundaries (present if nerg &gt; 0 ).

Four modes of input are allowed. The values are energy in MeV or, if
imom = 0 , momentum in MeV/c:

glyph[negationslash]

1. All bins E i for i = 1 , . . . , nerg may be specified in increasing order.

## Card 6:

## Card 7:

## /warning\_sign Caution

The particle-type identifiers given in Table D.22 are not exactly the
same as defined by the general MCNP6 numbering scheme for particle type
[Table 4.3]. Users therefore should choose values for ntype carefully.

2. If only one energy (momentum) value E 1 is entered, then E i = iE 1 for i = 2 , . . . , nerg .
3. If N &lt; nerg bins E i for i = 1 , . . . , N are entered in increasing order, then E i = E i -1 +( E N -E N -1 ) for i = N +1 , . . . , nerg .
4. If only two values, V 1 and V 2 , are entered, with V 1 &lt; 0 and V 2 &gt; 0 , then E nerg = V 2 and log 10 ( E i -1 /E ) = V 1 for i = 1 , . . . , nerg -1 (equal-lethargy spacing).

Angle bin boundaries (present if nang = 0 ).

For nang &gt; 0 , cosine bins are entered by one of the following options:

glyph[negationslash]

1. Cosine bins µ i for i = 1 , . . . , nang are entered in increasing order; µ nang is always set to 1.
2. If a null record ' / ' is present, nang equally spaced cosine bins -1 &lt; µ i ≤ 1 are defined with µ nang = 1 .
3. If only one value is entered, then the entered value is µ 1 and µ nang = 1 ; the remaining cosine boundaries are interpolated uniformly.
4. If two (or more) values are entered, then the first entered value is µ 1 , the second is µ nang -1 , and µ nang = 1 ; the remaining cosine boundaries are interpolated uniformly.

For nang &lt; 0 , the degree bins are entered by one of the following
options:

1. Degree bins ϕ i for i = 1 , . . . , nang are entered in decreasing order; ϕ nang is always set to 0.
2. If a null record ' / ' is present, nang equally spaced degree bins 180 &lt; ϕ i ≤ 0 are defined with ϕ nang = 0 .
3. If only one value is entered, then the entered value is ϕ 1 and ϕ nang = 0 ; the remaining cosine boundaries are interpolated uniformly.
4. If two (or more) values are entered, then the first entered value is ϕ 1 , the second is ϕ nang -1 , and ϕ nang = 0 ; the remaining cosine boundaries are interpolated uniformly.

Particle types to be tallied for this case (present if ntype &gt; 0 ).

Entries are a set of flags, k i , for i = 1 , . . . , ntype (see Table
D.22). These flags identify the particle types to be included in a
single cross-section edit case. Negative entries ( k i &lt; 0 ) indicate
tallies related to elastic scattering. Values of k i &gt; 0 designate the
tallying of production of the indicated particles type by nonelastic
processes.

In the absence of any nonelastic reaction models, only the elastic cases
will produce a meaningful tally.

When the default ( ntype = 0 ) is taken, all 26 edit types are allowed.
Only brief output is produced when no secondaries of a given type occur.
The ordering by particle type in the output is the following: proton,
neutron, π + , π 0 , π -, K + , K 0 , antiK 0 , K -, anti-proton, anti-
neutron, deuteron, triton, helion, alpha, photon, electron, positron, µ
-, µ + , ν e , antiν e , ν m , antiν m , elastic scattered projectile,
and elastic recoil nucleus.

Table D.22: Particle-type Designators for the ntype k i Flag

| Flag k i                         | Particle                                                                                                                                                                                                                                                                                         | Flag k i                            | Particle                                                                                                                                                                                                                                                                                                                                        |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 2 3 4 5 6 7 8 9 10 11 12 - 1 2 | neutron (n) photon ( γ ) electron (e - ) positron (e + ) proton (p + ) positive pion ( π + ) negative pion ( π - ) neutral pion ( π 0 ) negative muon ( µ - ) positive muon ( µ + ) electron neutrino ( ν e ) anti electron neutrino ( ν e ) elastic scattered projectile elastic recoil nucleus | 13 14 15 16 17 18 19 20 21 22 23 24 | muon neutrino ( ν m ) anti muon neutrino ( ν m ) positive kaon (K + ) negative kaon (K - ) kaon, short (K 0 S ) (previously K 0 ) kaon, long (K 0 L ) (previously anti- K 0 ) anti proton (p) anti proton (p) deuteron (d) (previously 2 H) triton (t) (previously 3 H) helion ( 3 He) (previously 3 He) alpha particle ( α ) (previously 4 He) |

-

The allowed k i flag values (needed on card 7) are given in Table D.22
(now with particle descriptions consistent with Table 4.3 though with
some symbols given previously also indicated).