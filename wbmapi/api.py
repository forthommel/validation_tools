#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import auth
import xml.etree.ElementTree as tree
from datetime import datetime

from lhc import LHCStatus, LHCShortStatus, LHCFillScheme

class api:
    _base_url_ = 'https://cmswbm.cern.ch/cmsdb/servlet'

    def __init__(self):
        print 'api created... base url=%s' % (self._base_url_)

    def getLHCShortStatus(self):
        data = auth.getContent('%s/LHCStatusDisplay?XML=1' % self._base_url_)
        data = tree.fromstring(data)

        for s in data.findall('DataSample'):
            lhc = LHCShortStatus()
            try:
                lhc.fillnum = int(s.find('fillnum').text)
                lhc.mode = s.find('mode').text
                lhc.prev_mode = s.find('prevmode').text
                lhc.timestamp = datetime.strptime(s.find('timestamp').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
            except AttributeError:
                print 'ERROR in parsing the LHC short status report'
                pass

            return lhc

    def getLHCStatus(self):
        data = auth.getContent('%s/LhcMonitor?FORMAT=XML' % self._base_url_)
        data = tree.fromstring(data)

        for s in data.findall('LhcSample'):
            lhc = LHCStatus()

            try:
                lhc.fillnum = int(s.find('FILLN').text)
                lhc.lastupdate = datetime.strptime(s.find('collectionTimeGMT').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
                lhc.collidingbunches = int(s.find('nCollidingBunches').text)
                lhc.injectionsch = LHCFillScheme(s.find('activeInjectionScheme').text.strip())
                lhc.comment = s.find('lhcPageOne').text.strip()
                lhc.betastar5 = float(s.find('BSTAR5').text)
            except AttributeError:
                print 'ERROR in parsing the LHC full status report'
                pass

            return lhc

