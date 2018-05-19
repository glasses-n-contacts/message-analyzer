from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re
from textblob import TextBlob
from scraper import MessageScraper
from variables import *


stop_words = set(stopwords.words('english'))


class MessageAnalyzer:

    def __init__(self, text):
        self.text = text
        self.text_clf = None
        self.avg_polarity = 0

    def word_tokenize(self, extend_list=False):
        all_tokens = []
        ps = PorterStemmer()
        if extend_list:
            for message in self.text:
                # all_tokens.extend(message.split())
                all_tokens.extend(nltk.word_tokenize(message.translate(string.punctuation)))
            all_tokens = [ps.stem(w) for w in all_tokens if w not in stop_words]  # and w.isalpha()]
        else:
            all_tokens = [nltk.word_tokenize(message.translate(string.punctuation)) for message in self.text]
        return all_tokens

    def word_frequencies(self):
        tokens = self.word_tokenize(True)
        return nltk.FreqDist(tokens)

    def tokenize(self):
        # create the transform
        vec = CountVectorizer()
        # tokenize and build vocab
        vec.fit(self.text)
        # summarize
        print(vec.vocabulary_)
        # encode document
        vector = vec.transform(self.text)
        # summarize encoded vector
        print(vector.shape)
        print(type(vector))
        print(vector.toarray())

    @staticmethod
    def clean_message(message):
        """
        Utility function to clean text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", message).split())

    def sentiment_analysis(self):
        polarities = {}
        for message in self.text:
            analysis = TextBlob(self.clean_message(message))
            polarities[message] = analysis.sentiment.polarity
            self.avg_polarity += analysis.sentiment.polarity

        self.avg_polarity /= len(self.text)
        for message in polarities:
            print(polarities[message], message)
        return polarities

if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    my_texts, other_texts = scraper.all_messages()
    analyzer = MessageAnalyzer(other_texts)
    # analyzer.tokenize()
    # freqs = analyzer.word_frequencies()
    # for word, frequency in freqs.most_common(50):
    #     print(u'{}: {}'.format(word, frequency))
    analyzer.sentiment_analysis()
    print('Avg polarity')
    print(analyzer.avg_polarity)
