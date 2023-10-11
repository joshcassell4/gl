import requests 
from bs4 import BeautifulSoup
import nltk
from nltk import pos_tag, word_tokenize
# headers_Get = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate',
#         'DNT': '1',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1'
#     }

headers_Get = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,de-CH;q=0.4,es;q=0.3',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"109.0.1518.78"',
    'sec-ch-ua-full-version-list': '"Not_A Brand";v="99.0.0.0", "Microsoft Edge";v="109.0.1518.78", "Chromium";v="109.0.5414.120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
}

def google(q, start=None):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8' + (("&start=" + str(start)) if start != None else '')
    print(url)
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
 #   output = []
    # for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
    #     url = searchWrapper.find('a')["href"] 
    #     text = searchWrapper.find('a').text.strip()
    #     result = {'text': text, 'url': url}
    #     output.append(result)

    return soup

def googleurls(q, start=None):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8' + (("&start=" + str(start)) if start != None else '')
    print(url)
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    ad = soup.find_all('a')
    l = [x.attrs['href'] for x in ad if 'href' in x.attrs.keys() and 'data-jsarwt' in x.attrs.keys()]
    #l2 = [x.attrs['href'] for x in ad if 'href' in x.attrs.keys()]
    la = [x for x in ad if 'href' in x.attrs.keys() and 'data-jsarwt' in x.attrs.keys()]
    # de = [(lk.findNext('span').findNext('span').findNext('span').findNext('span').findNext('span').findNext('span')\
    #     .findNext('span').findNext('span').findNext('span').findNext('span')\
    #     .findNext('span').findNext('span').text, (lk.attrs['href'] if 'href' in lk.attrs.keys() else '')) for lk in ad]
    #m = list(map(lambda o: (pos_tag(word_tokenize(o[0])), o[0], o[1]), de))
    # output = []
    # for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
    #     url = searchWrapper.find('a')["href"] 
    #     text = searchWrapper.find('a').text.strip()
    #     result = {'text': text, 'url': url}
    #     output.append(result)
    #ko = [k for k in m if k[1] != '']
    return (soup.text,l,la)
    
def getposgoogleurls(x):
    j = googleurls(x)
    # j[1] is links from first page
    m = [(x,req(x)) for x in j[1]]
    # clean data and tokenize text
    i = [(x[0],nltk.word_tokenize(x[1].text.strip())) for x in m]
    # pos tag data
    o = [(x[0],nltk.pos_tag(x[1])) for x in i if len(x[1]) > 0]
    # seperate and clean types, 'omitted' is in list of words to remove
    # jj = [(z,[i for i in j if i[1] =='JJ' and i[0].lower() not in ['omitted']]) for z,j in o]
    vbg = [(z,[i[0] for i in j if i[1] =='VBG' and i[0].lower() not in []]) for z,j in o]
    jj = [(z,[i[0] for i in j if i[1] =='JJ' and i[0].lower() not in []]) for z,j in o]
    nn = [(z,[i[0] for i in j if i[1] =='NN' and i[0].lower() not in []]) for z,j in o]
    
    return (o,vbg,jj,nn)
    

def req(url):
    s = requests.Session()
    #q = '+'.join(q.split())
    #url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    soup = BeautifulSoup(r.text, "html.parser")
    #    output = []
    # for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
    #     url = searchWrapper.find('a')["href"] 
    #     text = searchWrapper.find('a').text.strip()
    #     result = {'text': text, 'url': url}
    #     output.append(result)

    return soup
#  ('https://www.tiktok.com/@greek_pepperoni/video/7164179101505604910',
#    ['v',
#     '|',
#     'inFor',
#     'view',
#     'inCreate',
#     'effectsAboutNewsroomContactCareersTikTok',
#     'more©',
#     'jacob¡161',
#     'commentsLog']),
#   ('https://www.tiktok.com/discover/if-i-disappear-like-who-cares-nobody-cares-man',
#    ['nobody',
#     'inFor',
#     'view',
#     'inCreate',
#     'effectsAboutNewsroomContactCareersTikTok',
#     'more©',
#     'nobody',
#     'nobody',
#     'man',
#     'cinema',
#     'film',
#     'movie',
#     'edit',
#     'movieedit',
#     'filmedit',
#     'marin.filmss218.5K3.8M',
#     'justthetruth',
#     'depression',
#     'realitycheck',
#     'realtalk',
#     'canada',
#     'just.the.truth_0100.1K184.7K',
#     'pov',
#     'foryourpage',
#     'anxiety',
#     'mentalhealth',
#     'realquotezzs4582.6Mmales_vibe284.2K329.6K',
#     'pain',
#     'foryoupage',
#     'fypage',
#     'imfine.202334.9K14.1K',
#     'man',
#     'sadedit',
#     'animevidos2688771.7K🖤‼️',
#     'foryoupage',
#     'arksian15.2KUsersifidissapearlikewhocaresreal151',
#     'viewsif_i_disapper_nobody_cares423',
#     'viewsnobodycaresifidisaper42',
#     'viewsifidissapearlikewhocarsman8',
#     'viewsfeelslikenobodycares2621',
#     'viewsifidisappearlikewhocares333',
#     'viewsitslikenobodycares4700',
#     'viewsifeellikenobodycares2039',
#     'viewsifidissapearnobodycaresmyan🙂😌🙂0',
#     'viewswhocaresifidie3718']),
