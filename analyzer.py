from sklearn.feature_extraction.text import CountVectorizer
import nltk
from scraper import MessageScraper
from variables import *


class MessageAnalyzer:

    def __init__(self, text):
        self.text = text

    def word_tokenize(self):
        all_tokens = [nltk.word_tokenize(message) for message in self.text]
        return all_tokens

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
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO)
    my_texts, other_texts = scraper.get_texts()
    analyzer = MessageAnalyzer(my_texts)
    analyzer.tokenize()
    tokens = analyzer.word_tokenize()
    print(tokens)
