from src.pre_processing import Preprocessing

# ---------------------------------- main code ----------------------------------
if __name__ == "__main__":
    stop_file = open("../stopword-list.txt", "r")
    stop_list = stop_file.read().split("\n")

    file_name = "../trump-speeches/speech_0.txt"
    file = open(file_name, "r")
    file.readline()

    pre_processing = Preprocessing()
    pre_processing.stop_word = stop_list
    tokens = pre_processing.tokenizer(file.read())
    print(tokens)
