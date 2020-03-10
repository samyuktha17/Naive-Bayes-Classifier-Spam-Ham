import os
from collections import Counter
import json
import sys


def ham_conditional_probabilities(sum_count_ham, V, unique_tokens, ham_token_list):
    """
    :param sum_count_ham: total no of words in class ham
    :param V: smoothing factor -> vocabulary size
    :param unique_tokens: distinct tokens
    :param ham_token_list: ham tokens
    :return: dictionary with distinct token as key and conditional probability as value
    """
    ham_dict = {}
    smoothing_denominator = V + sum_count_ham  # one smoothing
    lookup_count_of_word_in_ham_content = Counter(ham_token_list)
    for unique_token in unique_tokens:
        smoothing_numerator = 1
        count_of_unique_token = lookup_count_of_word_in_ham_content.get(unique_token)
        if count_of_unique_token:
            smoothing_numerator += count_of_unique_token
        ham_dict[unique_token] = smoothing_numerator / smoothing_denominator
    return ham_dict


def spam_conditional_probabilities(sum_count_spam, V, unique_tokens, spam_token_list):
    """
    :param sum_count_spam: total no of words in class spam
    :param V: smoothing factor -> vocabulary size
    :param unique_tokens: distinct tokens
    :param spam_token_list: spam tokens
    :return: dictionary with distinct token as key and conditional probability as value
    """
    spam_dict = {}
    smoothing_denominator = V + sum_count_spam  # one smoothing
    lookup_count_of_word_in_spam_content = Counter(spam_token_list)
    for unique_token in unique_tokens:
        smoothing_numerator = 1
        count_of_unique_token = lookup_count_of_word_in_spam_content.get(unique_token)
        if count_of_unique_token:
            smoothing_numerator += count_of_unique_token
        spam_dict[unique_token] = smoothing_numerator / smoothing_denominator
    return spam_dict


def calculate_probabilities_ham_spam(ham_token_list, m):
    """
    :param ham_token_list: ham tokens
    :param m: total size of corpus
    :return: p(ham), p(spam), total no of words in class ham, total no of words in class spam
    """
    sum_count_ham = len(ham_token_list)
    sum_count_spam = m - sum_count_ham
    prob_spam = sum_count_spam / m
    prob_ham = sum_count_ham / m
    return prob_ham, prob_spam, sum_count_ham, sum_count_spam


def get_unique_tokens(ham_token_list, spam_token_list):
    """
    :param ham_token_list: ham tokens
    :param spam_token_list: spam tokens
    :return: vocabulary size, unique tokens (vocabulary), m -> total token size
    """
    corpus_tokens = ham_token_list + spam_token_list
    m = len(corpus_tokens)
    unique_tokens = set(corpus_tokens)
    return calculate_vocabulary_size(unique_tokens=unique_tokens), unique_tokens, m


def calculate_vocabulary_size(unique_tokens):
    """
    :param unique_tokens: set of tokens
    :return: vocabulary_size
    """
    return len(unique_tokens)


def token_maker(ham_text_combined, spam_text_combined):
    """
    :param ham_text_combined:  ham corpus
    :param spam_text_combined: spam corpus
    :return: ham tokens, spam tokens split by white space
    """
    return ham_text_combined.split(), spam_text_combined.split()


def read_files(hams, spams):
    """
    :param hams: ham file directory list
    :param spams: spam file directory list
    :return: list of strings - content of ham files and spam files
    """
    ham_content_text = " "
    for ham in hams:
        with open(ham, "r", encoding="latin1") as ham_file_ptr:
            ham_content_text += ham_file_ptr.read()
    spam_content_text = ""
    for spam in spams:
        with open(spam, "r", encoding="latin1") as spam_file_ptr:
            spam_content_text += spam_file_ptr.read()
    return ham_content_text, spam_content_text


def separate_ham_spam(all_file_paths):
    """
    :param all_file_paths: set of all file paths
    :return: ham txt files, spam txt files
    """
    ham_path = []
    spam_path = []
    for path in all_file_paths:
        pieces = path.split('\\')
        if pieces[-2] == 'ham':
            
            ham_path.append(path)
        else:
            spam_path.append(path)
    return ham_path, spam_path


def find_files(files, dirs, extensions):
    """
    :param files: list to hold paths
    :param dirs: initial base directory
    :param extensions: searches '.txt' extension
    :return: None
    """
    new_dirs = []
    for d in dirs:
        try:
            new_dirs += [os.path.join(d, f) for f in os.listdir(d)]
        except OSError:
            if os.path.splitext(d)[1] in extensions:
                files.append(d)

    if new_dirs:
        find_files(files, new_dirs, extensions)
    else:
        return


if __name__ == '__main__':
    files_set = []
    # local
    data_path = 'C:\\Users\\Samuktha\\Documents\\USC\\CSCI 544 Applied Natural Language Processing\\Spam or Ham'
    train_data_path = os.path.join(data_path, 'train10')
    # base_directory = sys.argv[0]
    # train_data_path = os.path.join(base_directory, 'train')
    find_files(files_set, dirs=[train_data_path], extensions=['.txt'])
    ham_file_paths, spam_file_paths = separate_ham_spam(files_set)
    ham_content, spam_content = read_files(ham_file_paths, spam_file_paths)

    ham_tokens, spam_tokens = token_maker(ham_content, spam_content)
    vocabulary_size, distinct_tokens, total_size = get_unique_tokens(ham_tokens, spam_tokens)

    probability_ham, probability_spam, ham_size, spam_size = calculate_probabilities_ham_spam(ham_tokens, total_size)
    ham_dictionary = ham_conditional_probabilities(ham_size, vocabulary_size, distinct_tokens, ham_tokens)
    spam_dictionary = spam_conditional_probabilities(spam_size, vocabulary_size, distinct_tokens, spam_tokens)

    model = dict(spam_dict=spam_dictionary, ham_dict=ham_dictionary, prob_ham=probability_ham,
                 prob_spam=probability_spam)

    with open('nbmodel.txt', "w") as write_ptr:
        json.dump(model, write_ptr)
    print("dumped")
  