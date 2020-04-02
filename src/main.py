import nltk
import openpyxl
from src.pre_processing import Preprocessing

# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    nltk.data.path.append("../resource/nltk_data/")

    stop_file = open("../resource/stopword-list.txt", "r")
    stop_list = stop_file.read().split("\n")

    bag_of_words = {}

    file_name = "../resource/trump-speeches/speech_0.txt"
    file = open(file_name, "r")
    file.readline()  # skips the title

    # <pre-processing>
    pre_processing = Preprocessing()
    pre_processing.stop_word = stop_list
    tokens = pre_processing.tokenizer(file.read())
    lemmas = pre_processing.lemmatizer(tokens)

    for lem in lemmas:
        try:
            bag_of_words[lem] = 0
        except KeyError:
            pass
    # </pre-processing>

    # print(bag_of_words.keys())
