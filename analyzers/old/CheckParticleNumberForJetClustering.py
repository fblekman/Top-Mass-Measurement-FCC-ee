from heppy.framework.analyzer import Analyzer

class CheckParticleNumberForJetClustering(Analyzer):
    '''
    from analyzers.CheckParticleNumberForJetClustering import CheckParticleNumberForJetClustering
    checker = cfg.Analyzer(
      CheckParticleNumberForJetClustering,
      input = 'particles_not_iso_lep',
      n_min = 4
    )
    '''

    def process(self, event):
        input_collection = getattr(event, self.cfg_ana.input)
        n_min = self.cfg_ana.n_min


        if len(input_collection) < n_min:
            return False
