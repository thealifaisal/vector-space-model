import tkinter as tk


class GUI:

    vsm = 0
    doc_sheet = 0

    search_box = 0
    alpha_box = 0
    result_box = 0
    search_button = 0

    def __init__(self, vsm, doc_sheet):
        self.vsm = vsm
        self.doc_sheet = doc_sheet

    def setGUI(self):

        _window = tk.Tk()
        _window.title("Vector Space Model")
        _window.resizable(False, False)

        frame = tk.Frame(_window, width=800, height=500, bg="gray15")
        frame.pack(fill=tk.X, expand=True)

        search_label = tk.Label(_window, text="Vector Search", width=15, bg="gray15", fg="white", font=("Courier", 30))
        search_label.place(relx=0.5, rely=0.13, anchor=tk.CENTER)

        self.search_box = tk.Entry(_window, width=50, font=("Calibre", 10))
        self.search_box.insert(0, "")
        self.search_box.place(relx=0.412, rely=0.28, anchor=tk.CENTER)

        self.alpha_box = tk.Spinbox(_window, width=15, font=("Calibre", 10), format="%.4f", increment=0.0001,
                                    from_=0, to=0.9999)
        self.alpha_box.place(relx=0.716, rely=0.28, anchor=tk.CENTER)

        # alpha_box = tk.Entry(window, width=18, font=("Calibre", 10))
        # alpha_box.insert(0, "Enter Alpha Value")
        # alpha_box.place(relx=0.72, rely=0.28, anchor=tk.CENTER)

        self.search_button = tk.Button(_window, text="Search", width=25, height=1, bg="MediumPurple4", fg="white",
                                       command=self.run_query)
        self.search_button.place(relx=0.50, rely=0.39, anchor=tk.CENTER)

        result_label = tk.Label(_window, text="Query Result", width=15, bg="gray15", fg="white", font=("Courier", 15))
        result_label.place(relx=0.50, rely=0.6, anchor=tk.CENTER)

        self.result_box = tk.Text(_window, width=75, height=6, bg="white", fg="black", font=("Calibre", 10))
        self.result_box.configure(state=tk.NORMAL)
        self.result_box.place(relx=0.50, rely=0.8, anchor=tk.CENTER)

        self.search_button.bind("<Enter>", self.on_enter)
        self.search_button.bind("<Leave>", self.on_leave)

        return _window

    def run_query(self):

        self.result_box.delete('1.0', 'end')

        # takes query from user as string appends a space to the end of query for tokenizer handling
        _query = self.search_box.get()
        _alpha = self.alpha_box.get()

        if _query != "" and _alpha != "":

            _query += " "
            _alpha = float(_alpha)

            # fills the query vector with tf-idf values
            self.vsm.update_doc_sheet(self.doc_sheet, _query)
            # ret result-set as {doc-id: angle, doc-id: angle, ...}
            _result_set = self.vsm.create_result_set(self.doc_sheet, _alpha)

            result_string = "{ "
            result_length = 0

            for doc in _result_set.keys():
                result_string += str(doc) + ", "
                result_length += 1

            result_string += "}"

            self.result_box.insert(tk.INSERT, "Length: " + str(result_length) + "\n\n")
            self.result_box.insert(tk.INSERT, "Relevant Documents: " + result_string)

            self.vsm.write_result_to_file("../out/result_set.txt", _result_set, _query, _alpha)
        else:
            self.result_box.insert(tk.INSERT, "Query or Alpha is empty... !!!" + "\n")

        return

    def on_enter(self, e):
        self.search_button['background'] = 'MediumPurple3'

    def on_leave(self, e):
        self.search_button['background'] = 'MediumPurple4'

    def on_click_search_box(self, e):
        self.search_box.delete(0, tk.END)
