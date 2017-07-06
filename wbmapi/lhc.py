#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class LHCFillScheme:
    """All useful information for a typical LHC filling scheme. For more information see [https://lpc.web.cern.ch/cgi-bin/fillingSchemeTab.py]"""
    _scheme_ = []
    def __init__(self, scheme=""):
        if scheme!="":
            self._scheme_ = scheme.split('_', 5)
        else: self._scheme_ = [""]*6
        assert(len(self._scheme_)==6)
    def raw(self):
        """Extract the raw format of the filling scheme"""
        return '_'.join(self._scheme_)
    def spacing(self):
        """Bunch spacing"""
        return self._scheme_[0]
    def numFillBunches(self):
        """Number of bunches per beam"""
        return int(self._scheme_[1].replace('b', ''))
    def numBunchesIP1and5(self):
        """Number of collisions in IP1 and IP5"""
        return int(self._scheme_[2])
    def numBunchesIP2(self):
        """Number of collisions in IP2"""
        return int(self._scheme_[3])
    def numBunchesIP8(self):
        """Number of collisions in IP8"""
        return int(self._scheme_[4])
    def variant(self):
        """General variant: `trainlength_injections_specialinfo`"""
        return self._scheme_[5]

class LHCstatus:
    fillnum = 0
    collidingbunches = 0
    betastar5 = 0.0
    comment = ""
    injectionsch = LHCFillScheme()
    lastupdate = datetime.now()
    def dump(self):
        print 'LHC status (updated on', self.lastupdate, '):'
        print '  fill:', self.fillnum
        print '  injection scheme:', self.injectionsch.raw()
        print '    (at IP1/5:', self.injectionsch.numBunchesIP1and5(), 'bunches)'
        print '  colliding bunches:', self.collidingbunches
        print '  beta* @ IP5:', self.betastar5
        print '  comment:', self.comment

