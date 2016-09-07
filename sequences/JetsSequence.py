import heppy.framework.config as cfg

def jets_sequence(number_jets, detector_name):
    from heppy.analyzers.Masker import Masker
    particles_not_iso_lep = cfg.Analyzer(
        Masker,
        output = 'particles_not_iso_lep',
        input = 'rec_particles',
        mask = 'sel_iso_leptons',
    )

    # from analyzers.CheckParticleNumberForJetClustering import CheckParticleNumberForJetClustering
    # check_particle_number = cfg.Analyzer(
    #   CheckParticleNumberForJetClustering,
    #   input = 'particles_not_iso_lep',
    #   n_min = number_jets
    # )

    from analyzers.CheckParticles import CheckParticles
    check_particles = cfg.Analyzer(
      CheckParticles,
      leptons = 'sel_iso_leptons',
      other_particles = 'particles_not_iso_lep',
      n_lep = 1,
      n_min = 4
    )

    from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
    jets = cfg.Analyzer(
        JetClusterizer,
        output = 'jets',
        particles = 'particles_not_iso_lep',
        fastjet_args = dict( njets = number_jets)
    )


    def track_selection_function(track):
        return track.q() != 0 and \
        abs(track.path.smeared_impact_parameter) < 2.5e-3 and \
        track.path.ip_resolution < 7.5e-4 and \
        track.e() > 0.4 # and \
        # track.path.min_dist_to_jet.Mag() < 7e-4 and \
        # track.path.min_dist_to_jet_significance < 10 and \
        # track.path.jet_point_min_approach.Mag() < 1e-2


    if detector_name == "CMS":
        import math
        def aleph_resolution(ptc):
            momentum = ptc.p3().Mag()
            return math.sqrt(25.**2 + 95.**2/ (momentum**2) )*1e-6

        from analyzers.ImpactParameterSimple import ImpactParameterSimple
        ip_simple = cfg.Analyzer(
            ImpactParameterSimple,
            jets = 'jets',
            method = 'simple',
            track_selection = track_selection_function,
            resolution = aleph_resolution
        )
    elif detector_name == "ILD":
        import math
        def ild_resolution(ptc):
            momentum = ptc.p3().Mag()
            theta = ptc.p4().Theta()
            return math.sqrt(5.**2 + 10**2/ (momentum**2 * math.sin(theta)**3 ) )*1e-6

        from analyzers.ImpactParameterSimple import ImpactParameterSimple
        ip_simple = cfg.Analyzer(
            ImpactParameterSimple,
            jets = 'jets',
            method = 'simple',
            track_selection = track_selection_function,
            resolution = ild_resolution
        )
    else:
        import pdb; pdb.set_trace()

    from analyzers.Sorter import Sorter
    sort_jets_btag = cfg.Analyzer(
      Sorter,
      'sort_jets_btag',
      input_objects = 'jets',
      sorter_func = lambda jet : jet.logbtag
    )

    from analyzers.JetsInvariantMasses import JetsInvariantMasses
    jets_invariant_masses = cfg.Analyzer(
      JetsInvariantMasses,
      jets = 'jets',
    )

    return [
        particles_not_iso_lep,
        # check_particle_number,
        check_particles,
        jets,
        # jets_energy_correction,
        ip_simple,
        sort_jets_btag,
        jets_invariant_masses
    ]
