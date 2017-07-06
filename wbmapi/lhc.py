#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class LHCstatus:
    fillnum = 0
    collidingbunches = 0
    betastar5 = 0.0
    comment = ""
    injectionsch = ""
    lastupdate = datetime.now()
    def dump(self):
        print 'LHC status (updated on', self.lastupdate, '):'
        print '  fill:', self.fillnum
        print '  injection scheme:', self.injectionsch.raw()
        print '    (at IP1/5:', self.injectionsch.numBunchesIP1and5(), 'bunches)'
        print '  colliding bunches:', self.collidingbunches
        print '  beta* @ IP5:', self.betastar5
        print '  comment:', self.comment

class LHCFillScheme:
    _scheme_ = []
    def __init__(self, scheme):
        self._scheme_ = scheme.split('_', 5)
        assert(len(self._scheme_)==6)
    def raw(self):
        return '_'.join(self._scheme_)
    def spacing(self):
        return self._scheme_[0]
    def numFillBunches(self):
        return int(self._scheme_[1].replace('b', ''))
    def numBunchesIP1and5(self):
        return int(self._scheme_[2])
    def numBunchesIP2(self):
        return int(self._scheme_[3])
    def numBunchesIP8(self):
        return int(self._scheme_[4])
    def variant(self):
        return self._scheme_[5]

