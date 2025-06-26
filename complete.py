from pynput import keyboard

controller = keyboard.Controller()

def write_word(word):
    for ch in word:
        controller.press(ch)
        controller.release(ch)

def delete_word(word):
    for i in range(len(word)):
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
    if hasattr(key, 'char') and key is not None:
        print(next)
        for i in range(len(mail)):
            if(key.char == next[i][0]):
                if(next[i][1] == (len(seq[i]))):
                    delete_word(seq[i])
                    write_word(mail[i])
                    next[i][0] = seq[i][0]
                    next[i][1] = 1
                else:
                    next[i][0] = seq[i][next[i][1]]
                    next[i][1] += 1
            else: 
                next[i][0] = seq[i][0]
                next[i][1] = 1
                
        #if(state[0] == 0 and key.char == "b"):
        #    state[0] += 1
        #elif(state[0] == 1 and key.char == "i"):
        #    state[0] += 1
        #elif(state[0] == 2 and key.char == "l"):
        #    state[0] += 1
        #else: 
        #    state[0] = 0

        # STATE 1

        #if(state[1] == 0 and key.char == "a"):
        #    state[1] += 1
        #elif(state[1] == 1 and key.char == "b"):
        #    state[1] += 1
        #elif(state[1] == 2 and key.char == "u"):
        #    state[1] += 1
        #elif(state[1] == 3 and key.char == "1"):
        #    state[1] += 1
        #elif(state[1] == 4 and key.char == "0"):
        #    state[1] += 1
        #else: 
        #    state[1] = 0

        
    #elif(state[0] == 3 and key == keyboard.Key.space):
    #    delete_word(seq[0])
    #    write_word(mail[0])
    #    state[0] = 0

def on_press(key):
    check_state(key)

def on_hotKey():
    return False

#hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<menu>'), on_hotKey())

def on_release(key):
    if(key == keyboard.Key.esc):
        return False
    
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: listener.join()