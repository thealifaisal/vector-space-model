import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def on_enter(e):
    search_button['background'] = 'MediumPurple3'


def on_leave(e):
    search_button['background'] = 'MediumPurple4'


def on_click_search_box(e):
    search_box.delete(0, tk.END)


# def on_click_alpha_box(e):
#     alpha_box.delete(0, tk.END)


window = tk.Tk()
window.title("Vector Space Model")
window.resizable(False, False)

frame = tk.Frame(window, width=800, height=500, bg="gray15")
frame.pack(fill=tk.X, expand=True)

search_label = tk.Label(window, text="Vector Search", width=15, bg="gray15", fg="white", font=("Courier", 30))
search_label.place(relx=0.5, rely=0.13, anchor=tk.CENTER)

search_box = tk.Entry(window, width=50, font=("Calibre", 10))
search_box.insert(0, "Search Vector Space")
search_box.place(relx=0.412, rely=0.28, anchor=tk.CENTER)

alpha_box = tk.Spinbox(window, width=15, font=("Calibre", 10), from_=0, to=0.99999, format="%.5f", increment=0.00001)
alpha_box.place(relx=0.716, rely=0.28, anchor=tk.CENTER)

# alpha_box = tk.Entry(window, width=18, font=("Calibre", 10))
# alpha_box.insert(0, "Enter Alpha Value")
# alpha_box.place(relx=0.72, rely=0.28, anchor=tk.CENTER)

search_button = tk.Button(window, text="Search", width=25, height=1, bg="MediumPurple4", fg="white")
search_button.place(relx=0.50, rely=0.39, anchor=tk.CENTER)

result_label = tk.Label(window, text="Query Result", width=15, bg="gray15", fg="white", font=("Courier", 15))
result_label.place(relx=0.50, rely=0.6, anchor=tk.CENTER)

result_box = ScrolledText(window, width=75, height=6, bg="white", fg="black", font=("Calibre", 10))
result_box.configure(state='disabled')
result_box.place(relx=0.50, rely=0.8, anchor=tk.CENTER)

search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)
search_box.bind("<FocusIn>", on_click_search_box)
# alpha_box.bind("<FocusIn>", on_click_alpha_box)

window.mainloop()
