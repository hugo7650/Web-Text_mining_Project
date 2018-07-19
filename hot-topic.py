import os

from Spiders import *
from Prasers import MainRanker

if __name__ == '__main__':

    # crawl pages from the given website
    spider = USnewsSpider()
    spider.start('./data/USnews')

    #ranker = MainRanker('./data/crawled', 29, True)
    #print(ranker.simple_BOW_rank())
    #print(ranker.BOW_stem_stop_rank())
    #print(ranker.POS_rank('NNP'))
    #print(ranker.ngrams_rank())
    #print(ranker.tfidf_rank(myhottest=30, stemmer_name='Snowball', para='"english"', to_remove=['student', 'school', 'safe', 'educ', 'teacher', 'learn', ]))

    
    print('Program ' + os.path.basename(__file__) + ' ends sucessfully')