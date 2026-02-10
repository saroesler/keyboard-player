import keyboard
from playsound import playsound
import json
import sys

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

def playsong(musicpath, lastpids, blocking):
    if len(lastpids) > 0:
        for lastpid in lastpids:
            child_pid, status = os.waitpid(lastpid, os.WNOHANG)
            
            if child_pid != 0:
                lastpids.remove(lastpid)
                print("clean")
    
    if len(lastpids) == 0 or not blocking:
        ppid = os.getpid()
        
        child_pid = os.fork()
        
        if child_pid == 0:
            
            os.setuid(int(os.environ['SUDO_UID']))
            #if blocking:
            #    playsound(musicpath, True)
            #else:
            playsound(musicpath)
            print("sound stop")
            
            exit(0)
        else:
            return lastpids + [child_pid]
    else:
        print("busy: reject")
    return lastpids
        
        # Release semaphore
        # sounds_playing.release()
    

    # Release semaphore
    #sounds_playing.release()


blocking = True

if len(sys.argv) > 1:
    if sys.argv[1] == "blocking":
        blocking = True
    elif sys.argv[1] == "nonblocking":
        blocking = False

# Open and read the JSON file
with open('settings.json', 'r') as file:
    data = json.load(file)


lastpids = []

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
        
        lastpids = playsong(musicpath, lastpids, blocking)
    
