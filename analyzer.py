from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import string
from scraper import MessageScraper
from variables import *


stop_words = set(stopwords.words('english'))


class MessageAnalyzer:

    def __init__(self, text):
        self.text = text

    def word_tokenize(self):
        all_tokens = [nltk.word_tokenize(message.translate(string.punctuation)) for message in self.text]
        return all_tokens

    def word_frequencies(self):
        tokens = []
        for message in self.text:
            tokens.extend(nltk.word_tokenize(message.translate(string.punctuation)))
        tokens = [w for w in tokens if w not in stop_words]
        freqs = nltk.FreqDist(tokens)
        return freqs

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


if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    my_texts, other_texts = scraper.all_messages()
    analyzer = MessageAnalyzer(other_texts)
    # analyzer.tokenize()
    freqs = analyzer.word_frequencies()
    for word, frequency in freqs.most_common(50):
        print(u'{}: {}'.format(word, frequency))
