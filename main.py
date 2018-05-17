from scraper import MessageScraper
from analyzer import MessageAnalyzer
from classifier import TextClassifier
from variables import *


if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    my_texts, other_texts = scraper.all_messages()
    slice_index = int(len(my_texts) * 0.9)
    train_my_texts = my_texts[:slice_index]
    train_other_texts = other_texts[:slice_index]
    test_my_texts = my_texts[slice_index:]
    test_other_texts = other_texts[slice_index:]

    target_indices = ([0] * len(train_my_texts)) + ([1] * len(train_other_texts))
    training_data = train_my_texts + train_other_texts
    test_data = test_my_texts + test_other_texts

    print(training_data)
    print(test_data)

    test_target_indices = ([0] * len(test_my_texts)) + ([1] * len(test_other_texts))
    targets = ['Lucy', 'Bill']
    classifier = TextClassifier(training_data, targets, target_indices)
    classifier.train('svm')
    classifier.predict(test_data, test_target_indices)
