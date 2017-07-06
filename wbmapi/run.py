from datetime import datetime

class TriggerInfo:
    name = ''
    enabled = False
    gt_rate = 0.0
    def dump(self):
        print 'trigger', self.name, 'enabled?', self.enabled, 'with gt rate:', self.gt_rate

class RunInfo:
    lhc_fill = 0
    lhc_energy = 0.0
    run_number = 0
    lumi_sections = 0
    sequence = ''
    start = datetime.now()
    stop = datetime.now()
    stopped = True
    clock = ''
    triggers = []

    def __init__(self, run_id=0):
        self.run_number = run_id

    def dump(self):
        print 'Run', self.run_number, 'with', self.lumi_sections, 'lumisections recorded'
        print '  clock:', self.clock
        print '  started at', self.start.ctime()
        if self.stopped:
            print '  stopped at', self.stop.ctime()
        print '  LHC fill:', self.lhc_fill, 'at sqrt(s) =', self.lhc_energy, 'TeV'
        print '  sequence:', self.sequence
        if len(self.triggers)>0:
            print '  triggers:'
            for t in self.triggers:
                t.dump()
