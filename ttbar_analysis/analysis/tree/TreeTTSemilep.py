from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from utils.my_ntuple import *

from ROOT import TFile

class TreeTTSemilep(Analyzer):

    def beginLoop(self, setup):
        super(TreeTTSemilep, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        var(self.tree, 'ev_number')

        bookMyParticle(self.tree, 'mc_lepton')
        bookMyParticle(self.tree, 'mc_neutrino')
        bookMyParticle(self.tree, 'mc_w_lep')

        bookMyLepton(self.tree, 'lep1')

        bookMyJet(self.tree, 'jet1')
        bookMyJet(self.tree, 'jet2')
        bookMyJet(self.tree, 'jet3')
        bookMyJet(self.tree, 'jet4')

        bookMCbQuark(self.tree, 'mc_bquark1')
        bookMCbQuark(self.tree, 'mc_bquark2')

        bookJetsInvariantMasses(self.tree)
        bookMissingEnergy(self.tree)


        bookMyP4(self.tree, 'total_gen')
        bookMyP4(self.tree, 'total_gen_visible')
        bookMyP4(self.tree, 'total_rec')


        var(self.tree, 'gen_energy')
        var(self.tree, 'gen_charged')
        var(self.tree, 'gen_photon')
        var(self.tree, 'gen_neutral')

        var(self.tree, 'rec_energy')
        var(self.tree, 'rec_charged')
        var(self.tree, 'rec_photon')
        var(self.tree, 'rec_neutral')

        var(self.tree, 'delta_energy')
        var(self.tree, 'delta_charged')
        var(self.tree, 'delta_photon')
        var(self.tree, 'delta_neutral')

        var(self.tree, 'n_gen')
        var(self.tree, 'n_gen_charged')
        var(self.tree, 'n_gen_photon')
        var(self.tree, 'n_gen_neutral')

        var(self.tree, 'n_rec')
        var(self.tree, 'n_rec_charged')
        var(self.tree, 'n_rec_photon')
        var(self.tree, 'n_rec_neutral')

        bookTopConstrainer(self.tree)

    def process(self, event):
        self.tree.reset()

        fill(self.tree, 'ev_number', event.iEv)

        if hasattr(event, 'mc_lepton'):
            mc_lepton = getattr(event, self.cfg_ana.mc_lepton)
            fillMyParticle(self.tree, 'mc_lepton', mc_lepton)
        if hasattr(event, 'mc_neutrino'):
            mc_neutrino = getattr(event, self.cfg_ana.mc_neutrino)
            fillMyParticle(self.tree, 'mc_neutrino', mc_neutrino)
        if hasattr(event, 'mc_w_lep'):
            mc_w_lep = getattr(event, "mc_w_lep")
            fillMyParticle(self.tree, 'mc_w_lep', mc_w_lep)

        leptons = getattr(event, self.cfg_ana.leptons)
        fillMyLepton(self.tree, 'lep1', leptons[0])

        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == 4:
                break
            fillMyJet(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

        if hasattr(event, self.cfg_ana.mc_b_quarks):
            mc_b_quarks = getattr(event, self.cfg_ana.mc_b_quarks)
            for iquark, quark in enumerate(mc_b_quarks):
                if iquark == 2:
                    break
                fillMCbQuark(self.tree, 'mc_bquark{iquark}'.format(iquark=iquark+1), quark)

        fillJetsInvariantMasses(self.tree, event)
        fillMissingEnergy(self.tree, event)


        if hasattr(event, 'total_gen'):
            fillMyP4(self.tree, 'total_gen', event.total_gen)
            fillMyP4(self.tree, 'total_gen_visible', event.total_gen_visible)
            fillMyP4(self.tree, 'total_rec', event.total_rec)

        if hasattr(event, 'gen_energy'):

            fill(self.tree, 'gen_energy', event.gen_energy)
            fill(self.tree, 'gen_charged', event.gen_charged)
            fill(self.tree, 'gen_photon', event.gen_photon)
            fill(self.tree, 'gen_neutral', event.gen_neutral)

            fill(self.tree, 'rec_energy', event.rec_energy)
            fill(self.tree, 'rec_charged', event.rec_charged)
            fill(self.tree, 'rec_photon', event.rec_photon)
            fill(self.tree, 'rec_neutral', event.rec_neutral)

            fill(self.tree, 'delta_energy', event.delta_energy)
            fill(self.tree, 'delta_charged', event.delta_charged)
            fill(self.tree, 'delta_photon', event.delta_photon)
            fill(self.tree, 'delta_neutral', event.delta_neutral)

            fill(self.tree, 'n_gen', event.n_gen)
            fill(self.tree, 'n_gen_charged', event.n_gen_charged)
            fill(self.tree, 'n_gen_photon', event.n_gen_photon)
            fill(self.tree, 'n_gen_neutral', event.n_gen_neutral)

            fill(self.tree, 'n_rec', event.n_rec)
            fill(self.tree, 'n_rec_charged', event.n_rec_charged)
            fill(self.tree, 'n_rec_photon', event.n_rec_photon)
            fill(self.tree, 'n_rec_neutral', event.n_rec_neutral)

        fillTopConstrainer(self.tree, event)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
