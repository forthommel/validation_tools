from wbmapi import api

def main():
    wbm = api.api()
    status = wbm.getLHCstatus()
    status.dump()

if __name__=='__main__':
    main()
    
