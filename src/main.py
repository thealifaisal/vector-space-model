from datetime import datetime
import openpyxl
from src.VSM import VSM


# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":

    # object of vsm class created that has methods for document and query processing
    vsm = VSM()

    # this search-engine is based on vector-space-model

    # and uses the 'cache' technique to store the calculated doc vectors
    # and bag-of-words in a file named '../out/tf-idf.xlsx'

    # when no cache is found, the calculations take approx. 8 seconds of which
    #   5 seconds is to pre-process the corpora for tokens, lemma, bag-of-words formation, and
    #   3 seconds to calculate tf-idf score for doc vectors

    # when cache is found,

    # SCENARIO A: ****** LOADING CACHE IN READ-WRITE MODE ******
    #   it only takes approx. 5 seconds to load the cache file into memory
    #   hence a performance improvement of 3 seconds is achieved with no extra CPU utilization

    # SCENARIO B: ****** LOADING CACHE IN READ-ONLY MODE ******
    #   it only takes approx. 1 seconds to load the cache file into memory
    #   hence a performance improvement of 7+ seconds is achieved with no extra CPU utilization

    # Therefore, Cache will be loaded in read-only mode for maximum performance

    # imports the data required for lemmatization
    vsm.import_nltk_data("../resource/nltk_data/")

    # 'workbook' is excel file object that contains a sheet which has bag-of-words
    # doc vectors, df, idf, and query vectors
    workbook = 0
    # 'len_of_bag_of_words' has the total number of unique words from corpora
    # e.g: 6015 in my case
    len_of_bag_of_words = 0

    print(datetime.now().strftime("%H:%M:%S") + ": checking cache...")
    try:
        # if try successful, file is already created, no need to re-evaluate docs
        # load the workbook
        workbook = openpyxl.load_workbook("../out/tf-idf.xlsx")
        # load the sheet
        doc_sheet = workbook["Sheet"]
        print(datetime.now().strftime("%H:%M:%S") + ": cache found and loaded")
        len_of_bag_of_words = doc_sheet.max_row - 1
        print(datetime.now().strftime("%H:%M:%S") + ": length of bag-of-words = " + str(len_of_bag_of_words))

    except FileNotFoundError:
        print(datetime.now().strftime("%H:%M:%S") + ": cache not found")
        # file is not created, scores will be calculated, create a file/cache
        workbook = openpyxl.Workbook()
        # returns a sheet with doc-vectors with doc-tf-idf, df, idf and bag-of-words
        doc_sheet = vsm.create_doc_sheet(workbook.active)
        # saves the cache file on disk
        workbook.save("../out/tf-idf.xlsx")
        print(datetime.now().strftime("%H:%M:%S") + ": cache saved to disk")

    # takes query from user as string appends a period to the end of query for tokenizer handling
    # query = input(datetime.now().strftime("%H:%M:%S") + "Search: ") + "."
    query = "Hillary Clinton "
    # alpha = float(input("enter alpha: "))
    alpha = 0.0005

    vsm.update_doc_sheet(doc_sheet, query)
    result_set = vsm.create_result_set(doc_sheet, alpha)
    vsm.write_result_to_file("../out/result_set.txt", result_set, query, alpha)

    workbook.close()
    print(datetime.now().strftime("%H:%M:%S") + ": cache-file closed")
    print(datetime.now().strftime("%H:%M:%S") + ": exit")
