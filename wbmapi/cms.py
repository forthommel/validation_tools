from datetime import datetime

class CMSStatus:
    collection_time = datetime.now()
    feds_state = {}
    # DCS-related
    magnetic_field = 0.0
    magnet_current = 0.0
    vacuum_pressure = 0.0
    # DAQ-related
    daq_state = ""
    dead_time = 0.0
    t0_transfer = False
    run_number = 0
    lumi_section = 0
    # trigger-related
    l1_menu = ""
    hlt_rate = 0.0
    # LHC-related
    instant_lumi = 0.0
    fill_lumi = 0.0
    crossing_angle = 0.0

    def inGlobal(self):
      """List of subsystems inside the global run"""
      return [fed for fed, state in self.feds_state.iteritems() if state==True]

    def inLocal(self):
      """List of subsystems remaining out of the global run"""
      return [fed for fed, state in self.feds_state.iteritems() if state==False]

    def dump(self):
        print 'CMS status (at '+self.collection_time.ctime()+'):'
        print '  DCS info:'
        print '    magnetic field (@', self.magnet_current, 'magnet current):', self.magnetic_field,'T'
        print '    vacuum pressure:', self.vacuum_pressure
        print '  DAQ state:', self.daq_state
        print '    current run:', self.run_number, "ls:", self.lumi_section
        print '    subsystems IN:', self.inGlobal()
        print '    subsystems OUT:', self.inLocal()
        print '    T0 transfer?', self.t0_transfer
        print '    dead time:', self.dead_time,'%'
        print '  TRG info:'
        print '    L1 menu:', self.l1_menu
        print '    HLT rate:', self.hlt_rate, 'kHz'
