import subprocess
import re

class api:
    _rgx_outof_ = re.compile('out of (\\d+) results')
    def __init__(self):
        'das api initialised...'

    def runsInDataset(self, dataset):
        return self.call('run dataset=%s' % dataset)

    def datasetsForRun(self, run):
        return self.call('dataset run=%d' % run )

    def call(self, query, limit=500):
        args = ['das_client', '--limit=%d' % limit, '--query', query]
        print args[0], 'will execute "%s"' % query
        res = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        output = []
        for l in res.split('\n'):
            if len(l)==0 or l=='None': continue
            if 'Showing ' in l:
                m = re.search(self._rgx_outof_, l)
                total_res = int(m.group(1))
                continue
            output.append(l)
        if total_res>limit:
            print 'WARNING more results than the expected limit:', total_res, '>', limit
        return output
