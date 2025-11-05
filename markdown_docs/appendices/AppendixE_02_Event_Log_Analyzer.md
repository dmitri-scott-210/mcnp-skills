---
title: "Appendix E.2 - Event Log Analyzer (ela.pl)"
chapter: "E.2"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.2_Event_Log_Analyzer_(ela.pl).pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

## E.2 Event Log Analyzer ( ela.pl )

The Event Log Analyzer (ELA) is a Perl utility with a Tk interface used
as a research tool to interrogate the event log produced by the MCNP
code to understand event-by-event evolution of the random walk
undertaken by a computational particle (i.e., a history). This utility
has also been used as part of the MCNP 'Advanced Variance Reduction'
class. MCNP practitioners are welcome to use this utility as is;
however, only limited support is available for it.

This utility was originally designed to work with the MCNP code, version
5.1.50. This is because a refined event log was added with version
5.1.50. Generating an event log with the MCNP code is usually performed
by using the DBCN card with entries such as those shown in Listing E.1.

```
dbcn 2j 1 5 10000 $ Print event log for histories 1--5, limit to 10k lines
```

Listing E.1: example\_event\_log.mcnp.inp.txt

Further documentation can be found in [352, 353].

Note that [352] is the latest released documentation on ELA, but it is
not current with all features. Around 2011, 'Distance Analysis' was
added and the 'Required Data' tab was eliminated. Also note that
checking track weight against weight window values only works for cell-
based weight windows.

## E.2.1 User Interface and Example

The ELA is primarily a GUI application, with its original documentation
provided in [352]. However, a complete example follows based on Listing
E.2.

```
1 Reduced-radius Godiva sphere showing an event log 2 c 3 c CELL CARDS 4 10 100 -18.74 -1 imp:n=1 5 20 0 1 imp:n=0 6 7 c SURFACE CARDS 8 1 so 8.5 9 10 c DATA CARDS 11 sdef erg=d1 12 sp1 -3 0.965 2.29 13 m100 92235.00c -.9473 14 92238.00c -.0527 15 dbcn 2j 1 5 10000 $ Print event log for histories 1--5, limit to 10k lines 16 nps 100 17 print 18 rand gen=2 seed=12345
```

Listing E.2: example\_event\_log.mcnp.inp.txt

The example events counted are shown in Fig. E.1. The event-tree,
surface-analysis, and distance-analysis settings shown in Figs. E.2,
E.3, and E.4, respectively, produce the example event tree, surface
analysis, and distance analysis shown in Figs. E.5, E.6, and E.7,
respectively.

Figure E.1: ELA Event Counter

<!-- image -->

<!-- image -->

- (a) View-enabled Events and Color Settings
- (b) Enabled Subevent Settings
- (c) Other Event-tree Options

<!-- image -->

<!-- image -->

Figure E.2: ELA Event-tree Settings

Figure E.3: ELA Surface-analysis Settings

<!-- image -->

Figure E.4: ELA Distance-analysis Settings

<!-- image -->

Figure E.5: ELA Event Tree

<!-- image -->

Figure E.6: ELA Surface-analysis Results

<!-- image -->

Figure E.7: ELA Distance-analysis Results

<!-- image -->

## E.2.2 Change Log

This section describes the evolution of the Event Log Analyzer.

## Version 1.0, 10 September 2007

- Original release.

## Version 1.1, 3 March 2011

- Added code so that ELA knows the directory in which it is installed. This directory information is now used in opening its resource files.
- Added command-line interface operation. Try one of the following to learn more: perl ela.pl --help or ./ela.pl -h .

Note that testing with some versions of Perl and Perl/Tk experience
warning messages at start up and core dumps when terminating GUI
operations.

Note also that use with Cygwin exhibits periodic misbehavior; with some
installs and systems the menu bar is hidden. An alternative free Perl
download for Windows is the Active Perl or Active State Perl.

## Version 1.2, 19 August 2013

- Updated #! path to be generic.

## Version 1.3, 18 January 2022

- Reformatted README.md file to Markdown and extracted content to MCNP manual. Revised wording to improve clarity and embed an example.