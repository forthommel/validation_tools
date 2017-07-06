from wbm_api import api as wbm_api
from das_api import api as das_api

def main():
    wbm = wbm_api.api()
    #lhc_status = wbm.getLHCShortStatus()
    #lhc_status.dump()

    cms_status = wbm.getCMSStatus()
    #cms_status.dump()
    print 'current CMS run:', cms_status.run_number

    run_info = wbm.getRunInfo(cms_status.run_number, False)
    run_info.dump()

    das = das_api.api()
    #das.call('run dataset=/L1MinimumBias/Run2016B-v2/RAW')
    print das.call('file dataset=/L1MinimumBias/Run2016B-v2/RAW run=275000')
    #print das.datasetsForRun(cms_status.run_number)

if __name__=='__main__':
    main()
    
