from multiprocessing.connection import Listener
import config

listener = Listener((config.server_address, config.server_port))

def calculate_changes(access_points, updated_access_points): 
    # loop through records to find changed records
    for access_point in access_points["access_points"]:
        is_found = False # flag variable to check if record has been deleted
        for updated_access_point in updated_access_points["access_points"]:
            if access_point["ssid"] == updated_access_point["ssid"]:
                is_found = True
                if access_point["snr"] != updated_access_point["snr"]:
                    print("%s SNR has changed from %s to %s" % (access_point["ssid"], access_point["snr"], updated_access_point["snr"]))
                if access_point["channel"] != updated_access_point["channel"]:
                    print("%s channel has changed from %s to %s" % (access_point["ssid"], access_point["channel"], updated_access_point["channel"]))
        if is_found == False:
             print("%s is removed from the list" % (access_point["ssid"]))
    # loop through updated records to find new records
    for updated_access_point in updated_access_points["access_points"]:
        is_new = True # flag variable to check if a new entry has been added
        for access_point in access_points["access_points"]:
            if updated_access_point["ssid"] == access_point["ssid"]:
                is_new = False
        if is_new == True:
            print("%s is added to the list with SNR %s and channel %s" % (updated_access_point["ssid"], updated_access_point["snr"], updated_access_point["channel"]))

if __name__ ==  "__main__":
    access_points = {}
    while True:
        conn = listener.accept()
        while True:
            msg = conn.recv()
            if msg == 'close connection':
                conn.close()
                break
            # check if we have access points in memory
            if access_points == {}:
                access_points = msg
            else:
                calculate_changes(access_points, msg)
                access_points = msg
listener.close()
