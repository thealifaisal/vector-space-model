import nltk
import openpyxl
from src.pre_processing import Preprocessing
import time


# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    # for lemmatizer, nltk_data was downloaded to resource
    # to use that data, we append its path to nltk`s data
    nltk.data.path.append("../resource/nltk_data/")

    # caches are used so that the next time program runs
    # no doc pre-processing is done which saves a lot of time
    # here cache is a file named tf-idf.xlsx
    cache = 0
    try:
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        cache = 1   # file is already created, no need to re-evaluate docs
    except FileNotFoundError:
        cache = 0   # file is not created, scores will be calculated

    # if cache exists
    if cache == 1:
        print("cache ready")
    else:
        # create a file/cache
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # total columns to be created: 118

        # <creating-columns>
        cell = sheet.cell(1, 1).value = "words"
        for i in range(2, 58):
            sheet.cell(1, i).value = "d.tf:" + str(i-2)
        sheet.cell(1, 58).value = "q.tf"
        sheet.cell(1, 59).value = "df"
        sheet.cell(1, 60).value = "idf"
        for i in range(61, 117):
            sheet.cell(1, i).value = "d.val:" + str(i-61)
        sheet.cell(1, 117).value = "q.val"
        # </creating-columns>

        # a stop-word file is opened and parsed to be saved as a list
        stop_file = open("../resource/stopword-list.txt", "r")
        stop_list = stop_file.read().split("\n")

        # two important data-structures are initialized
        bag_of_words = {}
        lemmas = []

        # a loop is run to iterate over the entire corpus of length 56
        for i in range(0, 56):
            file_name = "../resource/trump-speeches/speech_" + str(i) + ".txt"
            file = open(file_name, "r")
            file.readline()  # skips the title

            # <pre-processing>
            pre_processing = Preprocessing()
            pre_processing.stop_word = stop_list
            # a string of file was passed to tokenizer that returns a list of tokens
            tokens = pre_processing.tokenizer(file.read())
            # a set of lemma is returned as {lemma: tf}
            lemma_set = pre_processing.lemmatizer(tokens)
            # copy() deep copies the set into lemma list
            lemmas.append(lemma_set.copy())
            # list of tokens is unusable, so it is cleared
            tokens.clear()
            # since a deep-copy of lemma_set was appended and not its address was passed
            # this list can be cleared without effecting the one in lemmas
            lemma_set.clear()

            # lemma[i] gives a set for i-th doc and keys() gives lemmas in the set
            for lem in lemmas[i].keys():
                try:
                    # a set was used because of its speed due to hashing which costs O(1)
                    # otherwise a list would cost O(n) in searching the lemma from bag-of-words
                    # because to restrict the repetitive lemmas from entire corpus
                    bag_of_words[lem] = 0
                except KeyError:
                    # if lemma exists, it would throw KeyError and would do nothing
                    pass
            # </pre-processing>

        # length of bag-of-words is saved for future use
        len_of_bag_of_words = len(bag_of_words)
        print("Length of Bag-of-Words: " + str(len_of_bag_of_words))

        # keys from bag-of-words were converted into a list
        # so that keys() would not be called multiple times in the below loop
        bag_of_words = list(bag_of_words.keys())

        # writes words to excel sheet from 2nd row
        i = 2
        for words in bag_of_words:
            sheet.cell(i, 1).value = words
            i += 1

        # since bag-of-words was written to disk
        # it is not needed in memory so it is cleared
        bag_of_words.clear()

        # a lemmas-list is in memory which has sets for each document
        # each set has a key which is a lemma and a value against the key
        # as term-frequency

        workbook.save("../out/tf-idf.xlsx")
        workbook.close()

