from wbmapi import api

def main():
    wbm = api.api()
    #lhc_status = wbm.getLHCShortStatus()
    #lhc_status.dump()

    cms_status = wbm.getCMSStatus()
    #cms_status.dump()
    print 'current CMS run:', cms_status.run_number

    run_info = wbm.getRunInfo(cms_status.run_number, True)
    run_info.dump()

if __name__=='__main__':
    main()
    
