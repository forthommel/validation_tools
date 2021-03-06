#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import auth
import xml.etree.ElementTree as tree
from datetime import datetime

from lhc import LHCStatus, LHCShortStatus, LHCFillScheme
from cms import CMSStatus
from run import RunInfo, TriggerInfo

class api:
    _base_url_ = 'https://cmswbm.cern.ch/cmsdb/servlet'

    def __init__(self):
        print 'api created... base url=%s' % (self._base_url_)

    def getLHCShortStatus(self):
        """Retrieve a short summary of LHC conditions"""
        data = auth.getContent('%s/LHCStatusDisplay?XML=1' % self._base_url_)
        data = tree.fromstring(data)

        s = data.find('DataSample')
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
        """Retrieve a full summary of LHC conditions"""
        data = auth.getContent('%s/LhcMonitor?FORMAT=XML' % self._base_url_)
        data = tree.fromstring(data)

        s = data.findall('LhcSample')
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

    def getCMSStatus(self):
        """Retrieve a full summary of CMS conditions"""
        data = auth.getContent('%s/PageZero?FORMAT=XML' % self._base_url_)
        data = tree.fromstring(data)

        s = data.find('PageZeroSample')
        cms = CMSStatus()
        try:
            cms.collection_time = datetime.strptime(s.find('collectionTimeGMT').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
            cms.magnetic_field = float(s.find('bField').text)
            cms.magnet_current = float(s.find('magCur').text)
            cms.vacuum_pressure = float(s.find('vacuum').text)
            cms.feds_state['TRG'] = s.find('IO_TRG').text=='IN'
            cms.feds_state['CSC'] = s.find('IO_CSC').text=='IN'
            cms.feds_state['DAQ'] = s.find('IO_DAQ').text=='IN'
            cms.feds_state['DQM'] = s.find('IO_DQM').text=='IN'
            cms.feds_state['DT'] = s.find('IO_DT').text=='IN'
            cms.feds_state['ECAL'] = s.find('IO_ECAL').text=='IN'
            cms.feds_state['ES'] = s.find('IO_ES').text=='IN'
            cms.feds_state['HCAL'] = s.find('IO_HCAL').text=='IN'
            cms.feds_state['PIXEL'] = s.find('IO_PIXEL').text=='IN'
            cms.feds_state['RPC'] = s.find('IO_RPC').text=='IN'
            cms.feds_state['SCAL'] = s.find('IO_SCAL').text=='IN'
            cms.feds_state['TRACKER'] = s.find('IO_TRACKER').text=='IN'
            cms.feds_state['CASTOR'] = s.find('IO_CASTOR').text=='IN'
            cms.feds_state['HF'] = s.find('IO_HFLUMI').text=='IN'
            cms.feds_state['CTPPS'] = s.find('IO_CTPPS_TOT').text=='IN'
            cms.daq_state = s.find('state').text
            cms.dead_time = float(s.find('deadTimeActivePercent').text)
            cms.t0_transfer = s.find('tier0Transfer').text=='ON'
            cms.run_number = int(s.find('runNumber').text)
            cms.lumi_section = int(s.find('lumiSegmentNr').text)
            cms.l1_menu = s.find('l1Menu').text
            cms.hlt_rate = float(s.find('hltRate').text)
            cms.instant_lumi = float(s.find('instantLumi').text)
            cms.fill_lumi = float(s.find('lumiFill').text)
            cms.crossing_angle = float(s.find('angle').text)
        except AttributeError:
            print 'ERROR in parsing the CMS status report'
            pass

        return cms

    def getRunInfo(self, run_id, get_triggers=False):
        """Retrieve all available information on a CMS run
        @param get_triggers Also retrieve the L1 trigger level information?
        """
        data = auth.getContent('%s/RunSummary?RUN=%d&DB=default&FORMAT=XML' % (self._base_url_, run_id))
        data = tree.fromstring(data)

        s = data.find('runInfo')
        run = RunInfo(run_id)
        try:
            run.lhc_fill = int(s.find('lhcFill').text)
            run.lhc_energy = float(s.find('lhcEnergy').text)
            run.lumi_sections = int(s.find('nLumiSections').text)
            run.sequence = s.find('sequence').text
            run.start = datetime.strptime(s.find('startTime').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
            if s.find('stopTime').text==None:
                run.stopped = False
            else:
                run.start = datetime.strptime(s.find('stopTime').text+' GMT', '%Y.%m.%d %H:%M:%S %Z')
        except AttributeError:
            print 'ERROR in parsing the Run report'
            pass
        if get_triggers:
            try:
                algo_names = s.find('algoNames')
                algo_initial_presc = s.find('algoInitialPrescale')
                algo_en = s.find('algoEnable')
                gt_algo_low = s.find('gtAlgoLow')
                for i in range(0,512):
                    trig = TriggerInfo()
                    trig.name = algo_names.find('i%d' % i).text
                    if trig.name==None: continue
                    trig.enabled = algo_en.find('i%d' % i).text=='true'
                    trig.rate = float(gt_algo_low.find('i%d' % i).text)
                    run.triggers.append(trig)
            except AttributeError:
                print 'ERROR in parsing the Triggers report'
                pass

        return run
