Revision Notes
==============

May 26, 2021
------------

Experimental eigenvalues and uncertainties were compared against the 2015 revision of the ICSBEP.  The following changes were made:
* heu-met-inter-006 Case 2 - k-eigenvalue was changed from 0.9997 (from Revision 3) to 1.0001 (from Revision 4). The actual model in the test suite was from the Revision 4 changes (see Surface 11 and Table 32).
* ieu-met-fast-007 Case 4 - k-eigenvalue corrected from 1.0030 to 1.0300.
* leu-comp-therm-008 Case 1, 2, 5, 7, 8, 11 - The uncertainty was corrected from 0.0016 to 0.0012.
* mix-comp-therm-002 Case 30, 31, 32, 33, 34, 35 - The actual input file is the detailed model and not the simplified model.  The eigenvalues and uncertainty were changed to the detailed model values.
* u233-sol-therm-001 Case 2-5 : k-eigenvalues corrected from 1.0000 to 1.0005, 1.0006, 0.9998, and 0.9999 respectively.
* u233-sol-therm-008 : k-eigenvalue corrected from 1.0000 to 1.0006.

And the following discrepancies were noted but not corrected:
* heu-met-fast-004 Case 1 : ICSBEP-2015 provides no uncertainty, so a value of 0.001 was added in the original problem set.
* ieu-met-fast-001 Case 1-4 : Final benchmark model uncertainties are also not provided, and were set slightly higher than the experimental values in the original problem set.
* pu-met-fast-001 : The model is the simplified Revision 2 model.  Revision 3 updated the outer radius and lowered the uncertainty of the k-eigenvalue.
* For heu-met-fast-018, 019, 020, 021, 022, ieu-met-fast-003, 004, 005, 006, and pu-met-fast-022, 023, 024, 025, 026, the simplified model was used and compared against the detailed model benchmark eigenvalue.  For these problems, the additional uncertainty from the simplification process is not directly calculated, but the authors note that it is not expected to exceed 0.0002.  As this is relatively negligible, it is ignored, and comparisons for these problems can be noted to be slightly conservative.

Support was added for ENDF/B-VIII, and support removed from ENDF/B-VI.
Conversion was automated, in which ENDF/B-VII.1 ZAIDs were converted to ENDF/B-VIII ZAIDs.
6000.80c was converted to 98.93% 6012.00c and 1.07% 6013.00c.
The original specifications were not checked to determine if additional nuclides needed to be added, such as 74180.00c in natural tungsten.
