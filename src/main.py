import nltk
import openpyxl
import math
import threading
from datetime import datetime
from src.pre_processing import Preprocessing

# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    # for lemmatizer, nltk_data was downloaded to resource
    # to use that data, we append its path to nltk`s data-path
    if not nltk.data.path.__contains__("../resource/nltk_data/"):
        print(datetime.now().strftime("%H:%M:%S") + ": appending nltk_data path to nltk`data-path...")
        nltk.data.path.append("../resource/nltk_data/")

    # caches are used so that the next time program runs
    # no doc pre-processing is done which saves a lot of time
    # here cache is a file named tf-idf.xlsx

    # variable init
    cache = workbook = 0

    print(datetime.now().strftime("%H:%M:%S") + ": checking cache...")
    try:
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        # file is already created, no need to re-evaluate docs
        cache = 1
    except FileNotFoundError:
        # file is not created, scores will be calculated
        cache = 0

    # if cache exists
    if cache == 1:
        print(datetime.now().strftime("%H:%M:%S") + ": cache found and loaded")
    else:
        print(datetime.now().strftime("%H:%M:%S") + ": cache not found")
        print(datetime.now().strftime("%H:%M:%S") + ": preparing cache...")
        # create a file/cache
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # total columns to be created: 1+56+1+1+1+56+1 = 117

        # <creating-columns>
        cell = sheet.cell(1, 1).value = "words"
        for i in range(2, 58):
            sheet.cell(1, i).value = "d.tf:" + str(i - 2)
        sheet.cell(1, 58).value = "q.tf"
        sheet.cell(1, 59).value = "df"
        sheet.cell(1, 60).value = "idf"
        for i in range(61, 117):
            sheet.cell(1, i).value = "d.val:" + str(i - 61)
        sheet.cell(1, 117).value = "q.val"
        # </creating-columns>

        # a stop-word file is opened and parsed to be saved as a list
        stop_file = open("../resource/stopword-list.txt", "r")
        stop_list = stop_file.read().split("\n")

        # two important data-structures are initialized
        bag_of_words = {}
        lemmas = []

        # <pre-processing>
        print(datetime.now().strftime("%H:%M:%S") + ": pre-processing initiating...")

        # a loop is run to iterate over the entire corpus of length 56
        for i in range(0, 56):
            file_name = "../resource/trump-speeches/speech_" + str(i) + ".txt"
            file = open(file_name, "r")

            # skips the title
            file.readline()

            # creating a object of the Preprocessing class
            pre_processing = Preprocessing()

            # a stop-list is assigned to attribute of class
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

        print(datetime.now().strftime("%H:%M:%S") + ": pre-processing completed")
        # </pre-processing>

        # length of bag-of-words is saved for future use
        len_of_bag_of_words = len(bag_of_words)
        print(datetime.now().strftime("%H:%M:%S") + ": Length of Bag-of-Words: " + str(len_of_bag_of_words))

        # keys from bag-of-words were converted into a list
        # so that keys() would not be called multiple times in the below loop
        bag_of_words = list(bag_of_words.keys())

        # a lemmas-list is in memory which has sets for each document
        # each set has a key which is a lemma and a value against the key
        # as term-frequency
        # e.g: [{trump: 57, ...}, {trump:1, ...}, ...]

        # <tf-idf calculation>
        print(datetime.now().strftime("%H:%M:%S") + ": starting tf-idf calculations...")

        for i in range(2, len_of_bag_of_words + 2):
            word = sheet.cell(i, 1).value = bag_of_words[i-2]
            df = 0
            idf = 0.0
            for doc_id in range(0, 56):
                tf = lemmas[doc_id].get(word)
                if tf is None:
                    sheet.cell(i, doc_id + 2).value = 0
                else:
                    sheet.cell(i, doc_id + 2).value = tf
                    df += 1
            sheet.cell(i, 59).value = df
            idf = float(format(math.log10(56/df), '.5f'))
            sheet.cell(i, 60).value = idf
            for doc_id in range(0, 56):
                tf = float(sheet.cell(i, doc_id+2).value)
                value = float(format(tf*idf, '.5f'))
                sheet.cell(i, doc_id+61).value = value

        print(datetime.now().strftime("%H:%M:%S") + ": tf-idf calculations completed")
        # </tf-idf calculation>

        # since bag-of-words, and lemmas was written to disk
        # they are not needed in memory so they are cleared
        bag_of_words.clear()
        lemmas.clear()

        print(datetime.now().strftime("%H:%M:%S") + ": cleared not needed memory")

        workbook.save("../out/tf-idf.xlsx")
        workbook.close()
        print(datetime.now().strftime("%H:%M:%S") + ": cache saved to disk")

