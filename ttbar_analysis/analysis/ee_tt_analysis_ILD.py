"""ttbar signal analysis.


"""

import os
import copy
import heppy.framework.config as cfg

import logging
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

import random
random.seed(0xdeadbeef)

comp_tt = cfg.Component(
    'tt_semilep_ILD',
    files = [
        'lhe/eett_semilep_350GeV2.root'
    ]
)

selectedComponents = [comp_tt]

cdm_energy = 350.
number_jets = 4
detector_name = "ILD"

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    mode = 'ee',
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

if detector_name == "ILD":
    from sequences.PapasSequence_ILD import papas_sequence, detector, papas
elif detector_name == "CMS":
    from sequences.PapasSequence_CMS import papas_sequence, detector, papas

from sequences.MatchingMCSequence import matching_mc_sequence

from sequences.LeptonsSequence import leptons_sequence

from sequences.JetsSequence import jets_sequence

from sequences.MissingEnergySequence import missing_energy_sequence

from sequences.TopConstrainerSequence import top_constrainer_sequence

from sequences.MatchingTTbarSequence import matching_ttbar_sequence

from tree.TreeTTSemilep import TreeTTSemilep
tree = cfg.Analyzer(
    TreeTTSemilep,
    mc_lepton = 'mc_lepton',
    mc_neutrino = 'mc_neutrino',
    leptons = 'sel_iso_leptons',
    jets = 'jets',
    mc_b_quarks = 'mc_b_quarks',
)


sequence = cfg.Sequence( [source] )
sequence.extend(papas_sequence)
sequence.extend(matching_mc_sequence)
sequence.extend(leptons_sequence)
sequence.extend(jets_sequence(number_jets, detector_name))
sequence.extend(missing_energy_sequence(cdm_energy))
sequence.extend(top_constrainer_sequence(cdm_energy))

sequence.extend(matching_ttbar_sequence)

sequence.extend( [tree])


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    import random
    random.seed(0xdeadbeef)

    def process(iev=None):
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        if display:
            display.draw()

    def next():
        loop.process(loop.iEvent+1)
        if display:
            display.draw()

    iev = None
    usage = """usage: python ee_tt_analysis_cfg.py [ievent]

    Provide ievent as an integer, or loop on the first events.
    You can also use this configuration file in this way:

    heppy_loop.py OutDir/ ee_tt_analysis_cfg.py -f -N 100
    """
    if len(sys.argv)==2:
        papas.display = True
        try:
            iev = int(sys.argv[1])
        except ValueError:
            print usage
            sys.exit(1)
    elif len(sys.argv)>2:
        print usage
        sys.exit(1)


    loop = Looper( 'looper', config,
                   nEvents=10,
                   nPrint=1,
                   timeReport=True)

    simulation = None
    for ana in loop.analyzers:
        if hasattr(ana, 'display'):
            simulation = ana
    display = getattr(simulation, 'display', None)
    simulator = getattr(simulation, 'simulator', None)
    if simulator:
        detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
