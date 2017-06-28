#!/usr/bin/env python

import os
import sys
import re
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

ignore = (
    re.compile('.*\.css'),
)

class DogEventHandler(PatternMatchingEventHandler):
    def __init__(self, command, *args, **kwargs):
        super(DogEventHandler, self).__init__(*args, **kwargs)
        self.command = command

    def on_modified(self, event):
        os.system(self.command)

def main(args):
    command = ' '.join(args[1:])
    event_handler = DogEventHandler(command, ignore_patterns=['*.css'])
    observer = Observer()
    observer.schedule(event_handler, path=args[0], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: %s <file> <command>' % sys.argv[0]
    else:
        main(sys.argv[1:])
