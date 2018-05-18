from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from analyzer import MessageAnalyzer
import numpy as np
import nltk
import string


class TextClassifier:

    def __init__(self, training_data, targets, target_indices):
        self.training_data = [message.translate(string.punctuation) for message in training_data]
        self.targets = targets
        self.target_indices = target_indices
        self.text_clf = None
        self.analyzer = MessageAnalyzer(self.training_data)
        freqs = self.analyzer.word_frequencies()
        self.most_common_words = freqs.most_common(100)
        #print(self.most_common_words)

    # bag of words model where every word is a feature name w/ value of True
    @staticmethod
    def word_features(words):
        return dict([(word, True) for word in words])

    def find_features(self, line):
        features = {}
        for word_feature, frequency in self.most_common_words:
            features[word_feature] = (word_feature in line.lower())
        return features

    def create_features(self):
        feature_sets = [(self.find_features(words), self.targets[self.target_indices[i]]) for i, words in enumerate(self.training_data)]
        print('Feature sets:')
        print(feature_sets)
        return feature_sets

    def train_nltk(self):
        features = self.create_features()
        self.text_clf = nltk.NaiveBayesClassifier.train(features)

    def test_nltk(self, test_data):
        test_features = [(self.word_features(words), self.targets[self.target_indices[i]]) for i, words in enumerate(test_data)]
        print("Classifier accuracy percent:", (nltk.classify.accuracy(self.text_clf, test_features)) * 100)
        self.text_clf.show_most_informative_features(15)

    def train(self, classifier_type='svm'):
        if classifier_type == 'svm':
            text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                             ('clf-svm',
                              SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42))])
        elif classifier_type == 'logistic':
            text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf', LogisticRegression())])
        else:  # default: naive bayes
            text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB())])
        self.text_clf = text_clf.fit(self.training_data, self.target_indices)

    def predict(self, predict_data, correct_values=None):
        predicted = self.text_clf.predict(predict_data)
        if correct_values:
            performance = np.mean(predicted == correct_values)
            print('Performance:')
            print(performance)
        print('--Predicted vs actual--')
        for i, predict in enumerate(predicted):
            print(self.targets[predict] + ', ' + self.targets[correct_values[i]])
        return predicted
