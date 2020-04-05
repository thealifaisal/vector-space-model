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

    # returns a set of a doc: {lemma-0: tf, lemma-1: tf, ...}
    return lemma_set


def prepare_bag_of_words(_lemmas_set,  _bag_of_words):
    # lemma_set for i-th doc and keys() gives lemmas in the set
    lemmas = list(_lemmas_set.keys())
    for lem in lemmas:
        try:
            # a set was used because of its speed due to hashing which costs O(1)
            # otherwise a list would cost O(n) in searching the lemma from bag-of-words
            # because to restrict the repetitive lemmas from entire corpus
            _bag_of_words[lem] = 0
        except KeyError:
            # if lemma exists, it would throw KeyError and would do nothing
            pass
    # for loop ends
    return


def calculate_doc_score(_bag_of_words, _len_of_bag_of_words, _lemmas, _sheet):

    # _bag_of_words = all the unique lemmas from the corpora
    # lemmas = [doc0={trump: 57, ...}, doc1={trump:1, ...}, ...]

    print(datetime.now().strftime("%H:%M:%S") + ": initiating document tf-idf calculations...")

    # iterates row-by-row on _sheet which is better than col-by-col on a _sheet of 6000 rows
    # _sheet is not 0 indexed, so its index starts from 1
    # the 1st row has column names from prepare_sheet()
    # from 2nd row we will start placing the words from bag-of-words
    # iterates until all the words from bag-of-words are placed in sheet
    for i in range(2, _len_of_bag_of_words + 2):

        # i-2 is because bag-of-words is 0 indexed, and this retrieves word from the bag
        # and places into sheet`s cell in 1st column and also assigning to word variable
        word = _sheet.cell(i, 1).value = _bag_of_words[i - 2]

        # 'df' is document-frequency: tells the no. of docs in which word has appeared
        df = 0

        # iterates over the all 56 docs from 0 to 55
        for doc_id in range(0, 56):
            # _lemmas[doc_id] gives a doc as set and get(word) gives the value the term-frequency
            # set was used because of hashing as retrieval is O(1)
            # otherwise list would cost O(n)
            tf = _lemmas[doc_id].get(word)

            if tf is None:
                # tf is None when a word from bag does not appear in the doc
                # tf will be 0 for this doc column in sheet
                # doc_id + 2 is because doc_id starts from 0 and we have to skip the 'word' column
                _sheet.cell(i, doc_id + 2).value = 0
            else:
                # tf is assigned to that doc column
                _sheet.cell(i, doc_id + 2).value = tf
                # and df is incremented because word appears in this doc
                df += 1
        # for loop ends

        # df is assigned to df column
        _sheet.cell(i, 59).value = df

        # idf = log10(N/df), N = size of corpora
        idf = float(format(math.log10(56 / df), '.5f'))
        _sheet.cell(i, 60).value = idf

        # tf`s are assigned to doc cols and idf is calculated
        # we iterate again over the doc cols and place tf*idf in doc cols
        for doc_id in range(0, 56):
            tf = float(_sheet.cell(i, doc_id + 2).value)
            value = float(format(tf * idf, '.5f'))
            _sheet.cell(i, doc_id + 2).value = value
        # for loop ends

    # for loop ends

    print(datetime.now().strftime("%H:%M:%S") + ": completed document tf-idf calculations")
    return _sheet


def process_corpora(_bag_of_words, _lemmas):

    print(datetime.now().strftime("%H:%M:%S") + ": initiating pre-processing of documents...")

    # a loop is run to iterate over the entire corpus of length 56
    for i in range(0, 56):

        file_name = "../resource/trump-speeches/speech_" + str(i) + ".txt"
        file = open(file_name, "r")
        # skips the title
        file.readline()

        # lemma_set = {lemma: tf, ...}
        lemma_set = pre_processing("../resource/stopword-list.txt", file.read())

        # copy() deep copies the set into lemma list
        _lemmas.append(lemma_set.copy())

        # since tokens are created, file is now closed
        file.close()

        # since a deep-copy of lemma_set was appended and not its address was passed
        # this list can be cleared without effecting the one in lemmas
        lemma_set.clear()

        # _lemmas[i] gives a lemma_set for i-th doc
        # _bag_of_words and _lemmas[i] passed by reference
        prepare_bag_of_words(_lemmas[i], _bag_of_words)
    # for loop ends

    print(datetime.now().strftime("%H:%M:%S") + ": documents pre-processing completed")
    return


def prepare_sheet(_sheet):

    # total columns to be created: 1+56+1+1+1 = 60
    # <creating-columns>

    _sheet.cell(1, 1).value = "words"

    for i in range(2, 58):
        _sheet.cell(1, i).value = "d.tf:" + str(i - 2)
    # for loop ends

    _sheet.cell(1, 58).value = "q.tf"
    _sheet.cell(1, 59).value = "df"
    _sheet.cell(1, 60).value = "idf"

    # </creating-columns>
    return


def create_sheet(_sheet):

    print(datetime.now().strftime("%H:%M:%S") + ": preparing cache...")

    # _sheet is passed by reference
    prepare_sheet(_sheet)

    # two important data-structures are initialized
    bag_of_words = {}
    lemmas = []

    # bag_of_words and lemmas are passed by reference
    process_corpora(bag_of_words, lemmas)

    # length of bag-of-words is saved for future use
    _len_of_bag_of_words = len(bag_of_words)

    print(datetime.now().strftime("%H:%M:%S") + ": length of bag-of-words: " + str(_len_of_bag_of_words))

    # keys from set 'bag-of-words' were converted into a list
    # so that keys() would not be called multiple times in the calculate_tf_idf
    bag_of_words = list(bag_of_words.keys())

    # a 'lemmas' list is in memory after being processed by 'process_corpora()'
    # which has sets for each document
    # each set has a key which is a lemma and a value against the key
    # as term-frequency
    # e.g: lemmas = [{trump: 57, ...}, {trump:1, ...}, ...]

    # bag_of_words, lemmas, and _sheet are passed by reference
    calculate_doc_score(bag_of_words, _len_of_bag_of_words, lemmas, _sheet)

    # since bag-of-words, and lemmas was written to disk
    # they are not needed in memory so they are cleared
    bag_of_words.clear()
    lemmas.clear()

    print(datetime.now().strftime("%H:%M:%S") + ": cache prepared")
    print(datetime.now().strftime("%H:%M:%S") + ": cleared not needed memory")

    # returns an excel sheet with all the doc vectors with scores
    return _sheet


def import_nltk_data(path):
    # for lemmatizer, nltk_data was downloaded to resource
    # to use that data, we append its path to nltk`s data-path
    if not nltk.data.path.__contains__(path):
        print(datetime.now().strftime("%H:%M:%S") + ": appending nltk_data path to nltk`data-path...")
        nltk.data.path.append(path)
    return


# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    # this search-engine is based on vector-space-model

    # and uses the 'cache' technique to store the calculated doc vectors
    # and bag-of-words in a file named '../out/tf-idf.xlsx'

    # when no cache is found, in one run the calculations take approx. 11 seconds of which
    # 5 seconds is to pre-process the corpora for tokens, lemma, bag-of-words formation, and
    # 6 seconds to calculate tf-idf score for doc vectors

    # when cache is found, it only takes approx. 6 seconds or less to load the cache file into memory
    # hence a performance improvement of 5 seconds is achieved with no extra CPU utilization

    # imports the data required for lemmatization
    import_nltk_data("../resource/nltk_data/")

    workbook = 0
    len_of_bag_of_words = 0

    print(datetime.now().strftime("%H:%M:%S") + ": checking cache...")
    try:
        # if try successful, file is already created, no need to re-evaluate docs
        # load the workbook
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        # load the sheet
        sheet = workbook["Sheet"]
        print(datetime.now().strftime("%H:%M:%S") + ": cache found and loaded")
        len_of_bag_of_words = sheet.max_row - 1
        print(datetime.now().strftime("%H:%M:%S") + ": length of bag-of-words = " + str(len_of_bag_of_words))

    except FileNotFoundError:
        print(datetime.now().strftime("%H:%M:%S") + ": cache not found")
        # file is not created, scores will be calculated, create a file/cache
        workbook = openpyxl.Workbook()
        # returns a sheet with doc-vectors with doc-tf-idf, df, idf and bag-of-words
        sheet = create_sheet(workbook.active)
        # saves the cache file on disk
        workbook.save("../out/tf-idf.xlsx")
        print(datetime.now().strftime("%H:%M:%S") + ": cache saved to disk")


