import socket
import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import datetime
import json
import os.path
############################################## Variablen ##############################################
pc_name = ""
cpu_usage = 0
current_time = ""
server_host = ""
server_port = 0
############################################## Funktionen ##############################################
def get_pc_name():
    pc_name = platform.node()
    return pc_name

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time

############################################## Error-Messages ##############################################
def show_connection_error_10061():
    tk.Tk().withdraw()
    messagebox.showerror("Verbindungsfehler", "[WinError 10061] Es konnte keine Verbindung hergestellt werden, da der Zielcomputer die Verbindung verweigerte.")
def show_config_error_not_found():
    tk.Tk().withdraw()
    messagebox.showerror("Fehler", "Konfigurationsdatei nicht gefunden: config.json")

############################################## Config ##############################################
def read_config():
    config_file = "config.json"

    if not os.path.isfile(config_file):
        show_config_error_not_found()
        return create_default_config("config.json")

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config
def create_default_config(config_file):
    default_config = {
        "server_host": "localhost",
        "server_port": 1234,
    }

    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=4)

############################################## Connection-to-Server ##############################################
def send_data(server_host, server_port):
    # Verbinde mit dem Server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        print(f"Verbindung hergestellt zu: {server_host}:{server_port}")

        # Sende die Daten an den Server
        data = f"{pc_name};{cpu_usage};{current_time}"
        client_socket.sendall(data.encode())
        print(f"Daten erfolgreich gesendet: {data}")

    except ConnectionRefusedError:
        show_connection_error_10061()

    finally:
        # Schließe die Verbindung
        client_socket.close()

############################################## Main ##############################################
if __name__ == '__main__':
    config = read_config()
    pc_name = get_pc_name()

    if config is not None:
        server_host = config.get('server_host')
        server_port = config.get('server_port')
        while True:
            cpu_usage = get_cpu_usage()
            current_time = get_time()
            send_data(server_host, server_port)