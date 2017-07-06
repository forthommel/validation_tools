#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import auth
import xml.etree.ElementTree as tree
from datetime import datetime

from lhc import LHCstatus, LHCFillScheme

class api:
    _base_url_ = 'https://cmswbm.cern.ch/cmsdb/servlet'

    def __init__(self):
        print 'api created... base url=%s' % (self._base_url_)

    def getLHCstatus(self):
        data = auth.getContent('%s/LhcMonitor?FORMAT=XML' % self._base_url_)
        data = tree.fromstring(data)

        for s in data.findall('LhcSample'):
            lhc = LHCstatus()

            try:
                lhc.fillnum = int(s.find('FILLN').text)
                print s.find('collectionTimeGMT').text, datetime.strptime(s.find('collectionTimeGMT').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
                lhc.lastupdate = datetime.strptime(s.find('collectionTimeGMT').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
                lhc.collidingbunches = int(s.find('nCollidingBunches').text)
                lhc.injectionsch = LHCFillScheme(s.find('activeInjectionScheme').text.strip())
                lhc.comment = s.find('lhcPageOne').text.strip()
                lhc.betastar5 = float(s.find('BSTAR5').text)
            except AttributeError: pass

            return lhc

