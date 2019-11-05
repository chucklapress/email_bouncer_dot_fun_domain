#!/usr/bin/env python3
import inotify.adapters
import subprocess
import time

notifier = inotify.adapters.Inotify()
notifier.add_watch('/home/chucklapress/Maildir/new')

for event in notifier.event_gen():
    if event is not None:
        # print event      # uncomment to see all events generated
        if 'IN_CREATE' in event[1]:
             subprocess.run(["/home/chucklapress/./parser_new.py"])
             time.sleep(2)
             subprocess.run(["/home/chucklapress/./data_import.py"])
             time.sleep(1)
             print('IT IS COMPLETED')
