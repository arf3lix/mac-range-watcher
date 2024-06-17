import os
import time
import threading
from queue import Queue
from utils.config import mac_start, mac_end, trackcsv_path, blue_limit, yellow_limit, red_limit
from utils.models import Colors
from watcher.watchdog import Watchdog
from utils.logger import get_logger
from gui.popups import custom_popup
from plyer import notification

import os

_logger = get_logger(__name__)


def main():
    file_path = r'TrackMac.csv'
    gui_queue = Queue()
    

    def gui_thread(gui_queue):
        while True:
            try:
                if not gui_queue.empty():
                    title, message, bg_color = gui_queue.get()
                    custom_popup(title, message, bg_color)
            except Exception as e:
                _logger.error(e)
                time.sleep(5)
                continue


    threading.Thread(target=gui_thread, args=(gui_queue,), daemon=True).start()

    while True:
        try:
            
            trackmacs_file_path = rf"{os.path.join(trackcsv_path, file_path)}"
            check_mac_in_range(trackmacs_file_path, mac_start, mac_end, gui_queue, initial_check=True)
            wd = Watchdog(trackmacs_file_path, validate_trackfile, gui_queue)
            wd.start()
        except Exception as e:
            _logger.error(e)
            time.sleep(5)  # Delay before restarting to avoid rapid restart loops
            continue


# Function to validate the track file
def validate_trackfile(file_path, mac_range_start, mac_range_end, gui_queue):
    try:
        lines = read_trackfile(file_path)

        #print(lines)
        data = extract_data(lines)

        valid_trackfile = True

        if isinstance((non_consecutive_macs := validate_consecutive(data)), str) and non_consecutive_macs:
            gui_queue.put(("Validation Failed", f"Mac address no consecutivas :\n{non_consecutive_macs},\n llamar a ingenieria", Colors.RED))
            valid_trackfile = False

        if isinstance((duplicated_mac := check_duplicates(data)), str) and duplicated_mac:
            gui_queue.put(("Validation Failed", f"mac {duplicated_mac} duplicada,\n llamar a ingenieria", Colors.RED))
            valid_trackfile = False
        if not check_mac_in_range(file_path, mac_range_start, mac_range_end, gui_queue):
            valid_trackfile = False

        
        if valid_trackfile:
            # Enviar la notificación exitosa
            notification.notify(
                title="Nuevo registro de UUT",
                message="se acaba de registrar exitosamente un nuevo mac address",
                app_name="Mac Address Watcher",  # Nombre de la aplicación (opcional)
                timeout=5  # Duración de la notificación en segundos
            )
    except Exception as e:
        _logger.error(e)
        

def read_trackfile(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    return lines

def extract_data(lines):
    try:
        data = []
        for line in lines:
            parts = line.split(',')
            if len(parts) == 6:
                label_serial, inner_serial, date, code, mac_address, _ = parts
                data.append((label_serial, inner_serial, mac_address))
        return data
    except Exception as e:
        _logger.error(e)        

def validate_consecutive(data):
    mac_addresses = [int(item[2], 16) for item in data]

    for i in range(1, len(mac_addresses)):
        if mac_addresses[i] != mac_addresses[i-1] + 1:
            print(f"MAC addresses not consecutive at index {i}: {mac_addresses[i-1]} -> {mac_addresses[i]}")
            return f"{hex(mac_addresses[i-1]).upper()} != {hex(mac_addresses[i]).upper()}"

def check_duplicates(data):
    seen_mac_addresses = set()

    mac_addresses = [item[2] for item in data]

    for mac in mac_addresses:
        if mac in seen_mac_addresses:
            print(f"Duplicate MAC address found: {mac}")
            return mac

        seen_mac_addresses.add(mac)

def check_mac_in_range(file_path, mac_range_start, mac_range_end, gui_queue, initial_check=False):
    try:
        def mac_to_int(mac):
            return int(mac, 16)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if not lines:
            _logger.info("File is empty")
            return False

        last_line = lines[-1].strip()
        mac_address = last_line.split(',')[4]

        if initial_check:
            _logger.info("restarted...")

        
        mac_start_int = mac_to_int(mac_range_start)
        mac_end_int = mac_to_int(mac_range_end)
        mac_last_int = mac_to_int(mac_address)

        if mac_start_int <= mac_last_int <= mac_end_int:
            macs_left = mac_end_int - mac_last_int
            if macs_left < int(red_limit):
                gui_queue.put(("Alerta", f"quedan {macs_left} mac address", Colors.RED))
                return False
            elif initial_check:
                if macs_left < int(yellow_limit):
                    gui_queue.put(("Alerta", f"quedan {macs_left} mac address", Colors.ORANGE))
                    return False
                elif macs_left < int(blue_limit):
                    gui_queue.put(("Alerta", f"quedan {macs_left} mac address", Colors.YELLOW))
                    return False
        else:
            return False
        
        return True
    except Exception as e:
        _logger.error(e)
        gui_queue.put(("Alerta", f"Error inesperado,\nrevisar archivo trackmac.csv", Colors.RED))
        
        

if __name__ == "__main__":
    main()