from scraper import MessageScraper
from analyzer import MessageAnalyzer
from classifier import TextClassifier
from variables import *


if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    my_texts, other_texts = scraper.all_messages()
    print('my_texts:')
    print(my_texts)

    print('other_texts:')
    print(other_texts)
    print('----')

    slice_my_index = int(len(my_texts) * 0.8)
    slice_other_index = int(len(other_texts) * 0.8)

    train_my_texts = my_texts[:slice_my_index]
    train_other_texts = other_texts[:slice_other_index]

    test_my_texts = my_texts[slice_my_index:]
    test_other_texts = other_texts[slice_other_index:]

    print('Test my texts:')
    print(test_my_texts)

    print('Test other texts:')
    print(test_other_texts)
    print('----')

    target_indices = ([0] * len(train_my_texts)) + ([1] * len(train_other_texts))
    test_target_indices = ([0] * len(test_my_texts)) + ([1] * len(test_other_texts))

    training_data = train_my_texts + train_other_texts
    test_data = test_my_texts + test_other_texts

    print('Train my texts:')
    print(train_my_texts)

    print('Train other texts:')
    print(train_other_texts)

    print('----')
    targets = ['Lucy', 'Bill']
    classifier = TextClassifier(training_data, targets, target_indices)
    classifier.train('svm')
    classifier.predict(test_data, test_target_indices)
