from tkinter import *
from tkinter import messagebox
from tkinter import ttk as tk
import sys, os, csv, subprocess, signal, time
import pandas as pd

root = Tk()
root.geometry("800x400")
root.resizable(False, False)
root.title("TextCompleter by Blacklight")

file_name = "shortcuts.csv"

if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(["shortcut", "text"]) 

df = pd.read_csv("shortcuts.csv", delimiter="|", on_bad_lines='skip')

status = StringVar()
status.set("😴 INACTIVE 😴")

shortcut_lb = Label(root, text="Shortcut")
text_lb = Label(root, text="Text")

def limit_entry(limit, string_var):
    def callback(*args):   
        value = string_var.get()
        if(len(value) > limit):
            string_var.set(value[:limit])
    return callback

shortcut_var = StringVar()
shortcut_var.trace_add("write", limit_entry(14, shortcut_var))
text_var = StringVar()
text_var.trace_add("write", limit_entry(50, text_var))
shortcut_entry = Entry(root, width=19, font="Arial 10", justify="center", textvariable=shortcut_var)
text_entry = Entry(root, width=55, font="Arial 10", justify="center", textvariable=text_var)

shortcut_lb.pack()
shortcut_entry.pack()
text_lb.pack()
text_entry.pack(pady=(0, 10))

def reload_df():
    global df
    df.to_csv(file_name, sep="|", index=False)
    for widget in frame2.winfo_children():
        widget.destroy()
    load_shortcuts()

def add_shortcut():
    global df

    shortcut = shortcut_entry.get().lstrip().rstrip()
    text = text_entry.get().lstrip().rstrip()

    if(len(text) == 0 or len(shortcut) == 0):
        messagebox.showwarning("Open your eyes, man", "Fill in both fields!!!")
        return
    
    if(len(text) < len(shortcut)):
        messagebox.showwarning("Are you serious?", "Shortcut has to be shorter than the corresponding text. What a surprise, huh?")
        return
    
    if(shortcut in df["shortcut"].values):
        messagebox.showwarning("You forget fast", "Shortcut already exists!")
        return
    
    new_row = pd.DataFrame({"shortcut": [shortcut], "text": [text]})
    df = pd.concat([df, new_row], ignore_index=True)

    shortcut_entry.delete(0, END)
    text_entry.delete(0, END)

    reload_df()

def delete_shortcut(index):
    global df
    df.drop(index, inplace=True)
    reload_df()

script = None
script_running = False
def toggle_script():

    global script
    active = False

    def after_tasks():
        global script_running
        if(active):
            script_running = True
            status.set("🤓 ACTIVE 🤓")
        else:
            script_running = False
            status.set("😴 INACTIVE 😴")

        toggle_btn.config(state="normal")

    toggle_btn.config(state="disabled")

    if(script_running):

        if os.name == "nt": # Windows
            script.send_signal(signal.CTRL_BREAK_EVENT)
        else: # Linux, MacOS
            script.terminate()

        script.wait()
        active = False

    else:
        path = os.path.join(os.getcwd(), "dist_completer", "completer.exe")

        if os.name == "nt":
            script = subprocess.Popen([path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            script = subprocess.Popen([path])
        
        active = True

    root.after(1200, lambda: after_tasks()) # Wait long enough to execute/terminate script

Button(root, text="Add shortcut", command=add_shortcut).pack(pady=(0, 40))

toggle_btn = Button(root, text="Toggle TextCompleter", command=toggle_script)
toggle_btn.pack(pady=(0, 10))

Label(root, textvariable=status, font=100).pack(pady=(0, 20))

Label(root, text="Your shortcuts:").pack()

frame = Frame(root)
frame.pack(fill="both", expand=True)

canvas = Canvas(frame)
canvas.pack(side="left", fill="both", expand=True)

scroll_bar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scroll_bar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scroll_bar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame2 = Frame(canvas)

canvas.create_window((0, 0), window=frame2, anchor="nw")

frame2.grid_columnconfigure(0, weight=1)

def load_shortcuts():
    for index, row in df.iloc[::-1].iterrows():
        row_frame = Frame(frame2)
        row_frame.grid(sticky="ew", pady=2)

        row_number = Label(row_frame, text=index, anchor="w", width=5)
        row_number.grid(row=0, column=0, padx=(5, 10), sticky="w")

        s_lb = Label(row_frame, text=row["shortcut"], anchor="w", width=19)
        s_lb.grid(row=0, column=1, padx=5, sticky="w")

        t_lb = Label(row_frame, text=row["text"], anchor="w", width=55)
        t_lb.grid(row=0, column=2, padx=5, sticky="we")

        dl_shortcut_bt = Button(row_frame, text="Delete", command=lambda i=index: delete_shortcut(i))
        dl_shortcut_bt.grid(row=0, column=4, padx=(10, 5), sticky="e")

        row_frame.grid_columnconfigure(2, weight=1)
        row_frame.grid_columnconfigure(3, weight=1)

    # Important to see ALL shortcuts
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_close_window():
    if(script_running and script is not None):

        if os.name == "nt":
            script.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            script.terminate()

        script.wait()
    root.destroy()


load_shortcuts()
root.protocol("WM_DELETE_WINDOW", on_close_window)
root.mainloop()
