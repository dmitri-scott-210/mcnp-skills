---
title: "Chapter 6.5 - Normalization of Energy-dependent Tally Plots"
chapter: "6.5"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/6_MCNP_Geometry_and_Tally_Plotting/6.5_Normalization_of_Energy-dependent_Tally_Plots.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

Figure 6.17: View along polar axis at origin showing azimuthal planes at KMESH = 72, 306, and 360 degrees. The azimuthal vector, VEC , is to the right (360 degree plane)

<!-- image -->

- (a) If the mesh has multiple particle types, energies, etc, the indexes can be stepped through by clicking the PAR and N buttons before cycling the COLOR button. Ordering is described in the description of the wwn button in in §6.2.3.3.
4. Click the XY button which draws the plot colored by the values of the weight window mesh.
5. Click 10 in the Zoom bar twice.

The equivalent command input to the PLOT&gt; prompt is:

## la 0 1 wwn1:p color on la 0 0 mesh 3 ba 1 0 0 0 1 0 ex 10

This view is along the polar axis, which is defined by the AXS parameter
on the MESH card, and shows the segmentation of the spherical mesh from
the azimuthal angles (longitude) that are defined on the KMESH parameter
of the MESH card.

The view in Figure 6.18 can be achieved by following the same steps
listed above, but clicking the YZ button instead of the XY button.

This view orients the polar reference vector towards the top of the
geometry and shows essentially a slice of the cone that is defined by
the polar angles (latitude). Clicking in the lower-left box and typing '
PX 1 ', ' PX 2 ', ' PX 3 ' and so on will demonstrate this conical
section (see Figure 6.19). This shows the 3 bins that are defined on the
JMESH parameter of the MESH card.

07/14/2214 :34:10

Figure 6.18: Plot view orthogonal to polar axis showing polar bins JMESH = 36 and 126 degrees. The polar axis (0 degrees) is through the center of the mesh towards the top of the plot.

<!-- image -->

07/14/2214 :38 : 25

Figure 6.19: Plot view achieved with the command PX=2 . The polar axis is towards the top of the plot. The azimuthal axis is coming out of the screen. This view shows the smooth conical sections of the polar angles and the other vertical vertical lines not through the center of the mesh are the azimuthal angles intersecting with the slice (left-hand vertical is θ = 306 ◦ , right-hand vertical is ϕ = 72 ◦ .

<!-- image -->

## 6.5 Normalization of Energy-dependent Tally Plots

This section discusses two methods of normalizing an energy-dependent
tally for plotting:

- dividing by the width of each energy bin, and
- dividing by the logarithmic width of each energy bin (i.e., dividing by the lethargy width).

This section also discusses how to obtain plots that provide an easy
visualization for the tally results by the area under the curve.
Examples of both normalizations are provided for a logarithmic energy
abscissa.

## 6.5.1 MCNP6 Tally Values and Energy-normalized Tallies

Assume that an MCNP6 energy-dependent tally density such as flux or
reaction rate has a form of f ( E ) per unit energy. An MCNP6 tally
result T i in energy bin i from f ( E ) is

<!-- formula-not-decoded -->

where the energy bin limits are E l i to E u i . The T i s tend to be
small for small energy bins and large for larger energy bins. Thus,
there is no explicit information about the density f ( E ) in the T i s
unless all energy bins have the same constant width, in which case the
correct histogram shape of f ( E ) is obtained from the T i s. The
average value of f ( E ) over the energy range ∆ E i between E l i and E
u i is

<!-- formula-not-decoded -->

The f i ( E ) s are the bin-wise histogram representations of the tally
of f ( E ) because they are the average values of f ( E ) in each energy
bin. Note that f i ( E ) is a constant between E l and E u .

This E u -E l normalizing of T i , the default for a 2-D MCNP6 energy-
dependent tally plot, is generally agreed to be the proper way to
display the f i ( E ) s when the abscissa E of a 2-D plot is linear.
When a LINLIN (linear abscissa and linear ordinate) plot of f i ( E ) s
is made with the ordinate starting at zero, the visual area under each
histogram represents T i . This type of visually correct area plot will
be termed a Visually Accurate Area (VAA) plot. A VAA plot provides
correct visual information about the tally by the area under the
histogram.

The average energy E i for each f i ( E ) bin is

<!-- formula-not-decoded -->

where the f i ( E ) histogram approximation to f ( E ) cancels out. E i
is used as the average energy for plotting the statistical error bars
for tally bin i .

## 6.5.2 Definition of Neutron Lethargy

The lethargy, U , of a neutron with energy E is defined to be

<!-- formula-not-decoded -->

where E 0 is the upper neutron energy for the problem. On the average,
neutrons lose a fixed fraction of their energy in each elastic collision
with a specific isotope above thermal energies. The lethargy U is used
in nuclear reactor analysis to assess the average logarithmic energy
loss of these elastically scattered neutrons.

A neutron with energy E 0 has zero lethargy. As the neutron loses
energy, its lethargy increases (hence the name 'lethargy,' because the
neutron becomes more lethargic) and is always positive because no energy
is greater than E 0 . A neutron with zero energy has infinite lethargy.

For eigenvalue problems, MCNP6 calculates the Energy of the Average
neutron Lethargy causing Fission (EALF):

where Φ( E ) is the neutron flux and Σ f ( E ) is the fission cross
section. MCNP6 can plot energy-dependent tallies versus a logarithmic
energy scale using lethargy for tally bin normalization.

<!-- formula-not-decoded -->

## 6.5.3 Lethargy-normalized Tallies for a Logarithmic Energy Abscissa

When the abscissa E is logarithmic, the normalization of the tally
scores, T i , involves the differences in the natural logs ( ln ) of the
energy instead of the differences in the energies. It is useful to
relate the differences in the logs of the bin energies to the often used
neutron lethargy U :

<!-- formula-not-decoded -->

where U l i is the lethargy at E l i and U u i is the lethargy at E u i
(the ln( E 0 ) terms cancel: see Eq. (6.6)).

The tally T i can be converted to an average bin i lethargy-normalized
value F i ( U ) by

<!-- formula-not-decoded -->

The F i ( U ) s are the histogram approximation to F ( U ) per unit
lethargy. MCNP6 plots the F i ( U ) s instead of the f i ( E ) s for a
ln( E ) abscissa when the LETHARGY plot command is used. The F i ( U ) s
are not plotted when the energy abscissa is linear. Only the f i ( E ) s
and T i s can be plotted for a linear E abscissa. A LOGLIN (log abscissa
and linear ordinate) plot of the F i ( U ) s is a VAA plot because the
ln( E ) abscissa is linear in U and the area under the histogram is
visually correct.

## 6.5.4 Relation of Tally Lethargy Normalizing to Tally Energy Normalizing

To determine the functional form of F ( U ) in terms of f ( E ) , equate
the U and E density function areas to produce

<!-- formula-not-decoded -->

The negative sign is required because E decreases as U increases.
Integrating the left hand side of Eq. (6.10) from U u i to U l i is
equal to T i , as is the integral of the right hand side from E u i to E
l i .

The differential d U can be written in terms of energy E from Eq. (6.6)
as

<!-- formula-not-decoded -->

Substituting Eq. (6.11) for d U into Eq. (6.10) gives

<!-- formula-not-decoded -->

Equation (6.12) shows that F ( U ) can be thought of as the energy E
multiplied by f ( E ) . Thus, besides producing VAA LOGLIN plots,
lethargy-normalized plots have the additional virtue of flattening the 1
/E neutron flux shape that often occurs in neutron spectra. For an f ( E
) that has a 1 /E shape everywhere, F i ( U ) is a constant for all i
(as opposed to the widely varying f i ( E ) s), which produces a VAA
plot for the 1 /E shape. Lethargy-normalized plots remove many of the
decades of f i ( E ) change, represent the 1 /E portions of the spectrum
as a constant, and make understanding and comparing the F i ( U )
results easier.

## 6.5.5 Average Energy for a Lethargy-normalized Tally

The lethargy-averaged energy 〈 E i 〉 for energy bin i is defined as

<!-- formula-not-decoded -->

For the histogram approximation of F ( U ) by F i ( U ) , the F i ( U )
s cancel, and changing variables using Eq. (6.11) gives

In the limit as E u i -E l i becomes small, 〈 E i 〉 ≈ E i in Eq. (6.5)
as expected. This average 〈 E i 〉 is considered to be the centroid
energy for a lethargy-normalized bin and is used in MCNP6 to plot
statistical error bars, BAR plots, and PLINEAR plots, as well as
printing the plotted points using the PRINTPTS command.

<!-- formula-not-decoded -->

## 6.5.6 MCNP6 LETHARGY Command for Lethargy Normalization

Lethargy-normalized plots of energy-dependent tallies with a log energy
abscissa are made with the LETHARGY plotting command. This command
cannot be used for cross-section plots. For this command to apply, FREE
E must be active, LOGLIN or LOGLOG axes must be used, and the NONORM
command must not be invoked. The LETHARGY command cannot be used after a
COPLOT command and can be disabled to return to energy-bin-width tally
normalization for a log energy abscissa by using RESET LETHARGY .
Switching from a logarithmic energy to a linear energy abscissa with
LETHARGY in use will automatically change a plot of the F i ( U ) s to
the f i ( E ) s. Switching back to the log energy abscissa will again
plot the F i ( U ) s.

If an E 0 were specified for a log-abscissa plot, a linear lethargy
abscissa could be specified starting at the right with a value of zero
at E 0 and linearly increasing to the left in steps of about 2.3 per
energy decade decrease. MCNP6 does not label the abscissa as lethargy
because of the difficult energy interpretation. The logarithmic energy
decades are plotted instead to allow easier interpretation of the areas
under the lethargy-normalized histogram. For this reason, there is
neither a need nor a provision to specify E 0 .

1

1

## 6.5.7 Requirements for Producing a Visually Accurate Area (VAA) Tally Plot

Consider the characteristics of a function of one variable, such as an
MCNP6 2-D tally histogram plot. One important quantity for this
histogram is the integral over the tally range, which is the total MCNP6
tally. Another important characteristic is the shape of this histogram
that provides information about where the largest regions of the tally
have occurred. The area of a tally range under the plotted curve is a
measure of the contribution of each range to the total.

The area under this curve is best visualized with both the abscissa and
the ordinate having a linear scale. The ordinate usually has a lower
value of zero to represent correctly the curve area. A LINLIN plot of
the f i ( E ) s fits these criteria and therefore is a VAA plot. Often
linear scales do not allow complete display of a tally, so logarithmic
scales must be used. A logarithmic axis scale typically changes by
decades. Each decade change on the abscissa changes a ∆ E for a
specified length along the abscissa by a decade. The area under the
LOGLIN f i ( E ) curve is proportional to ∆ E , which is not reflected
in the visual area representation on the log abscissa plot. A
logarithmic ordinate does not visually display the correct tally
contribution under the curve because this area in the plot is
proportional to the number of ordinate decades. When both axes are
logarithmic, the visual interpretation in the plot of the area under the
curve is further obscured.

The lethargy variable U is linear in the logarithm of the energy as
defined in Eq. (6.6). U values for decreasing energy E values of E 0 , E
0 / 10 , and E 0 / 100 are 0, 2.3, and 4.6. Therefore, a LOGLIN plot of
the F i ( U ) s instead of the f i ( E ) s satisfies the VAA plot linear
scale criterion for visually examining the area under a curve. The area
under each histogram F i ( U ) is F i ( U ) · ( U l i -U u i ) , which
is exactly the bin i tally T i as defined in Eq. (6.9). Similarly, the
area under all the F i ( U ) s is the sum of the T i s, which is the
total MCNP6 tally. A LOGLIN plot of the F i ( U ) s is a VAA plot; a
LOGLIN plot of the f i ( E ) s is not a VAA plot.

## 6.5.7.1 Tally Fluctuation Chart History Score Plotting

Two-dimensional plots of a tally F ( x ) = xf ( x ) are made by dividing
the tally bin value by the width of the tally bin x i +1 -x i . VAA
plots of F ( x ) are plots whose visual area under the curve is an
accurate representation of the tally in each of the tally bins; i.e.,
the visual area represents F ( x )( x i +1 -x i ) for all abscissa
values. A VAA plot will be produced for a 'linlin0' (linear abscissa
scale, linear ordinate scale starting at 0) F ( x ) plot; i.e., the area
of F ( x ) from x i to x i +1 correctly represents the bin tally value
visually for all x when both the abscissa and ordinate scales are linear
and the smallest ordinate value is zero. A linlin0 plot can be achieved
with the following command:

LINLIN XLIMS 0 [max]

In a similar manner to the linlin0 VAA plot described above, a VAA plot
of F ( x ) on a 'loglin0' (log abscissa scale, linear ordinate scale
starting at 0) plot is produced if the tally bin value is divided by the
difference in the logarithms of the abscissa values. The loglin0 plot
can be achieved with:

LOGLIN XLIMS 0 [max]

If y = ln( x ) , then G ( y ) is defined to be

<!-- formula-not-decoded -->

A loglin0 plot of G ( y ) is a VAA plot of F ( x ) because y is linear
on a log abscissa and G ( y )( y i +1 -y i ) is the area of the tally
bin.

The relation between G ( y ) and F ( x ) is where

Therefore,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This y normalizing of the tally bin value to make a loglin G ( y ) plot
is equivalent to making a loglin xF ( x ) plot. Lethargy plotting of an
energy-dependent tally F ( E ) , with E representing energy, is the
equivalent of plotting G (ln( E )) = EF ( E ) on a loglin0 scale to
produce a VAA plot for the tally F ( E ) . For more information on
normalization of energy dependent tallies, see Section 6.5.

These normalizing statements can be generalized to any function h ( x )
. The VAA interpretation of a 2-D plot therefore depends on the abscissa
axis scale. A linlin0 plot of h ( x ) is a VAA h ( x ) plot and a
loglin0 h ( x ) plot is a VAA plot for h ( x ) /x .

Two-dimensional plots from a RUNTPE (but not a MCTAL ) file of the
empirical history score probability density function f ( x ) moments can
be made using the Tally Fluctuation Chart (TFC) tally plot commands
[§6.3.3.7]. In this case, the tally F ( x ) = xf ( x ) . From the
discussion above, a loglin0 F ( x ) plot can be interpreted as a VAA
plot for f ( x ) ; i.e., the area under the curve on a loglin0 scale
represents where the f ( x ) sampling has occurred. A linlin0 F ( x )
plot is a VAA plot for the tally F ( x ) .

Based on these observations, the following statements can be made about
TFC commands to create f ( x ) moment plots for the TFC bin of a tally
(without the NONORM option):

- f ( x ) TFC bin plots are VAA plots when
1. TFC P [ f ( x ) ] is on a linlin0 scale; and
2. TFC 1 [ xf ( x ) ] is on a loglin0 scale.
- xf ( x ) = F ( x ) TFC bin tally plots are VAA plots when
1. TFC 1 [ xf ( x ) = F ( x ) ] is on a linlin0 scale; and
2. TFC 2 [ x 2 f ( x ) = xF ( x ) ] is on a loglin0 scale.
- x n f ( x ) TFC bin tally moment plots are VAA plots when
1. TFC n [ x n f ( x ) ] is on a linlin0 scale; and
2. TFC n [ x n +1 f ( x ) ] is on a loglin0 scale.

The VAA contributions to the n th f ( x ) moment can be viewed with an x
n f ( x ) linlin0 plot or an x n +1 f ( x ) loglin0 plot. The empirical
f ( x ) slope result can be checked by viewing a TFC n plot. If the
high-score f ( x ) tail for a long-tailed distribution (not a finite
distribution) is proportional to 1 /x n , then the TFC n plot will be a
statistical constant at the high x scores. A large score f ( x ) slope
of at least n exists if the high-score TFC n [ x n f ( x ) ] values are
decreasing. VAA f ( x ) moment plots can be a useful tool in studying
the detailed impact of variance reduction techniques on f ( x ) (not the
history sampling time as function of x ) and the efficiency of a
calculation.

## 6.5.8 Comparisons of Energy and Lethargy Tally Normalizations for a Log in Energy Abscissa

Energy-normalized and lethargy-normalized log energy abscissa tally
plots for two analytic and two critical uranium assembly problems are
discussed to show which are VAA plots. The two analytic f ( E ) examples
will be accurate to three significant figures in the text.

loglin plot of f(e)=0.1 versus e for a uniform 0.0001 to 10 MeV source

Figure 6.20: A LOGLIN plot of energy-normed f i ( E ) versus E for a uniformly sampled energy source between 0.0001 and 10 MeV. The expected value of all f i ( E ) s is 0.1.

<!-- image -->

## 6.5.8.1 Example 1: A Constant f ( E ) = 0 . 100 from 0.0001-10 MeV

The first example is the tally of a uniform energy source between 0.0001
and 10 MeV. The expected value of all f i ( E ) s is 0.100. Figure 6.20
shows a plot of the five energy-normalized f i ( E ) s, each with an
energy bin width of a decade. The tally T i in the energy bin from 1 to
10 MeV is 0 . 1(10 -1) = 0 . 9 . The next lowest energy bin tally is 0 .
1(1 -0 . 1) = 0 . 09 . The tally bin T i s are decreasing by a decade
per decade decrease in energy, but the f i ( E ) s are a statistically
constant 0.1. Visually interpreting this LOGLIN plot of the f i ( E ) s
by the area under the curve may not be useful because the energies are
changing by decades along the logarithmic energy abscissa.

Figure 6.21 shows a LOGLIN lethargy-normalized plot of the corresponding
five F i ( U ) s. The ' f ( u ) = e f ( e ) bin normed' text on the
right hand side of the plot is a reminder that this is a lethargy-
normalized plot. The shapes of the f i ( E ) s in Fig. 6.20 and the F i
( U ) s in Fig. 6.21 are completely different. F i ( U ) for the 1 to 10
MeV tally bin is 0 . 9 / ln(10 / 1) = 0 . 391 . The area in the plot of
this bin is 0 . 391 ln(10 / 1) = 0 . 900 , which is the correct T i for
this bin. The tally bin area from 0.1 to 1 MeV is 0 . 391 ln(1 / 0 . 1)
= 0 . 0900 . The visual areas of each of the tally bins represent the
tally for that bin because of the linear lethargy abscissa obtained by
the lethargy normalization.

The LOGLIN lethargy-normalized plot in Fig. 6.21 clearly displays the
relative contribution of each of the five tally bins by the area under
the histogram.

Figure 6.22 shows the same plot as in Fig. 6.21, except the ordinate is
now logarithmic. The five F i ( U ) s are the same in both plots, but
the visual area interpretation in Fig. 6.22 is misleading because the
ordinate scale is logarithmic. Nevertheless, Fig. 6.22 is useful for
assessing the behavior of the F i ( U ) s that are small and cannot be
seen in Fig. 6.21 with the linear ordinate.

loglin plot of f(u)=e*f(e)=e*0.1 vs e

Figure 6.21: A LOGLIN plot of lethargy-normed energy-normed F i ( E ) versus E for a uniformly sampled energy source between 0.0001 and 10 MeV. The area F i ( E · ∆ U i ) of each tally bin is the tally value.

<!-- image -->

loglog plot of f(u)=e*f(e)=e*0.1 vs

Figure 6.22: A LOGLOG plot of F i ( U ) versus E for a uniformly sampled energy source between 10 -4 and 10 MeV. The smaller tallies not visible at lower energies in Fig. 6.21 can be seen here.

<!-- image -->

loglin plot of f(e)=l/e versus

e

fora1/e0.000001to0.1mevsource

Figure 6.23: A LOGLIN plot of f i ( E ) versus 1 /E energy source between 10 -6 and 0.1 MeV. Equal lethargy bin spacing (0.23) in energy is used, so all bins contribute the same amount to the tally for the 1 /E source.

<!-- image -->

## 6.5.8.2 Example 2: f ( E ) = 0 . 087 /E from 10 -6 -0.1 MeV

For a second example, an equal-lethargy 50-bin tally was made of a 1 /E
energy source from 10 -6 to 0.1 MeV. The lethargy width of each tally
bin is ln ( 0 . 1 / 10 -6 ) / 50 = 0 . 23 . All T i s have an expected
value of 0 . 23 / ln ( 0 . 1 / 10 -6 ) = 0 . 02 for the equal lethargy
energy bins. Figures 6.23 and 6.24 show LOGLIN and LOGLOG plots of the f
i ( E ) s. Each tally bin has a relative error of 0.2%. The f i ( E ) s
have the expected 1 /E shape of the source. The histograms in both
figures decrease with increasing energy because the T i s are constant
and ∆ E i s are continuously increasing. Neither Fig. 6.23 nor 6.24 is a
VAA plot because neither shows a meaningful visual under-the-curve area
representation of the T i s for this tally.

The lethargy-normalized plot of the F i ( U ) s in Fig. 6.25 is a VAA
plot. The F i ( U ) s are a statistical constant ( 0 . 02 / 0 . 23 = 0 .
087 ) for f ( E ) = 1 /E , as predicted by Eq. 6.12. Figure 6.25 shows
visually that all equal lethargy widths contribute equally to the total
tally, which is correct for the 1 /E source. The integral under the
curve of Fig. 6.25 is 0 . 087 ln ( 0 . 1 / 10 -6 ) = 1 , which is the
source strength. Once again, the shapes of the f i ( E ) s in Figs. 6.23
and 6.24 and the F i ( U ) s in Fig. 6.25 are completely different.

## 6.5.8.3 Example 3: Neutron Fluxes and Fission Rate Spectra for Two Critical Uranium Systems

A third and more realistic example is a comparison of f i ( E ) and F i
( U ) plots for the neutron fluxes and fission rate spectra calculated
by MCNP6 for two critical uranium systems:

1. a water-reflected, water-moderated array of 18 × 20 2.35% low-enriched uranium (LEU) UO 2 aluminum clad fuel elements [334]; and

Figure 6.24: A LOGLOG plot of f i ( E ) versus 1 /E energy source between 10 -6 and 0.1 MeV. The 1 /E behavior of f i ( E ) is evident.

<!-- image -->

## loglin plot of f(u)=e*f(e)=constant vs e for a1/e0.000001to0.1mevsource

Figure 6.25: A LOGLIN plot of F i ( U ) = Ef ( E ) = E (0 . 087 /E ) = 0 . 087 versus 1 /E energy source between 10 -6 and 0.1 MeV. The integral of this plot is unity, which is the source strength.

<!-- image -->

Table 6.1: Percentage of Fission Rates by Incident Neutron Energy

| System   | Spectrum   |   E < 0 . 0625 eV |   0 . 0625 eV < E < 100 keV |   100 keV < E |
|----------|------------|-------------------|-----------------------------|---------------|
| LEU      | Thermal    |              91.4 |                         4.5 |           4.1 |
| HEU      | Fast       |               0   |                         5.4 |          94.6 |

2. the Godiva bare metal 93.7% highly enriched uranium (HEU) sphere [335].

The calculations were performed with pre-ENDF/B-VII uranium isotope
cross sections (from Los Alamos National Laboratory Group T-16) that are
identified by a '.69c.' All other isotopes in the LEU system used
ENDF/B-VI '.66c' cross sections with '.60t' S ( α, β ) data for light
water and polyethylene. The calculated k eff. for the LEU system is
0.9968 with an estimated standard deviation of 0.0003. The HEU system k
eff. is 0.9987 with a standard deviation of 0.0003. The calculated EALF
for the LEU and HEU systems is 1 . 0 × 10 -7 MeV and 0.82 MeV. The
calculated percentages of the incident neutrons causing fission by
energy range are listed in Table 6.1.

Figures 6.26 and 6.27 compare the energy-normalized and lethargy-
normalized plots of the neutron flux f i ( E ) s and F i ( U ) s for the
thermal LEU and fast HEU systems.

The areas under all curves are one. Only the HEU flux values with
relative errors less than 0.1 were plotted, which is the reason this
flux curve terminates abruptly. The plots of the f i ( E ) s in Fig.
6.26 do not convey the contributions of the f i ( E ) flux by the area
under the curve because both scales are logarithmic. The 1 /E flux
behavior for the LEU system is evident in the figure over much of the
ten decades of the f i ( E ) s. Fig. 6.26 is not a VAA plot.

Figure 6.27 is a VAA plot because the visual area under each curve
accurately represents the contributions to the total flux by energy
range because both axes are linear. The 1 /E f i ( E ) flux behavior is
characterized as the flat F i ( U ) range, as predicted by Eq. (6.12).

Figure 6.28 shows a LOGLOG plot of the fission rate f i ( E ) s versus E
for the thermal neutron spectrum LEU and fast high-energy spectrum HEU
systems. Each curve is divided by the total tally over all energies so
the area under each curve is unity. Figure 6.28 shows the thermal and
fast fission rate shapes, but does little to convey the fission rate
percentages shown in Table 6.1. Figure 6.28 is not a VAA plot.

Figure 6.29 shows a LOGLIN plot of the f i ( E ) s versus E for just the
LEU system. The area under this curve representation of the LEU system
also does not visually agree with the results in Table 6.1: there is no
curve area above 6 × 10 -7 MeV (0.6 eV). This conclusion about incorrect
visual areas is not surprising since the F ( U ) and f ( E ) shapes
differ so markedly for the first two simple examples. Figure 6.29 is not
a VAA plot.

Figure 6.30 shows a LOGLIN VAA plot of the fission rate F i ( U ) s
versus E for both systems. The area beneath both curves is one. Now the
fission rate percentages occurring in each energy range become clear and
visually match the results in Table 6.1. The LOGLIN lethargy-normalized
plot in Fig. 6.30 visually conveys much more information about the
fission rate characteristics as a function of energy than the plot of
the f i ( E ) s in Figs. 6.28 and 6.29.

Comparing the LEU f i ( E ) s in Fig. 6.29 with the LEU F i ( U ) s in
Fig. 6.30 shows that the f i ( E ) thermal fission rate peak in Fig.
6.29 is skewed toward the lower energies. This shift is caused by the
ever-increasing 1 / ∆ E i for decreasing energies. The visual area
representation of the LEU tally is correct for F i ( U ) in Fig. 6.30
and incorrect for f i ( E ) in Fig. 6.29.

Figure 6.31 shows a LOGLOG plot of the fission rate F i ( U ) s versus E
. Even though the visual area under this curve is misrepresented by the
log ordinate, the behavior of the smaller F i ( U ) values versus E
becomes clearer.

loglin plotof flux f（u)=e*f（e)vse

Figure 6.26: A LOGLOG plot of energy-normed neutron flux f i ( E ) versus E for the thermal LEU (larger curve) and fast HEU (smaller curve) systems. The area under curves is one.

<!-- image -->

## loglogplotofneutron flux f（e)vse

## for a thermal LEU and fast HEU system

Figure 6.27: A LOGLIN plot of the lethargy-normed flux F i ( U ) versus E for the thermal LEU (smaller curve) and fast HEU (larger curve) systems. The area under curves is one.

<!-- image -->

## loglin plot of fission rate f(e) vs e

Figure 6.28: A LOGLOG plot of the fission rate f i ( E ) versus E for the thermal LEU (larger curve) and fast HEU (smaller curve) systems. The area under curves is one.

<!-- image -->

## loglog plot of fission rate f（e)vs e

Figure 6.29: A LOGLIN plot of the fission rate f i ( E ) versus E for the thermal LEU. The area under curve is one.

<!-- image -->

## loglinplot of fission rate f(u)vse

Figure 6.30: A LOGLIN plot of the fission rate f i ( E ) versus E for the thermal LEU (left curve) and fast HEU (right curve) systems. The area under curves is one.

<!-- image -->

loglog plot of fission rate f（u)vse

Figure 6.31: A LOGLOG plot of the fission rate F i ( E ) versus E for the thermal LEU (left curve) and fast HEU (right curve) systems. The area under curves is one.

<!-- image -->

## 6.5.9 Summary of Energy-normalized and Lethargy-normalized MCNP6 Tally Plots

Visually Accurate Area (VAA) plots allow an accurate visual assessment
of the contributions made to a tally by various ranges. For a LINLIN
plot, the energy-normalized f i ( E ) s are VAA plots. For a LOGLIN
plot, the LETHARGY command produces lethargy-normalized F i ( U ) s that
are VAA plots. All other plots, which may provide useful information
about the tally, are not VAA plots. The energy location in a tally bin
of the statistical error bars for energy-normalized and lethargy-
normalized plots is different, as shown by Eqs. (6.5) and (6.14).

VAA plots are useful tools that allow visual assessment of the
characteristics of the tally by examining the area under the curve.
Equal abscissa bin spacing is not required for VAA plots. The more
uniformly subdivided the abscissa intervals are, however, the easier the
area visualization becomes; e.g., it may be hard to estimate the area
for a narrow bin that is much higher than other bins. If the abscissa
intervals are all the same length, then the shape of a plot is identical
to a NONORM plot where the bin T i s themselves are plotted. The
magnitude of the two curves will differ by the bin-width normalization.
MCNP6 can create lethargy-normalized plots for ln( E ) abscissas for all
particle types when the LETHARGY plotting command is used.

The bottom-line: both the LINLIN energy-normalized and LOGLIN lethargy-
normalized plots of energydependent tallies allow a direct tally
contribution visualization by the area under the histogram.