from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class MonitorFolder(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created file: {event.src_path}")
    
    def on_deleted(self, event):
        print(f"Deleted file: {event.src_path}")
    
    def on_modified(self, event):
        print(f"Modified file: {event.src_path}")

def monitor_directory(directory):
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


directory_to_monitor = "C:/DIR"
monitor_directory(directory_to_monitor)
