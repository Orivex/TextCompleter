from pynput import keyboard
import sys
from tkinter import *
from tkinter import ttk as tk

controller = keyboard.Controller()

def write_word(word):
    for ch in word:
        controller.press(ch)
        controller.release(ch)

def backspace(times):
    for i in range(times):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)

mail = [
    "email42@gmail.com",
    "email44@gmail.com"
    ]

seq = [
    "em42",
    "em44"
    ]

next = []

for i in range(len(seq)): 
    next.append([seq[i][0], 1])

def check_state(key): 
    print(next)
    for i in range(len(mail)):
        if hasattr(key, 'char') and key is not None:
            if key.char == next[i][0]:
                if(next[i][1] < len(seq[i])):
                    next[i][0] = seq[i][next[i][1]]
                next[i][1] += 1
            else: 
                next[i][0] = seq[i][0]
                next[i][1] = 1
        elif key == keyboard.Key.space: 
            if next[i][1] == (len(seq[i])+1):
                backspace(len(seq[i])+1)
                write_word(mail[i])
                next[i][0] = seq[i][0]
                next[i][1] = 1



def for_canonical(f):
    return lambda k: f(l.canonical(k))

    
def on_hot_key():
    print("HOT")
    sys.exit()
    root.quit()
    
hot_key = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<menu>'),
    on_hot_key)

def on_press(key):
    check_state(key)
    on_press_hotkey(key)

def on_release(key):
    on_release_hotkey(key)




root = Tk()
frm = tk.Frame(root)
frm.grid()
root.geometry("600x400")
tk.Label(frm, text="Full Email").grid(column=0, row=0)
tk.Label(frm, text="Short cut").grid(column=1, row=0)
cray = 0
entry = tk.Entry(root, textvariable=cray,font="Arial 10")
entry.grid(column=0, row=1)
root.mainloop()
root.after_cancel(sys.exit())

with keyboard.Listener(

    
        on_press=on_press,
        on_release=on_release) as l:
    on_press_hotkey = for_canonical(hot_key.press)
    on_release_hotkey = for_canonical(hot_key.release)

    l.join()