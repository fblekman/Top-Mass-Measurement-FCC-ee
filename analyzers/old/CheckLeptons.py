from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter, Counters

class CheckLeptons(Analyzer):
    '''
    Example:
    from analyzers.CheckLeptons import CheckLeptons
    check_leptons = cfg.Analyzer(
      CheckLeptons,
      objects = 'sel_iso_leptons',
    )
    '''

    def beginLoop(self, setup):
        super(CheckLeptons, self).beginLoop(setup)

        self.counters.addCounter('events')
        self.counters.counter('events').register('All events')
        self.counters.counter('events').register('One lepton')


    def process(self, event):

        input_collection = getattr(event, self.cfg_ana.objects)

        self.counters.counter('events').inc('All events')
        if len(input_collection) == 1:
            self.counters.counter('events').inc('One lepton')
        else:
            return False
