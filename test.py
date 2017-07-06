from wbmapi import api

def main():
    wbm = api.api()
    status = wbm.getLHCShortStatus()
    status.dump()

if __name__=='__main__':
    main()
    
