import heppy.framework.config as cfg

def top_constrainer_sequence(cdm_energy):
    from utils.TopConstrainerAnalyzer import TopConstrainerAnalyzer
    top_constrainer = cfg.Analyzer(
      TopConstrainerAnalyzer,
      jets = 'jets',
      leptons = 'leptons',
      sqrts = 350.,
      top_mass = 173.,
      w_mass = 80.4,
      tophadRec_m = 164.59,
      tophadRec_w = 17.13,
      whadRec_m = 81.88,
      whadRec_w = 16.69,
      toplepRec_m = 177.37,
      toplepRec_w = 20.25,
      wlepRec_m = 105.43,
      wlepRec_w = 17.37,
    )


    return [
        top_constrainer
    ]
