#!/usr/bin/env python3
import os, time
import subprocess
path_to_watch = "/home/chucklapress/Maildir/new"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (2)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added:
       print( "Added: ", ", ".join (added))
       subprocess.run(["/home/chucklapress/./parser_new.py"])
  if removed: print( "Removed: ", ", ".join (removed))
  before = after

# keeping this function in the repo in case you decide the you dont want to rely on inotify library its just another watching function
