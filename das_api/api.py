import subprocess

class api:
    def __init__(self):
        'das api initialised...'

    def call(self, query):
        res = subprocess.Popen(['das_client', '--limit=100', '--query', query], stdout=subprocess.PIPE).communicate()[0]
        for l in res.split('\n'):
            print l
