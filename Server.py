import socket
import csv
import threading
import re
import tkinter as tk
from tkinter import messagebox
import json
import os.path
############################################## Variablen ##############################################
host = ""
port = 0
############################################## Funktionen ##############################################
def handle_client(client_socket, client_address):
    try:
        print(f"Verbindung hergestellt von: {client_address}")

        # Empfange die Daten vom Client
        data = client_socket.recv(1024).decode()

        # Speichere die Daten in einer CSV-Datei
        with open('cpu_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.split(';'))

        print(f"Daten empfangen und in 'cpu_data.csv' gespeichert: {data}")

    except ConnectionResetError:
        print(f"Verbindung von {client_address} unerwartet geschlossen.")

    finally:
        client_socket.close()
        print(f"Verbindung geschlossen von: {client_address}")

def start_server(host, port):
    # Erstelle einen Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binde den Socket an die angegebene Adresse und Port
    server_socket.bind((server_host, server_port))

    # Warte auf eingehende Verbindungen
    server_socket.listen(5)
    print(f"Der Server wartet auf eingehende Verbindungen auf {server_host}:{server_port}")

    try:
        while True:
            # Akzeptiere eine eingehende Verbindung
            client_socket, client_address = server_socket.accept()

            # Starte einen Thread zur Verarbeitung des Clients
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    finally:
        server_socket.close()
        print("Server wurde beendet.")
############################################## Messages ##############################################
def show_config_error_not_found():
    tk.Tk().withdraw()
    messagebox.showerror("Fehler", "Konfigurationsdatei nicht gefunden: config_server.json")
def show_config_success_message():
    tk.Tk().withdraw()
    messagebox.showinfo("Erfolgreich", "Die Konfiguration wurde erfolgreich erstellt.")
############################################## Config ##############################################
def read_config():
    config_file = "config_server.json"

    if not os.path.isfile(config_file):
        show_config_error_not_found()
        save_config()
        show_config_success_message()
        return None

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config
def save_config():
    config = {
        "server_host": socket.gethostbyname(socket.gethostname()),
        "server_port": int(1234)
    }

    with open('config_server.json', 'w') as f:
        json.dump(config, f, indent=4)

    show_config_success_message()
    exit()
############################################## Utils ##############################################
def is_valid_ipv4(ip):
    pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    return pattern.match(ip)
def is_valid_port(port):
    pattern = re.compile(r"\b(?:[0-9]{1,5})\b")
    return pattern.match(port)
############################################## Main ##############################################
if __name__ == '__main__':
    config = read_config()
    if config is not None:
        server_host = config.get('server_host')
        server_port = config.get('server_port')
        start_server(host, port)
