from multiprocessing.connection import Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import config

def load_access_points(access_points_file):
    """Loading and parcing access points from a json file"""
    f = open(access_points_file)
    data = json.load(f)
    f.close()
    return data

def send_message(message):
    """Sending message to the server"""
    conn = Client((config.server_address, config.server_port))
    conn.send(message)
    conn.send('close connection')
    conn.close()

class  MyHandler(FileSystemEventHandler):
    # the function is triggered when the file is changed
    def on_modified(self, event):
        send_message(load_access_points(config.access_points_file))

if __name__ ==  "__main__":
    send_message(load_access_points(config.access_points_file))
    # starting monitor the file for changes
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path=config.access_points_file,  recursive=False)
    observer.start()
    observer.join()

