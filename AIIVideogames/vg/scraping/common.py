import urllib2
from bs4 import BeautifulSoup


def open_link(url):
    f = urllib2.urlopen(url)
    html_doc = f.read()
    f.close()

    return BeautifulSoup(html_doc, 'html.parser')


def open_link_cookies(url, cookies):
    f = urllib2.build_opener()
    
    cookies_str = ''
    for name,value in cookies.items():
        cookies_str += (name+'='+value+';')
        
    f.addheaders.append(('Cookie', cookies_str))
    f.addheaders.append(('Accept-Language', 'es-ES,es;q=0.9'))
    
    html_doc = f.open(url).read()
    f.close()

    return BeautifulSoup(html_doc, 'html.parser')