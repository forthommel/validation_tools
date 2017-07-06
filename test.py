from wbmapi import api

def main():
    wbm = api.api()
    lhc_status = wbm.getLHCShortStatus()
    lhc_status.dump()

    cms_status = wbm.getCMSStatus()
    cms_status.dump()

if __name__=='__main__':
    main()
    
