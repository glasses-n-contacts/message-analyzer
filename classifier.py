from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
import numpy as np


class TextClassifier:

    def __init__(self, training_data, targets, target_indices):
        self.training_data = training_data
        self.targets = targets
        self.target_indices = target_indices
        self.text_clf = None

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
