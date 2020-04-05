import math
from datetime import datetime

import nltk
import openpyxl

from src.pre_processing import Preprocessing


def import_stop_list(path):
    # a stop-word file is opened and parsed to be saved as a list
    stop_file = open(path, "r")
    stop_list = stop_file.read().split("\n")
    stop_file.close()
    return stop_list


def process_query(query):
    print()


def pre_processing(stop_list_path, string):

    stop_list = import_stop_list(stop_list_path)

    # creating a object of the Preprocessing class
    _pre_processing = Preprocessing()

    # a stop-list is assigned to attribute of class
    _pre_processing.stop_word = stop_list

    # a string of file was passed to tokenizer that returns a list of tokens
    tokens = _pre_processing.tokenizer(string)

    # a set of lemma is returned as {lemma: tf}
    lemma_set = _pre_processing.lemmatizer(tokens)

    # list of stop-word is unusable, so it is cleared
    stop_list.clear()

    # list of tokens is unusable, so it is cleared
    tokens.clear()

    return lemma_set


def prepare_bag_of_words(_lemmas_set,  _bag_of_words):
    # lemma_set for i-th doc and keys() gives lemmas in the set
    for lem in _lemmas_set.keys():
        try:
            # a set was used because of its speed due to hashing which costs O(1)
            # otherwise a list would cost O(n) in searching the lemma from bag-of-words
            # because to restrict the repetitive lemmas from entire corpus
            _bag_of_words[lem] = 0
        except KeyError:
            # if lemma exists, it would throw KeyError and would do nothing
            pass
    return _bag_of_words


def process_corpora():

    # two important data-structures are initialized
    _bag_of_words = {}
    _lemmas = []

    print(datetime.now().strftime("%H:%M:%S") + ": pre-processing initiating...")

    # a loop is run to iterate over the entire corpus of length 56
    for i in range(0, 56):

        file_name = "../resource/trump-speeches/speech_" + str(i) + ".txt"
        file = open(file_name, "r")
        # skips the title
        file.readline()

        # lemma_set = {lemma: tf}
        lemma_set = pre_processing("../resource/stopword-list.txt", file.read())

        # copy() deep copies the set into lemma list
        _lemmas.append(lemma_set.copy())

        # since tokens are created, file is now closed
        file.close()

        # since a deep-copy of lemma_set was appended and not its address was passed
        # this list can be cleared without effecting the one in lemmas
        lemma_set.clear()

        # _lemmas[i] gives a lemma_set for i-th doc
        _bag_of_words = prepare_bag_of_words(_lemmas[i], _bag_of_words)

    print(datetime.now().strftime("%H:%M:%S") + ": pre-processing completed")

    return _bag_of_words, _lemmas


def calculate_doc_score(_bag_of_words, _len_of_bag_of_words, _lemmas, _sheet):

    print(datetime.now().strftime("%H:%M:%S") + ": starting tf-idf calculations...")

    for i in range(2, _len_of_bag_of_words + 2):
        word = _sheet.cell(i, 1).value = _bag_of_words[i - 2]
        df = 0

        for doc_id in range(0, 56):
            tf = _lemmas[doc_id].get(word)
            if tf is None:
                # when doc not have word, tf will be 0
                _sheet.cell(i, doc_id + 2).value = 0
            else:
                _sheet.cell(i, doc_id + 2).value = tf
                df += 1

        _sheet.cell(i, 59).value = df
        idf = float(format(math.log10(56 / df), '.5f'))
        _sheet.cell(i, 60).value = idf

        for doc_id in range(0, 56):
            tf = float(_sheet.cell(i, doc_id + 2).value)
            value = float(format(tf * idf, '.5f'))
            _sheet.cell(i, doc_id + 61).value = value

    print(datetime.now().strftime("%H:%M:%S") + ": tf-idf calculations completed")

    return _sheet


def prepare_sheet(_sheet):
    # total columns to be created: 1+56+1+1+1+56+1 = 117
    # <creating-columns>

    _sheet.cell(1, 1).value = "words"

    for i in range(2, 58):
        _sheet.cell(1, i).value = "d.tf:" + str(i - 2)

    _sheet.cell(1, 58).value = "q.tf"
    _sheet.cell(1, 59).value = "df"
    _sheet.cell(1, 60).value = "idf"

    for i in range(61, 117):
        _sheet.cell(1, i).value = "d.val:" + str(i - 61)
    _sheet.cell(1, 117).value = "q.val"

    # </creating-columns>

    return _sheet


def create_sheet(_sheet):
    # caches are used so that the next time program runs
    # no doc pre-processing is done which saves a lot of time
    # and provides readability of data after the program has been closed
    # here cache is a file named tf-idf.xlsx

    print(datetime.now().strftime("%H:%M:%S") + ": cache not found")
    print(datetime.now().strftime("%H:%M:%S") + ": preparing cache...")

    _sheet = prepare_sheet(_sheet)

    # a lemmas-list is in memory which has sets for each document
    # each set has a key which is a lemma and a value against the key
    # as term-frequency
    # e.g: [{trump: 57, ...}, {trump:1, ...}, ...]
    bag_of_words, lemmas = process_corpora()

    # length of bag-of-words is saved for future use
    len_of_bag_of_words = len(bag_of_words)
    print(datetime.now().strftime("%H:%M:%S") + ": Length of Bag-of-Words: " + str(len_of_bag_of_words))

    # keys from bag-of-words were converted into a list
    # so that keys() would not be called multiple times in the calculate_tf_idf
    bag_of_words = list(bag_of_words.keys())

    _sheet = calculate_doc_score(bag_of_words, len_of_bag_of_words, lemmas, _sheet)

    # since bag-of-words, and lemmas was written to disk
    # they are not needed in memory so they are cleared
    bag_of_words.clear()
    lemmas.clear()

    print(datetime.now().strftime("%H:%M:%S") + ": cleared not needed memory")

    return _sheet


def import_nltk_data(path):
    # for lemmatizer, nltk_data was downloaded to resource
    # to use that data, we append its path to nltk`s data-path
    if not nltk.data.path.__contains__(path):
        print(datetime.now().strftime("%H:%M:%S") + ": appending nltk_data path to nltk`data-path...")
        nltk.data.path.append(path)


# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    import_nltk_data("../resource/nltk_data/")

    workbook = 0
    print(datetime.now().strftime("%H:%M:%S") + ": checking cache...")
    try:
        # file is already created, no need to re-evaluate docs
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        print(datetime.now().strftime("%H:%M:%S") + ": cache found and loaded")

    except FileNotFoundError:
        # file is not created, scores will be calculated, create a file/cache
        workbook = openpyxl.Workbook()
        sheet = create_sheet(workbook.active)
        workbook.save("../out/tf-idf.xlsx")
        print(datetime.now().strftime("%H:%M:%S") + ": cache saved to disk")



