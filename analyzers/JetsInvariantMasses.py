from heppy.framework.analyzer import Analyzer
from ROOT import TLorentzVector
from itertools import combinations

class JetsInvariantMasses(Analyzer):
    '''Store some variables related to the invariant masses of the jets.

    The analyzer computes:
    - four_jets_mass: invariant mass of the jets in the event
    - the invariant mass of every possible pair of jets
    then store:
    - four_jets_mass
    - min_jets_mass: smallest invariant mass of a pair of jets
    - second_min_jets_mass: next to smallest invariant mass of a pair of jets

    Here is an example:
    from analyzers.JetsInvariantMasses import JetsInvariantMasses
    jets_variables = cfg.Analyzer(
      JetsInvariantMasses,
      jets = 'jets',
    )

    TODO: four_jets_mass -> hadronic_mass!!! Nobody likes this name!
    '''

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)

        def invariant_mass(ptc_list):
            totalp4 = reduce(lambda total, particle: total + particle.p4(),
                             ptc_list, TLorentzVector(0., 0., 0., 0.))
            return totalp4.M()

        four_jets_mass = invariant_mass(jets)

        inv_masses = []
        for combination in combinations(jets, 2):
            aux_m_inv = invariant_mass(combination)
            inv_masses.append(aux_m_inv)
        inv_masses.sort(key = lambda x: x)
        min_jets_mass = inv_masses[0]
        second_min_jets_mass = inv_masses[1]

        event.four_jets_mass = four_jets_mass
        event.min_jets_mass = min_jets_mass
        event.second_min_jets_mass = second_min_jets_mass
