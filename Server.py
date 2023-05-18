import socket
import csv
import threading

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
    server_socket.bind((host, port))

    # Warte auf eingehende Verbindungen
    server_socket.listen(5)
    print(f"Der Server wartet auf eingehende Verbindungen auf {host}:{port}")

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

if __name__ == '__main__':
    host = '192.168.0.141'  # Server-Host
    port = 1234  # Server-Port

    start_server(host, port)
