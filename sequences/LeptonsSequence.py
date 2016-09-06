import heppy.framework.config as cfg

from heppy.analyzers.Filter import Filter
leptons = cfg.Analyzer(
    Filter,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'rec_particles',
    filter_func = lambda ptc: ptc.e()>10. and abs(ptc.pdgid()) in [11, 13]
)


from analyzers.LeptonAnalyzer import LeptonAnalyzer
from utils.isolation import Cone
iso_leptons = cfg.Analyzer(
    LeptonAnalyzer,
    leptons = 'leptons',
    particles = 'rec_particles',
    iso_area = Cone(0.3)
)


sel_iso_leptons = cfg.Analyzer(
    Filter,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    filter_func = lambda lep: lep.iso.sume < 15.
)


# from analyzers.CheckLeptons import CheckLeptons
# check_leptons = cfg.Analyzer(
#   CheckLeptons,
#   objects = 'sel_iso_leptons',
# )


leptons_sequence = [
    leptons,
    iso_leptons,
    sel_iso_leptons,
    # check_leptons
    ]
