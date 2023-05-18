import socket
import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import datetime

pc_name = ""
cpu_usage = 0
current_time = ""
def get_pc_name():
    pc_name = platform.node()
    return pc_name

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time

def show_error_message():
    tk.Tk().withdraw()
    messagebox.showerror("Verbindungsfehler", "[WinError 10061] Es konnte keine Verbindung hergestellt werden, da der Zielcomputer die Verbindung verweigerte.")

def send_data(server_host, server_port, data):
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
        show_error_message()

    finally:
        # Schließe die Verbindung
        client_socket.close()

if __name__ == '__main__':
    server_host = 'localhost'  # Server-Host
    server_port = 1234  # Server-Port
    data = 'Hallo, Server!'  # Daten, die an den Server gesendet werden sollen
    #while True:
        #send_cpu_usage(server_host, server_port)


