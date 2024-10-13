import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from graph import show_graph
from algo import build_graphs
data = []



# adding the data to the table and the array
def add_to_table():
    value1 = entry1.get()
    value2 = entry2.get()
    value3 = entry3.get()
    for val in data:
        if value1 == val[0]:
            messagebox.showerror("Input Error", "This task already exists!")
            return
    dep = value3.split(",")
    flag = False
    if value3 != '-':
        for i in dep:
            temp = False
            for val in data:
                if i == val[0]:
                    temp = True
            if not temp:
                flag = True
    if flag:
        messagebox.showerror("Input Error", "Please enter an existing dependency or - !")
        return
    if not value1.isalpha() or not len(value1) == 1:
        messagebox.showerror("Input Error", "The task name must be a letter!")
        return
    if not value2.isdigit():
        messagebox.showerror("Input Error", "The duration must be numeric!")
        return
    table.insert('', 'end', values=(value1, value2, value3))
    data.append((value1, value2, value3))
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)


# clearing the table and the array
def clear_table():
    for item in table.get_children():
        table.delete(item)
    data.clear()


# all the graph data will be taken from this function
def submit():
    build_graphs(data)
    show_graph(data)


# main window
root = tk.Tk()
root.title("Critical Path Method")
# text boxes
label1 = tk.Label(root, text="Activity name:")
label1.grid(row=0, column=0, padx=10, pady=10)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=10)
label2 = tk.Label(root, text="Duration:")
label2.grid(row=1, column=0, padx=10, pady=10)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=10)
label3 = tk.Label(root, text="Dependencies separated by a coma or write '-' :")
label3.grid(row=2, column=0, padx=10, pady=10)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, padx=10, pady=10)
# buttons
add_button = tk.Button(root, text="Add to Table", command=add_to_table)
add_button.grid(row=3, column=0, padx=10, pady=10)
clear_button = tk.Button(root, text="Clear Table", command=clear_table)
clear_button.grid(row=3, column=1, padx=10, pady=10)
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, column=2, padx=10, pady=10)
# table
table = ttk.Treeview(root, columns=("Task", "Duration", "Dependency"), show='headings')
table.heading("Task", text="Task")
table.heading("Duration", text="Duration")
table.heading("Dependency", text="Dependency")
table.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()