# coding: utf-8
# BeautifulSoup Demo

#import packages
import urllib.request
import json
from lxml import etree
import threading

"""
    This is a tool file that helps the main program to craw data from the sepcific website.
    And the tools are aimed for this assignment. It is not garanteed that they can be applied
to other purposes.
"""

class DataGovSpider():
    '''
        This object process the crawling jobs, in specific for this assignment.
    '''
    def __init__(self, num_pages= 10):
        # Setup urls for each page
        initial_url = 'https://www.data.gov/education/page/'
        self.start_urls = [(initial_url + str(i)) for i in range(1, num_pages)]
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.68 Safari/537.36'}
        # use pages attribute to record how many file has been written, in order to sepcify the
        # exact file name.
        self.pages = 0
        self.xpath = '//*[@id="main"]/div[2]/article'

    def start(self, filename_main= './data/crawled'):
        '''
            In this method it will invoke the sub macro to write each page into each
        following files, with file name: filename_main + str(i) + '.txt'
            And this method will return the number pages it wrote to document, index
        start from 0 end (include) at pages-1.
        '''
        for tbl_url in self.start_urls:
            print('crawling from table of content')
            req = urllib.request.Request(url=tbl_url,headers=self.headers)
            try:
                data = urllib.request.urlopen(req).read()
                treedata = etree.HTML(data)
                urls = treedata.xpath('//*[@id="main"]/div[2]/article/header/h2/a/@href')

                tpool=[]
                for url in urls:
                    url='https://www.data.gov/education/'+url
                    t=threading.Thread(target=extract_from_page,args=(url, self.xpath, filename_main,))
                    tpool.append(t)
                    t.start()
                for t in tpool:
                    t.join()

                print("crawl from one main page, move to the next table of pages...")
            except: continue

        return self.pages

class USnewsSpider():
    '''
        This object process the crawling jobs, in specific for this assignment.
    '''
    def __init__(self, num_pages= 1000):
        # Setup urls for each page
        initial_url = 'https://www.usnews.com/topics/subjects/k_12_education?offset='
        self.start_urls = [(initial_url + str(i) + '&renderer=json') for i in range(0, num_pages,10)]
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.68 Safari/537.36','Referer': 'https://www.usnews.com/topics/subjects/k_12_education','Cookie': 'akacd_www=2177452799~rv=70~id=a685edab78689288983e0930f489ef8f; s_cc=true; s_fid=683CD3DA45EA94BF-064C7333AA4EF013; ak_bmsc=378C63BB70F6A3AA683A031A06A6155917C60B1D7E7100009109525BE736C947~pl99dtjX0d3bBpxt4lOpPDjRnh/H/6aFh7NkU2hJl4Q6sI4YwQLmh+9xOEVBvIjdgF3UlgRwprmlRVl3fzFxfMfqIAjS3CF/b8/0PU3BM9zU5sFzsedwYjVw07SmXBIlrE6nqlBVTyILAwreJT43chzuOyseZak/OUHqZg/V3Sq7C+NZod9izygb8M7fh9+B3nVT3fM3ITMx0dF/GZX7bXk3mb2+H7988heArAriv/dhw=; s_sq=%5B%5BB%5D%5D; JSESSIONID=FB845546D48DA3F2E34CB9860644AA3B; bm_sv=742B7A18A60B689BAAF7E10685DDE2F8~w9B4LppRedGuQPwCahR642gP0SiOJe4PggytgIKI7cipMI+c1Y0FQ/1zKJes4lIUvqKE53yRQkL0pxGeTbH0nplLQUxhm6dJrXzlNR8gwHW0sn2Bbifh3gwEgPvzMSes35BW27BgPby2o/U7UItnof4jQyBZOpUZyjbp6zegTEk=; utag_main=v_id:0164b18c7a56000d4533ba37d27703072003506a00bd0$_sn:4$_ss:0$_st:1532111805992$_pn:3%3Bexp-session$ses_id:1532109940545%3Bexp-session'}
        # use pages attribute to record how many file has been written, in order to sepcify the
        # exact file name.
        self.pages = 0
        self.xpath = '//*[@id="app"]/div/div/div[2]/div[3]/div[1]'

    def start(self, filename_main= './data/crawled'):
        '''
            In this method it will invoke the sub macro to write each page into each
        following files, with file name: filename_main + str(i) + '.txt'
            And this method will return the number pages it wrote to document, index
        start from 0 end (include) at pages-1.
        '''
        for tbl_url in self.start_urls:
            print('crawling from table of content')
            req = urllib.request.Request(url=tbl_url,headers=self.headers)
            data = json.loads(urllib.request.urlopen(req).read())

            urls=[]
            for j in data['stories']:
                urls.append(j['permalink'])

            tpool=[]
            for url in urls:
                t=threading.Thread(target=extract_from_page,args=(self, url, self.xpath, filename_main,))
                tpool.append(t)
                t.start()
            for t in tpool:
                t.join()

            print("crawl from one main page, move to the next table of pages...")

        return self.pages

class TheGuardianSpider():
    '''
        This object process the crawling jobs, in specific for this assignment.
    '''
    def __init__(self, num_pages= 10):
        # Setup urls for each page
        initial_url = 'https://www.theguardian.com/education'
        self.start_urls = [(initial_url)]
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.68 Safari/537.36'}
        # use pages attribute to record how many file has been written, in order to sepcify the
        # exact file name.
        self.pages = 0
        self.xpath = '//*[@id="article"]/div[2]/div/div[1]/div/p'

    def start(self, filename_main= './data/crawled'):
        '''
            In this method it will invoke the sub macro to write each page into each
        following files, with file name: filename_main + str(i) + '.txt'
            And this method will return the number pages it wrote to document, index
        start from 0 end (include) at pages-1.
        '''
        for tbl_url in self.start_urls:
            print('crawling from table of content')
            req = urllib.request.Request(url=tbl_url,headers=self.headers)
            data = urllib.request.urlopen(req).read().decode('utf-8')
            treedata = etree.HTML(data)
            idlist = ['education', 'news', 'students', 'in-depth', 'teacher-network', 'global-view', 'opinion']
            urls = []
            for i in idlist:
                urls+=treedata.xpath('//*[@id="'+i+'"]/div/div[2]/div[1]/ul/li/div/div/a/@href')

            tpool=[]
            for url in urls:
                t=threading.Thread(target=extract_from_page,args=(url, self.xpath, filename_main,))
                tpool.append(t)
                t.start()
            for t in tpool:
                t.join()

            print("crawl from one main page, move to the next table of pages...")

        return self.pages

def extract_from_page(self, url, xpath, filename_main):
    '''
        By finding the html file inside the article, then write to a txt file.
    '''
    if url == '':
        return False
    req = urllib.request.Request(url=url,headers=self.headers)
    data = urllib.request.urlopen(req).read().decode('utf-8')
    treedata = etree.HTML(data)
    article = treedata.xpath(xpath)
    if article == []:
        return False
    print('Acquire page and prepare to write to file ' + str(self.pages))
    #print(article)
    print('\tthrough url: ' + url)

    with open(filename_main + str(self.pages) + '.txt', 'w') as f:
        for i in article:
            f.write(i.xpath('string(.)'))
        self.pages += 1
    print('Done crawling from one page...')
    return True
