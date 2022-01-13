from multiprocessing.connection import Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import config

def load_access_points(access_points_file):
    f = open(access_points_file)
    data = json.load(f)
    f.close()
    return data

def send_message(message):
    conn = Client((config.server_address, config.server_port))
    conn.send(message)
    conn.send('close connection')
    conn.close()

class  MyHandler(FileSystemEventHandler):
    def on_modified(self,  event):
        global access_points
        updated_access_points = load_access_points(config.access_points_file)
        for access_point in access_points["access_points"]:
            is_found = False
            for updated_access_point in updated_access_points["access_points"]:
                if access_point["ssid"] == updated_access_point["ssid"]:
                    is_found = True
                    if access_point["snr"] != updated_access_point["snr"]:
                        send_message("%s SNR has changed from %s to %s" % (access_point["ssid"], access_point["snr"], updated_access_point["snr"]))
                    if access_point["channel"] != updated_access_point["channel"]:
                        send_message("%s channel has changed from %s to %s" % (access_point["ssid"], access_point["channel"], updated_access_point["channel"]))
            if is_found == False:
                send_message("%s is removed from the list" % (access_point["ssid"]))
        for updated_access_point in updated_access_points["access_points"]:
            is_new = True
            for access_point in access_points["access_points"]:
                if updated_access_point["ssid"] == access_point["ssid"]:
                    is_new = False
            if is_new == True:
                send_message("%s is added to the list with SNR %s and channel %s" % (updated_access_point["ssid"], updated_access_point["snr"], updated_access_point["channel"]))
        access_points = updated_access_points

if __name__ ==  "__main__":
    access_points = load_access_points(config.access_points_file)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path=config.access_points_file,  recursive=False)
    observer.start()
    observer.join()

