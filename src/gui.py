# ******************************************
#
#   AUTHOR: ALI FAISAL
#   Github: https://github.com/thealifaisal/
#
# ******************************************

import tkinter as tk


class GUI:

    # below attributes are created because these will accessed by the run_query() method
    vsm = 0
    doc_sheet = 0

    search_box = 0
    alpha_box = 0
    result_box = 0
    search_button = 0

    # constructor
    def __init__(self, vsm, doc_sheet):
        self.vsm = vsm
        self.doc_sheet = doc_sheet

    # creates the GUI
    def setGUI(self):

        # an object of window is created
        _window = tk.Tk()
        _window.title("Vector Space Model")
        # window cannot be resized
        _window.resizable(False, False)

        # frame is created and placed above the _window
        frame = tk.Frame(_window, width=800, height=500, bg="gray15")
        frame.pack(fill=tk.X, expand=True)

        # creates a label that displays "Vector Search"
        search_label = tk.Label(_window, text="Vector Search", width=15, bg="gray15", fg="white", font=("Courier", 30))
        search_label.place(relx=0.5, rely=0.13, anchor=tk.CENTER)

        # creates the search_box where query will be entered
        self.search_box = tk.Entry(_window, width=50, font=("Calibre", 10))
        self.search_box.insert(0, "")
        self.search_box.place(relx=0.412, rely=0.28, anchor=tk.CENTER)

        # creates the alpha_box where alpha value will be entered
        self.alpha_box = tk.Spinbox(_window, width=15, font=("Calibre", 10), format="%.4f", increment=0.0001,
                                    from_=0, to=0.9999)
        self.alpha_box.place(relx=0.716, rely=0.28, anchor=tk.CENTER)

        # a search_button is created, on its on-click run_query() method will be executed
        self.search_button = tk.Button(_window, text="Search", width=25, height=1, bg="MediumPurple4", fg="white",
                                       command=self.run_query)
        self.search_button.place(relx=0.50, rely=0.39, anchor=tk.CENTER)

        # creates a label that displays "Query Result"
        result_label = tk.Label(_window, text="Query Result", width=15, bg="gray15", fg="white", font=("Courier", 15))
        result_label.place(relx=0.50, rely=0.6, anchor=tk.CENTER)

        # a result-box is created that displays the query result
        self.result_box = tk.Text(_window, width=75, height=6, bg="white", fg="black", font=("Calibre", 10))
        self.result_box.configure(state=tk.NORMAL)
        self.result_box.place(relx=0.50, rely=0.8, anchor=tk.CENTER)

        # when the mouse enters the scope of search-button, on_enter method is executed
        self.search_button.bind("<Enter>", self.on_enter)
        # when the mouse leaves the scope of search-button, on_leave method is executed
        self.search_button.bind("<Leave>", self.on_leave)

        # returns the window object
        return _window

    # processes the query and writes result to result-box and to file
    def run_query(self):

        # deletes the contents of result-box
        self.result_box.delete('1.0', 'end')

        # takes query and alpha-value from the user as a string
        _query = self.search_box.get()
        _alpha = self.alpha_box.get()

        # if both query and alpha value are entered then proceed
        # otherwise display error on result-box
        if _query != "" and _alpha != "":

            # appends a space to the end of query for tokenizer handling
            _query += " "

            # converts the alpha-value to float
            _alpha = float(_alpha)

            # fills the query vector with tf-idf values in doc-sheet
            self.vsm.update_doc_sheet(self.doc_sheet, _query)

            # after creating a result-set
            # returns a result-set as {doc-id: angle, doc-id: angle, ...}
            _result_set:dict = self.vsm.create_result_set(self.doc_sheet, _alpha)

            # appends a curly-brace to start of result string
            result_string = "{ "
            result_length = 0

            # iterates for every doc in result-set
            for doc in _result_set.keys():
                result_string += str(doc) + ", "
                result_length += 1

            # appends a curly-brace to end of result string
            result_string += "}"

            # writes the result-length in result-box
            self.result_box.insert(tk.INSERT, "Length: " + str(result_length) + "\n\n")

            # writes the relevant documents in result-box
            self.result_box.insert(tk.INSERT, "Relevant Documents: " + result_string)

            # writes the result-set to file
            self.vsm.write_result_to_file("../out/result_set.txt", _result_set, _query, _alpha)

            # clearing result set
            _result_set.clear()
        else:
            # when query or alpha is empty
            # displays the error in result-box
            self.result_box.insert(tk.INSERT, "Query or Alpha is empty... !!!" + "\n")

        return

    # on hover functions

    def on_enter(self, e):
        self.search_button['background'] = 'MediumPurple3'

    def on_leave(self, e):
        self.search_button['background'] = 'MediumPurple4'
