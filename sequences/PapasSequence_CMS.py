import heppy.framework.config as cfg


from heppy.analyzers.Filter import Filter
def is_stable_also_neutrino(x):
    return x.status()==1
gen_particles_stable_and_neutrinos = cfg.Analyzer(
    Filter,
    output = 'gen_particles_stable_and_neutrinos',
    input_objects = 'gen_particles',
    filter_func = is_stable_also_neutrino
)


def is_stable(x):
    return x.status()==1 and abs(x.pdgid()) not in [12,14,16] and x.pt() > 1e-5
gen_particles_stable = cfg.Analyzer(
    Filter,
    output = 'gen_particles_stable',
    input_objects = 'gen_particles',
    filter_func = is_stable
)

from heppy.analyzers.PapasSim import PapasSim
from detectors.CMS_mod import CMS
detector = CMS()

def is_energy(ptc):
    return ptc.e()>1.
papas = cfg.Analyzer(
    PapasSim,
    instance_label = 'papas',
    detector = detector,
    gen_particles = 'gen_particles_stable',
    sim_particles = 'sim_particles',
    merged_ecals = 'ecal_clusters',
    merged_hcals = 'hcal_clusters',
    tracks = 'tracks',
    output_history = 'history_nodes',
    display_filter_func = is_energy,
    display = False,
    verbose = True
)

from heppy.analyzers.PapasPFBlockBuilder import PapasPFBlockBuilder
pfblocks = cfg.Analyzer(
    PapasPFBlockBuilder,
    tracks = 'tracks',
    ecals = 'ecal_clusters',
    hcals = 'hcal_clusters',
    history = 'history_nodes',
    output_blocks = 'reconstruction_blocks'
)

from heppy.analyzers.PapasPFReconstructor import PapasPFReconstructor
pfreconstruct = cfg.Analyzer(
    PapasPFReconstructor,
    instance_label = 'papas_PFreconstruction',
    detector = detector,
    input_blocks = 'reconstruction_blocks',
    history = 'history_nodes',
    output_particles_dict = 'particles_dict',
    output_particles_list = 'particles_list'
)

def is_lepton(ptc):
    return abs(ptc.pdgid()) in [11, 13]
select_leptons = cfg.Analyzer(
    Filter,
    'sel_all_leptons',
    output = 'sim_leptons',
    input_objects = 'papas_sim_particles',
    filter_func = is_lepton
)

from analyzers.LeptonSmearerCMS import LeptonSmearerCMS
smear_leptons = cfg.Analyzer(
    LeptonSmearerCMS,
    'smear_leptons',
    output = 'smeared_leptons',
    input_objects = 'sim_leptons',
)


from heppy.analyzers.Merger import Merger
merge_particles = cfg.Analyzer(
    Merger,
    instance_label = 'merge_particles',
    inputA = 'papas_PFreconstruction_particles_list',
    inputB = 'smeared_leptons',
    output = 'rec_particles',
)

papas_sequence = [
    gen_particles_stable_and_neutrinos,
    gen_particles_stable,
    papas,
    pfblocks,
    pfreconstruct,
    select_leptons,
    smear_leptons,
    merge_particles
]
