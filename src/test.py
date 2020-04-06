import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer


def import_nltk_data(path):
    # for lemmatizer, nltk_data was downloaded to resource
    # to use that data, we append its path to nltk`s data-path
    if not nltk.data.path.__contains__(path):
        nltk.data.path.append(path)
    return


import_nltk_data("../resource/nltk_data/")

lm = WordNetLemmatizer()

print(lm.lemmatize("hilary"))
