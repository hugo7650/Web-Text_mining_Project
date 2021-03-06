from splinter import Browser
from selenium.webdriver.common.keys import Keys
from html2text import HTML2Text
import time

"""
    This is a tool file that helps the main program to craw data from the sepcific website.
    And the tools are aimed for this assignment. It is not garanteed that they can be applied
to other purposes.
"""

class DataGovSpider():
    '''
        This object process the crawling jobs, in specific for this assignment.
    '''
    def __init__(self, num_pages= 40):
        # Setup urls for each page
        initial_url = 'https://www.data.gov/education/page/'
        self.start_urls = [(initial_url + str(i) + '/') for i in range(1, num_pages)]
        self.browser = Browser('chrome')
        # use pages attribute to record how many file has been written, in order to sepcify the
        # exact file name.
        self.pages = 0

    def start(self, filename_main= './data/crawled'):
        '''
            In this method it will invoke the sub macro to write each page into each
        following files, with file name: filename_main + str(i) + '.txt'
            And this method will return the number pages it wrote to document, index
        start from 0 end (include) at pages-1.
        '''
        xpath_root = '//*[@id="main"]/div[2]/article'
        xpath_secondary = '/header/h2/a'
        for tbl_url in self.start_urls:
            print('crawling from table of content')
            self.browser.visit(tbl_url)
            time.sleep(1)

            urls = []
            # get the number of links in the table of content page
            num_links = len(self.browser.find_by_xpath(xpath_root))
            for i in range(1, num_links+1):
                url = self.browser\
                    .find_by_xpath(xpath_root + '[' + str(i) + ']' + xpath_secondary)
                # store the url for each page in case changing the browser behavior
                if url == []:
                    print('no url found in this tag')
                else:
                    urls.append(url['href'])

            # invoking each function to read and extract the texts
            for url in urls:
                self.extract_from_page(url, filename_main)

            print("crawl from one main page, move to the next table of pages...")

        return self.pages

    def extract_from_page(self, url, filename_main):
        '''
            By finding the html file inside the article, then write to a txt file.
        '''
        mybrowser = Browser('chrome')
        mybrowser.visit(url)# + '?printable=1')
        article = mybrowser.find_by_xpath('//*[@id="main"]/div[2]/article')
        if article == []:
            mybrowser.quit()
            return
        print('acquire page and prepare to write to file ' + str(self.pages))
        print('through url: ' + url)

        # setup the html2text object
        h2t = HTML2Text()
        h2t.ignore_links = True
        h2t.bypass_tables = False
        with open(filename_main + str(self.pages) + '.txt', 'w', encoding='utf-8') as f:
            f.write(h2t.handle(article.value))
            self.pages += 1
        mybrowser.quit()
        time.sleep(2)

class USnewsSpider():
    '''
        This object process the crawling jobs, in specific for this assignment.
    '''
    def __init__(self, num_pages= 100):
        # Setup urls for each page
        self.initial_url = 'https://www.usnews.com/topics/subjects/k_12_education'
        self.num_pages = num_pages
        self.browser = Browser('chrome')
        # use pages attribute to record how many file has been written, in order to sepcify the
        # exact file name.
        self.pages = 0

    def start(self, filename_main= './data/crawled'):
        '''
            In this method it will invoke the sub macro to write each page into each
        following files, with file name: filename_main + str(i) + '.txt'
            And this method will return the number pages it wrote to document, index
        start from 0 end (include) at pages-1.
        '''
        xpath_root = '//*[@id="00000142-9228-d1f0-a5c6-b2fdbbdb0000"]/div/div'
        xpath_secondary = '/div[1]/h3/a'
        self.browser.visit(self.initial_url)

        # This method is aimed at need to scroll down the page in order to acquire more pieces
        div_index = 1
        pages_crawled = 0
        items = self.browser.find_by_xpath(xpath_root)
        while pages_crawled < self.num_pages:
            # Check if it is needed to scroll down the pages or scroll down the page
            if len(items) < div_index:
                print("scrolling down the page...")
                active_web_element = self.browser.driver.switch_to_active_element()
                active_web_element.send_keys(Keys.PAGE_DOWN)
                active_web_element.send_keys(Keys.PAGE_DOWN)
                time.sleep(5)
                items = self.browser.find_by_xpath(xpath_root)
                continue

            # Now assume the content is enough
            tag_a = self.browser.find_by_xpath(
                xpath_root + '[' + str(div_index) + ']' + xpath_secondary)
            if (not tag_a == []):
                self.extract_from_page(tag_a["href"], filename_main)
            # No matter the extracting is sucessfull, move to the nex tag.
            div_index += 1

        return self.pages

    def extract_from_page(self, url, filename_main)->bool:
        '''
            By finding the html file inside the article, then write to a txt file.
        '''
        mybrowser = Browser('chrome')
        mybrowser.visit(url)# + '?printable=1')
        article = mybrowser.find_by_xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]')
        if article == []:
            mybrowser.quit()
            return False
        print('Acquire page and prepare to write to file ' + str(self.pages))
        print('\tthrough url: ' + url)

        # setup the html2text object
        h2t = HTML2Text()
        h2t.ignore_links = True
        h2t.bypass_tables = False
        with open(filename_main + str(self.pages) + '.txt', 'w', encoding='utf-8') as f:
            f.write(h2t.handle(article.value))
            self.pages += 1
        mybrowser.quit()
        print('Done crawling from one page...')
        time.sleep(2)
        return True