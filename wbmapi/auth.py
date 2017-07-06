import urllib, urllib2
import cookielib
import re
import HTMLParser
from os.path import expanduser, join

def getContent(url):
    cj = cookielib.MozillaCookieJar()
    cj.load(join(expanduser('~'), '.globus', 'ssocookie.txt'))
    headers = { "Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    req = urllib2.Request(url, None, headers)
    cookies_handler = urllib2.HTTPCookieProcessor(cj)
    redirect_handler = urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(cookies_handler, redirect_handler)

    res = opener.open(url).read()
    ret = re.search('<form .+? action="(.+?)">', res)
    if ret == None: raise Exception("error: The page doesn't have the form with adfs url, check 'User-agent' header")
    url = urllib2.unquote(ret.group(1))
    h = HTMLParser.HTMLParser()
    post_data_local = []
    re_post = re.compile('input type="hidden" name="([^"]*)" value="([^"]*)"')
    for match in re_post.finditer(res):
        post_data_local += [(match.group(1), h.unescape(match.group(2)))]
    if not post_data_local: raise Exception("error: The page doesn't have the form with security attributes, check 'User-agent' header")
    req = urllib2.Request(url)
    req.add_data(urllib.urlencode(post_data_local))
    r = opener.open(req)
    data = r.read()
    r.close()
    return data

