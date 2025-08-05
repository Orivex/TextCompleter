from pynput import keyboard
import sys
import pandas as pd

controller = keyboard.Controller()
df = pd.read_csv("shortcuts.csv", delimiter="|")

def write_word(word):
    for ch in word:
        controller.press(ch)
        controller.release(ch)

def backspace(times):
    for i in range(times):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)

text = df["text"].tolist()

shortcut = df["shortcut"].tolist()

next = []

for i in range(len(shortcut)): 
    next.append([shortcut[i][0], 1])

def check_state(key): 
    for i in range(len(text)):
        if hasattr(key, 'char') and key is not None:
            if key.char == next[i][0]:
                if(next[i][1] < len(shortcut[i])):
                    next[i][0] = shortcut[i][next[i][1]]
                next[i][1] += 1
            else: 
                next[i][0] = shortcut[i][0]
                next[i][1] = 1
        elif key == keyboard.Key.space: 
            if next[i][1] == (len(shortcut[i])+1):
                backspace(len(shortcut[i])+1)
                write_word(text[i])
                next[i][0] = shortcut[i][0]
                next[i][1] = 1

    print(next)

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

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as l:
    on_press_hotkey = for_canonical(hot_key.press)
    on_release_hotkey = for_canonical(hot_key.release)

    l.join()