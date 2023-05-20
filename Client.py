import socket
import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import datetime
import json
import os.path
import re
############################################## Variablen ##############################################
pc_name = ""
cpu_usage = 0
memory_usage = 0
current_time = ""
server_host = ""
server_port = 0
client_socket = None
############################################## Funktionen ##############################################
def get_pc_name():
    pc_name = platform.node()
    return pc_name

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_ram_usage():
    ram_usage = psutil.virtual_memory().percent
    return ram_usage

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time
def add_to_json():
    try:
        # Load existing data from the JSON file
        with open("config_client.json", 'r') as file:
            existing_data = json.load(file)

        # Increment the specified field value
        existing_data["send_total_stats"] += 1

        # Write the updated data back to the JSON file
        with open("config_client.json", 'w') as file:
            json.dump(existing_data, file, indent=4)

        #print("The value of 'send_total_stats' in 'config_client.json' has been incremented.")

    except Exception as e:
        print("An error occurred while updating the JSON file:", str(e))

############################################## Messages ##############################################
def show_connection_error_10061():
    tk.Tk().withdraw()
    messagebox.showerror("Verbindungsfehler", "[WinError 10061] Es konnte keine Verbindung hergestellt werden, da der Zielcomputer die Verbindung verweigerte.")
    exit()
def show_config_error_not_found():
    tk.Tk().withdraw()
    messagebox.showerror("Fehler", "Konfigurationsdatei nicht gefunden: config_client.json")
def show_config_success_message():
    tk.Tk().withdraw()
    messagebox.showinfo("Erfolgreich", "Die Konfiguration wurde erfolgreich erstellt.")
############################################## Config ##############################################
def read_config():
    config_file = "config_client.json"

    if not os.path.isfile(config_file):
        show_config_error_not_found()
        configure_server()
        return None

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config
def save_config(root, server_host, server_port):
    if not is_valid_ipv4(server_host):
        messagebox.showerror("Fehler", "Ungültige IPv4-Adresse")
        exit()
    if not is_valid_port(server_port):
        messagebox.showerror("Fehler", "Ungültiger Port")
        exit()
    root.destroy()

    config = {
        "server_host": server_host,
        "server_port": int(server_port),
        "first_connection": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "send_total_stats": 0,
    }

    with open('config_client.json', 'w') as f:
        json.dump(config, f, indent=4)

    show_config_success_message()
    exit()
def configure_server():
    root = tk.Tk()
    root.title("Server-Konfiguration")

    host_label = tk.Label(root, text="Server-IP-Adresse:")
    host_entry = tk.Entry(root)
    port_label = tk.Label(root, text="Server-Port:")
    port_entry = tk.Entry(root)

    host_label.pack()
    host_entry.pack()
    port_label.pack()
    port_entry.pack()

    ok_button = tk.Button(root, text="OK", command=lambda: save_config(root, host_entry.get(), port_entry.get()))
    ok_button.pack()

    root.mainloop()
############################################## Utils ##############################################
def is_valid_ipv4(ip):
    pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    return pattern.match(ip)
def is_valid_port(port):
    pattern = re.compile(r"\b(?:[0-9]{1,5})\b")
    return pattern.match(port)
############################################## Connection-to-Server ##############################################
def send_data(server_host, server_port):
    # Verbinde mit dem Server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))

        # Sende die Daten an den Server
        data = f"{pc_name};{cpu_usage};{memory_usage};{current_time}"
        client_socket.sendall(data.encode())
        add_to_json()
        print(f"Daten erfolgreich gesendet: {data}")

    except ConnectionRefusedError:
        show_connection_error_10061()
        exit()

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
        print(f"Verbindung hergestellt zu: {server_host}:{server_port}")
        while True:
            cpu_usage = get_cpu_usage()
            current_time = get_time()
            memory_usage = get_ram_usage()
            send_data(server_host, server_port)