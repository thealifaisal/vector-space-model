import nltk
import openpyxl
from src.pre_processing import Preprocessing


# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    nltk.data.path.append("../resource/nltk_data/")

    cache = 0
    try:
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        cache = 1   # file is already created, no need to re-evaluate docs
    except FileNotFoundError:
        cache = 0   # file is not created, scores will be calculated

    if cache == 0:
        # create a file
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # total columns to be created: 118
        cell = sheet.cell(1, 1).value = "words"
        for i in range(2, 58):
            sheet.cell(1, i).value = "d.tf:" + str(i-2)
        sheet.cell(1, 58).value = "q.tf"
        sheet.cell(1, 59).value = "df"
        sheet.cell(1, 60).value = "idf"
        for i in range(61, 117):
            sheet.cell(1, i).value = "d.val:" + str(i-61)
        sheet.cell(1, 117).value = "q.val"
        workbook.save("../out/tf-idf.xlsx")
        workbook.close()
    else:
        print("cache ready")


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

    len_of_bag_of_words = len(bag_of_words)
