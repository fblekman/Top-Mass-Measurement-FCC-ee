from heppy.framework.analyzer import Analyzer
from ROOT import TLorentzVector
from itertools import combinations

class JetsInvariantMasses(Analyzer):
    '''
    from analyzers.JetsInvariantMasses import JetsInvariantMasses
    jets_variables = cfg.Analyzer(
      JetsInvariantMasses,
      jets = 'jets',
    )
    '''

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)

        four_jets_mass = 0.
        min_jets_mass = 0.
        second_min_jets_mass = 0.

        def invariant_mass(ptc_list):
            totalp4 = TLorentzVector(0,0,0,0)
            for ptc in ptc_list:
                totalp4 += ptc.p4()
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
