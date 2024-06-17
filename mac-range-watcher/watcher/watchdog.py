import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from utils.config import mac_start, mac_end

class Watchdog:
    def __init__(self, file_to_watch, callback, gui_queue, debounce_time=5):
        self.file_to_watch = file_to_watch
        self.callback = callback
        self.gui_queue = gui_queue
        self.event_handler = FileModifiedHandler(file_to_watch=self.file_to_watch, callback=self.callback, gui_queue=self.gui_queue, debounce_time=debounce_time)
        self.observer = Observer()

    def start(self):
        directory_to_watch = os.path.dirname(self.file_to_watch)
        self.observer.schedule(self.event_handler, path=directory_to_watch, recursive=False)

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch, callback, gui_queue, debounce_time):
        self.file_to_watch = file_to_watch
        self.callback = callback
        self.gui_queue = gui_queue
        self.debounce_time = debounce_time
        self.last_modified = 0

    def on_modified(self, event):
        if event.src_path == self.file_to_watch:
            current_time = time.time()
            if current_time - self.last_modified > self.debounce_time:
                print("modified")
                self.callback(event.src_path, mac_start, mac_end, self.gui_queue)
                self.last_modified = current_time