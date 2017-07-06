import subprocess

class api:
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
            if 'Showing ' in l or len(l)==0 or l=='None': continue
            output.append(l)
        return output
