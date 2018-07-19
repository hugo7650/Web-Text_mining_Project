import nltk
from nltk.util import ngrams
from collections import defaultdict
import math
import re

class MainRanker():
    '''
        This class encapsulate all methods that ranks the topics.
        Beside the __init__() method, each other method name end with rank using the
    initialized filename to rank using the following method. And they all return a list
    of tuple (with keyword(str) and frequency(int)), started with the hottest topic.
        You can choose whether to plot the curve in initializing the object or runing the ranking.
    '''
    def __init__(self, filename_main, num_files, will_plot= False, hottest= 10):
        '''
            In the following method, they will actually open file in filename_main + str(i) + '.txt'
        to open the file.
        '''
        self.filename_main = filename_main
        self.num_files = num_files
        self.will_plot = will_plot
        self.hottest = hottest # specify the number of hottest topic returned by the ranker

    def extract_words(self, filename, will_lower= True)->list:
        '''
            This method returns a list of words from the specific file
            And each element is encoded in 'utf-8'
            will_lower argument specifies whether to change all uppercase char into lowercase
        '''
        # start with open the file
        to_return = []
        with open(filename, 'r', encoding='utf-8') as f:
            # preprocess the file
            raw_text = f.read().replace('\n', ' ').replace('\r', '')
            tokens = nltk.word_tokenize(raw_text)

            # extracting only words
            if (will_lower):
                temp = [w.lower() for w in tokens]
                tokens = temp # change to lower case
            temp = [w for w in tokens if w.isalpha()]
            tokens = temp
            # extract only alphabetical words
            to_return = tokens

        return to_return

    def simple_BOW_rank(self, mywill_plot= None, myhottest= None):
        '''
            This method applys simple bag of words procedure. And return hot topics
            And it didn't remove any stop words
        '''
        # prase the arguments for this method
        if mywill_plot == None:
            mywill_plot = self.will_plot
        if myhottest == None:
            myhottest = self.hottest

        # generate a frequency dictionary for all tokens
        freq_words = nltk.FreqDist()
        for i in range(self.num_files):
            # add samples in the file
            freq_words.update( self.extract_words(self.filename_main + str(i) + '.txt') )

        # sort the frequency list in decending order
        sorted_freq_words = sorted(freq_words.items(),\
                                    key = lambda k:k[1],\
                                    reverse = True
                                   )

        # display and return the answer
        print('Applying simple bag of words method with max frequency: ' + str(sorted_freq_words[0][1]))
        if mywill_plot:
            freq_words.plot(myhottest)

        return sorted_freq_words[:myhottest]

    def BOW_stem_stop_rank(self, mywill_plot= None, myhottest= None, stemmer_name= 'Porter'):
        '''
            This method applies bag-of-words and then stemming and stop words removal method
            And you can choose stemmer by specifying in the stemmer_name attribute. You have
        at least the followin choise:
                Porter
                Lancaster
        '''
        # prase the arguments for this method
        if mywill_plot == None:
            mywill_plot = self.will_plot
        if myhottest == None:
            myhottest = self.hottest

        # generate a frequency dictionary for all tokens not in stopwords
        # and use stemmer to stem the word in each document
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = eval('nltk.' + stemmer_name + 'Stemmer()')
        freq_words = nltk.FreqDist()
        for i in range(self.num_files):
            # add samples in the file
            words = self.extract_words(self.filename_main + str(i) + '.txt')
            temp = [w for w in words if (not w in stopwords)]
            freq_words.update([stemmer.stem(w) for w in temp])

        # sort the frequency list in decending order
        sorted_freq_words = sorted(freq_words.items(),\
                                    key = lambda k:k[1],\
                                    reverse = True
                                   )

        # display and return the answer
        print('Applying bag-of-words and stemming and stopword removal with max frequency: ' + str(sorted_freq_words[0][1]))
        if mywill_plot:
            freq_words.plot(myhottest)

        return sorted_freq_words[:myhottest]

    def POS_rank(self, focus, mywill_plot= None, myhottest= None):
        '''
            This method applies part-of-speech tagging approach
            focus: it should be a string and specifies which kind of tags this program should focus
        on, for example:
                NN: Noun, singular or mass
                NNP: Proper noun, singular
                NNS: Noun, plural
                NNPS: Proper noun, plural 
        '''
        # prase the arguments for this method
        if mywill_plot == None:
            mywill_plot = self.will_plot
        if myhottest == None:
            myhottest = self.hottest

        # generate a frequency dictionary for all tokens not in stopwords
        # and use stemmer to stem the word in each document
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = eval('nltk.PorterStemmer()')
        freq_words = nltk.FreqDist()
        for i in range(self.num_files):
            # add samples in the file
            words = self.extract_words(self.filename_main + str(i) + '.txt', False)
            temp = [w for w in words if (not w in stopwords)]
            stemmed = [stemmer.stem(w) for w in temp]
            with_tags = nltk.pos_tag(stemmed)
            # select words with specific tag
            selected = [w for (w,t) in with_tags if t == focus]
            freq_words.update(selected)

        # sort the frequency list in decending order
        sorted_freq_words = sorted(freq_words.items(),\
                                    key = lambda k:k[1],\
                                    reverse = True
                                   )

        # display and return the answer
        print('Applying POS ranking with max frequency: ' + str(sorted_freq_words[0][1]))
        if mywill_plot:
            freq_words.plot(myhottest)

        return sorted_freq_words[:myhottest]

    def ngrams_rank(self, n= 2, mywill_plot= None, myhottest= None, stemmer_name= 'Porter'):
        '''
            Applying ngrams method to extract tokens and then count, sort to find the hottest topic.
            The argurment n means the n-grams, when n=2 (also is a default value) all tokens will be
        unigrams and bigrams (no intermediate)
        '''
        # prase the arguments for this method
        if mywill_plot == None:
            mywill_plot = self.will_plot
        if myhottest == None:
            myhottest = self.hottest
        
        # generate a frequency dictionary for all tokens not in stopwords
        # and use stemmer to stem the word in each document
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = eval('nltk.LancasterStemmer()')
        freq_words = nltk.FreqDist()
        for i in range(self.num_files):
            # add samples in the file
            words = self.extract_words(self.filename_main + str(i) + '.txt')
            words += ngrams(words, n)
            temp = [w for w in words if (not w in stopwords)]
            stemmed = [stemmer.stem(w) for w in temp]
            with_tags = nltk.pos_tag(stemmed)
            # select words with specific tag
            selected = [w for (w,t) in with_tags if t.startwith('N')]
            freq_words.update(selected)

        # sort the frequency list in decending order
        sorted_freq_words = sorted(freq_words.items(),\
                                    key = lambda k:k[1],\
                                    reverse = True
                                   )

        # display and return the answer
        print('Applying ngrams ranking with max frequency: ' + str(sorted_freq_words[0][1]))
        if mywill_plot:
            freq_words.plot(myhottest)

        return sorted_freq_words[:myhottest]

    def tfidf_rank(self, mywill_plot= None, myhottest= None, stemmer_name= 'Porter', para= None, to_remove= []):
        '''
            Based on the previous counting method, adding tf-idf method to rank the importance of words
            to_remove: you specifies words that you expelicitly don't want to be counted, they does not include stop words
        '''
        # prase the arguments for this method
        if mywill_plot == None:
            mywill_plot = self.will_plot
        if myhottest == None:
            myhottest = self.hottest

        # generate a frequency dictionary for all tokens not in stopwords
        # and use stemmer to stem the word in each document
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = eval('nltk.' + stemmer_name + 'Stemmer(' +  para + ')')
        freq_words = nltk.FreqDist()
        # use for count the idf of each term
        word_idf = defaultdict(lambda: 0)
        for i in range(self.num_files):
            # add samples in the file
            words = self.extract_words(self.filename_main + str(i) + '.txt')

            temp = [w for w in words if (not w in stopwords)]
            to_add = [stemmer.stem(w) for w in temp]
            to_add = [w for w in to_add if not w in to_remove]
            word_set = set(to_add)
            freq_words.update(to_add)

            # set the idf
            for word in word_set:
                word_idf[word] += 1
                
        # Calculate the idf of each word
        for word in freq_words.keys():
            word_idf[word] = math.log(self.num_files / float(1 + word_idf[word]))

        # update frequency list with tf idf
        for word in freq_words.keys():
            freq_words[word] *= word_idf[word]

        # sort the frequency list in decending order
        sorted_freq_words = sorted(freq_words.items(),\
                                    key = lambda k:k[1],\
                                    reverse = True
                                   )

        # display and return the answer
        print('Applying bag-of-words and stemming and stopword removal with max frequency: ' + str(sorted_freq_words[0][1]))
        if mywill_plot:
            freq_words.plot(myhottest)

        return sorted_freq_words[:myhottest]