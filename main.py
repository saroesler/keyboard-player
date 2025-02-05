import keyboard
from playsound import playsound
import json

import threading
import random
import os

# Value can be changed.
# The max number of sounds allow to be played at the same time
max_sounds = 10
sounds_folder="./sounds"

# ----------------------------------------
# FROM HERE ON DOWN DON'T THE CHANGE CODE!
#                (or do?)
# ----------------------------------------

# sounds_playing = threading.Semaphore(max_sounds)

def playsong(musicpath):
    
    ppid = os.getpid()
    
    child_pid = os.fork()
    
    if child_pid == 0:
        
        os.setuid(int(os.environ['SUDO_UID']))
        

        playsound(musicpath)
    else:
        os.waitpid(child_pid, 0)
        
        # Release semaphore
        # sounds_playing.release()
    

    # Release semaphore
    #sounds_playing.release()




# Open and read the JSON file
with open('settings.json', 'r') as file:
    data = json.load(file)



while True:
    event = keyboard.read_event()
    
    if event.name not in data['keys']:
        print("%s not supported" % event.name)
        continue
    
    musicpath = data['keys'][event.name]

    # When key is pressed start thread for playing sound
    # and check if we can decrement semaphore counter
    if event.event_type == "down":
    # and sounds_playing.acquire(blocking=False):
        print(musicpath)

        thread = threading.Thread(target=playsong, args=[musicpath])
        thread.start()
