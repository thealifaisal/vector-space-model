from src.pre_processing import Preprocessing
import nltk

# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    nltk.data.path.append("../resource/nltk_data/")

    stop_file = open("../resource/stopword-list.txt", "r")
    stop_list = stop_file.read().split("\n")

    file_name = "../resource/trump-speeches/speech_0.txt"
    file = open(file_name, "r")
    file.readline()     # skips the title

    pre_processing = Preprocessing()
    pre_processing.stop_word = stop_list
    tokens = pre_processing.tokenizer(file.read())
    lemmas = pre_processing.lemmatizer(tokens)
