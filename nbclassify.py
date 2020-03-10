import os
import json
import math
import sys
import random


def calculate_test_spam_probability_log(all_test_file_tokens, spam_dict, prob_spam):
    # Use log -> normal naive bayes causes underflow.
    all_spam_probabilities = []
    log_value = math.log10(prob_spam)
    for test_file_tokens in all_test_file_tokens:
        log_adder = log_value
        for test_file_token in test_file_tokens:
            conditional_probability = spam_dict.get(test_file_token)
            if conditional_probability:
                log_adder = log_adder + math.log10(conditional_probability)
        all_spam_probabilities.append(log_adder)
    return all_spam_probabilities


def calculate_test_ham_probability_log(all_test_file_tokens, ham_dict, prob_ham):
    # Use log -> normal naive bayes causes underflow.
    all_ham_probabilities = []
    log_value = math.log10(prob_ham)
    for test_file_tokens in all_test_file_tokens:
        log_adder = log_value
        for test_file_token in test_file_tokens:
            conditional_probability = ham_dict.get(test_file_token)
            if conditional_probability:
                log_adder = log_adder + math.log10(conditional_probability)
        all_ham_probabilities.append(log_adder)
    return all_ham_probabilities


def calculate_test_ham_probability(all_test_file_tokens, ham_dict, prob_ham):
    all_ham_probabilities = []
    for test_file_tokens in all_test_file_tokens:
        multiply_value = prob_ham
        for test_file_token in test_file_tokens:
            conditional_probability = ham_dict.get(test_file_token)
            if conditional_probability:
                multiply_value = multiply_value * conditional_probability
        all_ham_probabilities.append(multiply_value)
    return all_ham_probabilities


def calculate_test_spam_probability(all_test_file_tokens, spam_dict, prob_spam):
    all_spam_probabilities = []
    for test_file_tokens in all_test_file_tokens:
        multiply_value = prob_spam
        for test_file_token in test_file_tokens:
            conditional_probability = spam_dict.get(test_file_token)
            if conditional_probability:
                multiply_value = multiply_value * conditional_probability
        all_spam_probabilities.append(multiply_value)
    return all_spam_probabilities


def read_files(test_files):
    """
    :param test_files:
    :return: all tokens from all files
    """
    all_tokens = []
    for test_file in test_files:
        with open(test_file, "r", encoding="latin1") as test_file_ptr:
            test_tokens = test_file_ptr.read().split()
            all_tokens.append(test_tokens)
    return all_tokens


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
    test_files_set = []
    base_directory = 'C:\\Users\\Samuktha\\Documents\\USC\\CSCI 544 Applied Natural Language Processing\\Spam or Ham'
    dev_data_path = os.path.join(base_directory, 'dev')  # local
    find_files(test_files_set, dirs=[dev_data_path], extensions=['.txt'])
    complete_tokens = read_files(test_files_set)
    with open('nbmodel.txt', "r", encoding="latin1") as read_ptr:
        model = json.load(read_ptr)
    probability_ham = model['prob_ham']
    probability_spam = model['prob_spam']
    ham_dictionary = model['ham_dict']
    spam_dictionary = model['spam_dict']
    ham_probabilities = calculate_test_ham_probability_log(complete_tokens, ham_dictionary, probability_ham)
    spam_probabilities = calculate_test_spam_probability_log(complete_tokens, spam_dictionary, probability_spam)
    compare_probabilities = zip(test_files_set, ham_probabilities, spam_probabilities)
    with open("nboutput.txt", "w") as write_ptr:
        for directory, p_ham, p_spam in compare_probabilities:
            if p_ham > p_spam:
                write_ptr.write("ham" + " " + directory + "\n")
            elif p_spam > p_ham:
                write_ptr.write("spam" + " " + directory + "\n")
            else:
                if random.randint(0, 1):
                    write_ptr.write("spam" + " " + directory + "\n")
                else:
                    write_ptr.write("ham" + " " + directory + "\n")






