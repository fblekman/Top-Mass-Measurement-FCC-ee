# Unordered suggestions by a Professor to improve the b tagging algorithm
=======================================================
## To start with
* CMS software is mostly taken from the ALEPH one + improvements
* The algorithm I wrote is called __jet probability__

## What CMS is currently using
* Track counting: sort the tracks by IP significance and consider as discriminant variables the IP of the 4th or 5th track.
* Secondary vertex significance
* Jet probability: it is what we coded, but Andrea said that it requires that all the jets with probability < 0.5% (or something like that) must receive the same actual probability, that means _probability < 0.5% => probability = 0.5%_. Indeed, without this requirement, it is enough to have one track with very large significance to get a very small probability. You can also make a very simple combination by considering the product _JetProbability x P4_ where P4 is the probability of the 4th track (ordered by IP significance).
* Significance Secondary vertex (ssv): you fit a Secondary vertex and consider the significance. In addition you can consider the secondary vertex mass.
* Then you can combine all these variables with a MVA (that is the CMS algorithm).
* There is no significant difference between the two IP definitions, and Andrea does not even remember very well which of the two is currently used in the CMS software.
* The cut on the distance between the jet axis and the track is really important (in CMS is _dist < 700 um_)

## What we should do in Professor's opinion
* Do something in order to consider:
  * Fake tracks: difficult, probably the only way is a full simulation with pattern recognition
  * Early multiple scattering: if a particle gets important multiple scattering in the inner part of the tracker, then the track resolution is more affected than if it got in the outer part (and probably it is not really gaussian).
* Implementing the geometry for the tracker (that means, given a real track, consider the hits on the tracker, apply a smearing and then fit again the track __without__ pattern recognition) is useful only to obtain the correct errors on the track parameters. This could be probably also achieved by a correct parametrization of the covariance matrix of the track parameters, as a function of the hit resolution. This does not consider neither the early multiple scattering, nor the fake tracks though.
* Maybe, in order to consider the early multiple scattering, one can propagate the track between two consecutive layers of the tracker and then create a new track with the parameters changed due to the multiple scattering and iterate these process until the end of the tracker. Then consider these hits and fit the track.
* For the secondary vertex, we can either write the vertex fit, or use the __RAVE__ package (https://rave.hepforge.org/) that, of course, must be compiled and linked in the FCC software.
