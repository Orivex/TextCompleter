from pynput import keyboard
import sys

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


def on_press(key):
    check_state(key)
    hotkey_exit.press(listener.canonical(key))
    hotkey_stop_start.press(listener.canonical(key))

def on_release(key):
    hotkey_exit.release(listener.canonical(key))
    hotkey_stop_start.release(listener.canonical(key))
    
def on_hotkey_exit():
    sys.exit()


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
stopped = False

def on_hotkey_stop_start():
    global stopped
    if(stopped):
        listener.start()
    else:
        listener.stop()

    stopped = not stopped


hotkey_exit = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<menu>+<enter>'), on_hotkey_exit)
hotkey_stop_start = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<menu>'), on_hotkey_stop_start)

listener.join()