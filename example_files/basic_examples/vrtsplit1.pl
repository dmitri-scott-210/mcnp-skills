#!/usr/bin/perl
#
# vrtsplit1.pl
#  
#    Perl script to calculate cell IMP values for MCNP using
#    a pervious a previous outp file.  Values calculated to
#    equalize tracks entering a group of cells.  The cells are
#    assumed to be more or less in a direct line between the
#    source cell and the tally region.
#
#    By:  Roger L. Martz
#         February 11, 2009
#
# Save total number of arguments from the command line.
#
  $args = $#ARGV;
  if ($#ARGV > -1) {
    $infile =  shift @ARGV;
    print "\n Running $0\n";
    print "\n Finding new splitting ratios based on ";
    print "Input File:  $infile \n\n";
#
    open (IN1, $infile) or die "Can't open file $infile\n";
#
    my $pt60  = "print table 60";
    my $pt126 = "print table 126";
    my $stop  = "total";
    my $xx;
#
#   See if the print tables are present before proceeding.
#
    my $nPT60  = 0;
    my $nPT126 = 0;
    while ($xx = <IN1>) {
      if ( !eof ) {
        if ($xx =~ /$pt60/) {
          $nPT60++;
        }
        if ($xx =~ /$pt126/) {
          $nPT126++;
        }
      }
    }
    close IN1;
#
#   Open second file.
#
    if ($args > 0) {
      $secfile =  shift @ARGV;
      print " Splitting ratios for cells in file: $secfile \n\n";
      open (IN2, $secfile) or die "Can't open file $secfile\n";
      while ($xx = <IN2>) {
        @words = split " ", $xx;
        for ($i=0; $i <= $#words; $i++)  {
          $uCells = push @useCells, $words[$i];
        }
      }
      close IN2;
    }
#
#   Continue if the print tables are in the file.
#
    if (($nPT60 > 0) && ($nPT126 > 0)) {
      open (IN1, $infile) or die "Can't open file $infile\n";
#
#     Search for print table 60
# 
      until ( ($xx=<IN1>) =~ /$pt60/) {   
#        print "$xx";
      }
#
#     Skip the header info for table 60
#
      $xx=<IN1>; 
      $xx=<IN1>; 
      $xx=<IN1>; 
      $xx=<IN1>; 
#
#     Grab the cell importances.
#
      my $i = 0;
      until ( ($xx=<IN1>) =~ /$stop/) {   
#
        @words = split " ", $xx;
        if (($#words > 4) && ($words[$#words] > 0.0)) {
          $imps{$words[1]} = $words[$#words];
	  $cells[$i] = $words[1];
	  $i++;
        }
      }
#
#     Search for print table 126
# 
      until ( ($xx=<IN1>) =~ /$pt126/) {   
#      print "$xx";
      }
      $xx=<IN1>; 
      $xx=<IN1>; 
      $xx=<IN1>; 
      $xx=<IN1>;
      $xx=<IN1>;

#     Grab the tracks entering.
#
      until ( ($xx=<IN1>) =~ /$stop/) {   
#
        @words = split " ", $xx;
        if (($#words > 4) && ($words[2] > 0.0)) {
          $tracks{$words[1]} = $words[2];
        }
      }
      close IN1;
#
#     Calculate the new importances.
#   
      my $iRatio = 0.;
      my $tRatio = 0.;
      if ($args < 1) {
        for ($i = 0; $i <= $#cells; $i++)  {
          $useCells[$i] = $cells[$i];
        }
      }
#
      $newI{$useCells[0]} = 1.0;
      $newM{$useCells[0]} = 1.0;
      for ($i = 1; $i <= $#useCells; $i++)  {
        if (($imps{$useCells[$i-1]} > 0.0) && ($tracks{$useCells[$i]} > 0.0)) {
          $iRatio = $imps{$useCells[$i]} / $imps{$useCells[$i-1]};
          $tRatio = $tracks{$useCells[$i-1]} / $tracks{$useCells[$i]};
          $newI{$useCells[$i]} = $newI{$useCells[$i-1]} * $iRatio * $tRatio;
          if ($newI{$useCells[$i-1]} < 1) {
            $newI{$useCells[$i-1]} = 1;
          }
          $newM{$useCells[$i]} = $newI{$useCells[$i]} / $newI{$useCells[$i-1]};    
        }
      } 
#
#     Print table.
#    
      print "  Cell   New Importance         Ratio\n";
      for ($i=0; $i <= $#useCells; $i++) {
        printf "%6d  %15.2f  %12.2f\n", $useCells[$i], $newI{$useCells[$i]}, $newM{$useCells[$i]};
      } 
#
#     Output split-ratio file.
#
      $outfile = "splitratio.inp";
      print "\nCreating splitting ratio file:  $outfile \n";
      open (FOUT, ">$outfile") or die "Can't open file $outfile\n";
      printf FOUT "     %7.2f ", $newM{$useCells[0]};
      my $j=1;
      for ($i=1; $i <= $#useCells; $i++) {
        if ($j == 0) {      
          printf FOUT "     %7.2fm", $newM{$useCells[$i]};
        }
        elsif ($j == 4)  {
          $j = -1;
          printf FOUT " %7.2fm\n", $newM{$useCells[$i]};	
        }
        else  {
          printf FOUT " %7.2fm", $newM{$useCells[$i]};
        } 
        $j++;
      }
      close FOUT;  
#
#     Output importance file.
#
      $outfile = "importance.inp";
      print "\nCreating splitting ratio file:  $outfile \n\n";
      open (FOUT, ">$outfile") or die "Can't open file $outfile\n";
      for ($i=0; $i <= $#useCells; $i++) {
        printf FOUT " %f\n", $newI{$useCells[$i]};
      }
      close FOUT; 
#
    }        # -- end if for processing with print tables
    else {
      if ($nPT60 < 1) {
        print "\n ***** No Print Table 60 in input file.\n\n";
      }
      if ($nPT126 < 1) {
        print "\n ***** No Print Table 126 in input file.\n\n";
      }
    }
  }
  else {
#
      print <<end_of_text;

      ******************************************************************
      This script (vrtsplit1.pl) adjusts cell importances to 
      obtain a constant track distribution and requires 1 or 2 
      input files on the command line.

      The first file to appear on the command line must be an 
      MCNP output file (outp) with Print Tables 60 & 126.

      The second file is optional.  This file contains cell numbers,
      separated by white space, for which the ratios are calculated.
      Cell numbers may be all on one line, one per line, or a mixture.

      If the second file is not present, the script will calculate cell
      importances and ratios for all cells present in Print Table 60
      that have non-zero tracks and non-zero importances.  

      If the second file is present, the cell importances are calculated
      for only those cells present in the file for all that have non-
      zero tracks and non-zero importances.  Ratios are calculated
      for cell pairs starting from the first pair of cell numbers.
      The first two cell numbers form the first pair.  The second and
      third cell numbers form the second pair, etc.

      Cell importances appear in the default or specified order in
      the file: importance.inp

      Cell importance ratios appear in m-notation in the default 
      or specified order in the file: splitratio.inp
      
      ******************************************************************

end_of_text
#
  }
