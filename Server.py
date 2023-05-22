import socket
import csv
import threading
import datetime
import tkinter as tk
from tkinter import messagebox
import json
import os.path
import logging
############################################## Variablen ##############################################
host = ""
port = 0
############################################## Funktionen ##############################################
def handle_client(client_socket, client_address):
    try:
        logging.info(get_time() + "Verbindung hergestellt von: " + str(client_address))
        print(f"Verbindung hergestellt von: {client_address}")

        # Empfange die Daten vom Client
        logging.info(get_time() + "Empfange Daten von: " + str(client_address))
        data = client_socket.recv(1024).decode()

        # Speichere die Daten in einer CSV-Datei
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.split(';'))
        logging.info(get_time() + "Daten empfangen und in 'data.csv' gespeichert: " + data)
        print(f"Daten empfangen und in 'data.csv' gespeichert: {data}")

    except ConnectionResetError:
        logging.error(get_time() + "Verbindung von " + str(client_address) + " unerwartet geschlossen.")
        print(f"Verbindung von {client_address} unerwartet geschlossen.")

    finally:
        # Schließe die Verbindung zum Client
        client_socket.close()
        print(f"Verbindung geschlossen von: {client_address}")
        logging.info(get_time() + "Verbindung geschlossen von: " + str(client_address))

def start_server(host, port):
    try:
        # Erstelle einen Socket
        logging.info(get_time() + "Erstelle einen Socket")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binde den Socket an die angegebene Adresse und Port
        logging.info(get_time() + "Binde den Socket an die angegebene Adresse und Port")
        server_socket.bind((server_host, server_port))
        # Warte auf eingehende Verbindungen
        logging.info(get_time() + "Warte auf eingehende Verbindungen")
        server_socket.listen(5)
        print(f"Der Server wartet auf eingehende Verbindungen auf {server_host}:{server_port}")
        while True:
            # Akzeptiere eine eingehende Verbindung
            client_socket, client_address = server_socket.accept()
            logging.info(get_time() + "Akzeptiere eine eingehende Verbindung")


            # Starte einen Thread zur Verarbeitung des Clients
            logging.info(get_time() + "Starte einen Thread zur Verarbeitung des Clients")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except OSError as e:
        if e.errno == 10048:
            show_socket_error_10048()
            logging.error(get_time() + "Socketadresse wird bereits verwendet.")
    finally:
        server_socket.close()
        logging.info(get_time() + "Server wurde beendet.")
        print("Server wurde beendet.")

############################################## Messages ##############################################
def show_config_error_not_found():
    tk.Tk().withdraw()
    messagebox.showerror("Fehler", "Konfigurationsdatei nicht gefunden: config_server.json")
    logging.error(get_time() + "Konfigurationsdatei nicht gefunden: config_server.json")
def show_config_success_message():
    tk.Tk().withdraw()
    messagebox.showinfo("Erfolgreich", "Die Konfiguration wurde erfolgreich erstellt.")
    logging.info(get_time() + "Die Konfiguration wurde erfolgreich erstellt.")
def show_socket_error_10048():
    tk.Tk().withdraw()
    messagebox.showerror("Fehler", "[WinError 10048] Die angegebene Socketadresse wird bereits verwendet.")
    logging.error(get_time() + "[WinError 10048] Die angegebene Socketadresse wird bereits verwendet.")
    exit()

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

    logging.info(get_time() + "Konfigurationsdatei wurde erstellt.")
    show_config_success_message()
    exit()


############################################## Utils ##############################################

def get_time():
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S ")
    return current_time


############################################## Main ##############################################
if __name__ == '__main__':
    # Logging
    #logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    config = read_config()
    if config is not None:
        server_host = config.get('server_host')
        server_port = config.get('server_port')
        # Thread für den Server
        server_thread = threading.Thread(target=start_server, args=(server_host, server_port))
        server_thread.start()
