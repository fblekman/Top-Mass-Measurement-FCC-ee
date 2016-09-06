#!/bin/env python
"""Book and fill functions specialized for e+e- collision and top mass analysis."""

def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )

# Simple p4
def bookMyP4( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_px'.format(pName=pName))
    var(tree, '{pName}_py'.format(pName=pName))
    var(tree, '{pName}_pz'.format(pName=pName))
    var(tree, '{pName}_theta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_m'.format(pName=pName))

def fillMyP4( tree, pName, p4 ):
    fill(tree, '{pName}_e'.format(pName=pName), p4.e() )
    fill(tree, '{pName}_px'.format(pName=pName), p4.p4().Px() )
    fill(tree, '{pName}_py'.format(pName=pName), p4.p4().Py() )
    fill(tree, '{pName}_pz'.format(pName=pName), p4.p4().Pz() )
    fill(tree, '{pName}_theta'.format(pName=pName), p4.p4().Theta() )
    fill(tree, '{pName}_phi'.format(pName=pName), p4.phi() )
    fill(tree, '{pName}_m'.format(pName=pName), p4.m() )

# Simple particle
def bookMyParticle( tree, pName ):
    var(tree, '{pName}_pdgid'.format(pName=pName))
    bookMyP4(tree, pName)

def fillMyParticle( tree, pName, particle ):
    fill(tree, '{pName}_pdgid'.format(pName=pName), particle.pdgid() )
    fillMyP4(tree, pName, particle )

# jet
def bookComponent( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))

def fillComponent(tree, pName, component):
    fill(tree, '{pName}_e'.format(pName=pName), component.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), component.pt() )
    fill(tree, '{pName}_num'.format(pName=pName), component.num() )

pdgids = [211, 22, 130, 11, 13]

def bookMyJet( tree, pName ):
    bookMyP4(tree, pName )
    for pdgid in pdgids:
        bookComponent(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid))

    var(tree, '{pName}_btag'.format(pName = pName))
    var(tree, '{pName}_logbtag'.format(pName = pName))
    var(tree, '{pName}_log10btag'.format(pName = pName))

    var(tree, '{pName}_n_signif_larger3'.format(pName = pName))
    var(tree, '{pName}_m_inv_signif_larger3'.format(pName = pName))
    var(tree, '{pName}_angle_wrt_jet_dir_larger'.format(pName = pName))
    var(tree, '{pName}_combined_b_tag'.format(pName = pName))

    var(tree, '{pName}_mc_b_quark_index'.format(pName = pName))

def fillMyJet( tree, pName, jet ):
    fillMyP4(tree, pName, jet )

    for pdgid in pdgids:
        component = jet.constituents.get(pdgid, None)
        if component is not None:
            fillComponent(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid), component )

    if hasattr(jet, 'btag'):
        fill(tree, '{pName}_btag'.format(pName = pName), jet.btag)
        fill(tree, '{pName}_logbtag'.format(pName = pName), jet.logbtag)
        fill(tree, '{pName}_log10btag'.format(pName = pName), jet.log10btag)

    if hasattr(jet, 'n_signif_larger3'):
        fill(tree, '{pName}_n_signif_larger3'.format(pName = pName), jet.n_signif_larger3)
        fill(tree, '{pName}_m_inv_signif_larger3'.format(pName = pName), jet.m_inv_signif_larger3)
        fill(tree, '{pName}_angle_wrt_jet_dir_larger'.format(pName = pName), jet.angle_wrt_jet_dir_larger)

    if hasattr(jet, 'combined_b_tag'):
        fill(tree, '{pName}_combined_b_tag'.format(pName = pName), jet.combined_b_tag)

    if hasattr(jet, 'mc_b_quark_index'):
        fill(tree, '{pName}_mc_b_quark_index'.format(pName = pName), jet.mc_b_quark_index)


# Isolation
iso_pdgids = [211, 22, 130]

def bookMyIso(tree, pName):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))
    var(tree, '{pName}_pt_wrt_lepton'.format(pName=pName))

def fillMyIso(tree, pName, iso):
    fill(tree, '{pName}_e'.format(pName=pName), iso.sume )
    fill(tree, '{pName}_num'.format(pName=pName), iso.num )
    fill(tree, '{pName}_pt_wrt_lepton'.format(pName=pName), iso.pt_wrt_lepton )


# Lepton
def bookMyLepton( tree, pName, pflow=True ):
    bookMyParticle(tree, pName )
    if pflow:
        for pdgid in iso_pdgids:
            bookMyIso(tree, '{pName}_iso{pdgid:d}'.format(pName=pName, pdgid=pdgid))
    bookMyIso(tree, '{pName}_iso'.format(pName=pName))
    var(tree, '{pName}_match_with_mc'.format(pName=pName))

def fillMyLepton( tree, pName, lepton ):
    fillMyParticle(tree, pName, lepton )
    for pdgid in iso_pdgids:
        isoname='iso_{pdgid:d}'.format(pdgid=pdgid)
        if hasattr(lepton, isoname):
            iso = getattr(lepton, isoname)
            fillMyIso(tree, '{pName}_iso{pdgid:d}'.format(pName=pName, pdgid=pdgid), iso)
    fillMyIso(tree, '{pName}_iso'.format(pName=pName), lepton.iso)
    if hasattr(lepton, 'match_with_mc'):
        fill(tree, '{pName}_match_with_mc'.format(pName=pName), lepton.match_with_mc)


# Mc b quark
def bookMCbQuark(tree, pName):
    bookMyP4(tree, pName)
    var(tree, '{pName}_index_nearest_jet'.format(pName=pName) )
    var(tree, '{pName}_delta_alpha_wrt_nearest_jet'.format(pName=pName) )
    bookMyJet(tree, '{pName}_nearest_jet'.format(pName=pName) )

def fillMCbQuark(tree, pName, quark):
    fillMyP4(tree, pName, quark)
    fill(tree, '{pName}_index_nearest_jet'.format(pName=pName), quark.index_nearest_jet )
    fill(tree, '{pName}_delta_alpha_wrt_nearest_jet'.format(pName=pName), quark.delta_alpha_wrt_nearest_jet )
    fillMyJet(tree, '{pName}_nearest_jet'.format(pName=pName), quark.nearest_jet )


# Jets Variable
def bookJetsInvariantMasses(tree):
    var(tree, 'four_jets_mass')
    var(tree, 'min_jets_mass')
    var(tree, 'second_min_jets_mass')

def fillJetsInvariantMasses(tree, event):
    if hasattr(event, 'four_jets_mass'):
        fill(tree, 'four_jets_mass', event.four_jets_mass)
        fill(tree, 'min_jets_mass', event.min_jets_mass)
        fill(tree, 'second_min_jets_mass', event.second_min_jets_mass)


# Missing Energy
def bookMissingEnergy(tree):
    bookMyP4(tree, 'missing_sim')
    bookMyP4(tree, 'missing_rec')

def fillMissingEnergy(tree, event):
    if hasattr(event, 'missing_sim'):
        fillMyP4(tree, 'missing_sim', event.missing_sim)
    if hasattr(event, 'missing_rec'):
        fillMyP4(tree, 'missing_rec', event.missing_rec)


# Top Constrainer
def bookTopConstrainer(tree):
    var(tree, 'success')
    var(tree, 'chi2_algorithm')
    var(tree, 'tophadRec')
    var(tree, 'whadRec')
    var(tree, 'toplepRec')
    var(tree, 'wlepRec')
    var(tree, 'missingMassRec')
    var(tree, 'tophadFit')
    var(tree, 'whadFit')
    var(tree, 'toplepFit')
    var(tree, 'wlepFit')
    var(tree, 'missingMassFit')

    var(tree, 'chi2_tophadRec')
    var(tree, 'chi2_whadRec')
    var(tree, 'chi2_toplepRec')
    var(tree, 'chi2_wlepRec')
    var(tree, 'chi2_top_constrainer')

def fillTopConstrainer(tree, event):

    if hasattr(event, 'success'):
        fill(tree, 'success', event.success)

    if hasattr(event, 'chi2_algorithm'):
        fill(tree, 'chi2_algorithm', event.chi2_algorithm)
        fill(tree, 'tophadRec', event.tophadRec.p4().M())
        fill(tree, 'whadRec', event.whadRec.p4().M())
        fill(tree, 'toplepRec', event.toplepRec.p4().M())
        fill(tree, 'wlepRec', event.wlepRec.p4().M())
        fill(tree, 'missingMassRec', event.missingMassRec.p4().M())
        fill(tree, 'tophadFit', event.tophadFit.p4().M())
        fill(tree, 'whadFit', event.whadFit.p4().M())
        fill(tree, 'toplepFit', event.toplepFit.p4().M())
        fill(tree, 'wlepFit', event.wlepFit.p4().M())
        fill(tree, 'missingMassFit', event.missingMassFit.p4().M())

        fill(tree, 'chi2_tophadRec', event.chi2_tophadRec)
        fill(tree, 'chi2_whadRec', event.chi2_whadRec)
        fill(tree, 'chi2_toplepRec', event.chi2_toplepRec)
        fill(tree, 'chi2_wlepRec', event.chi2_wlepRec)
        fill(tree, 'chi2_top_constrainer', event.chi2_top_constrainer)
