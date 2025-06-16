from socket import *
import socket
import threading
import logging
import time
import sys

logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] %(message)s')

def proses_string(request_string):
    logging.warning(f"[SERVER] Memproses permintaan: {request_string.strip()}")
    balas = "ERROR\r\n"
    if (request_string.startswith("TIME") and request_string.endswith("\n")):
        from datetime import datetime
        now = datetime.now()
        waktu = now.strftime("%d-%m-%Y %H:%M:%S")
        balas = f"JAM {waktu}\r\n"
    elif (request_string.startswith("QUIT") and request_string.endswith("\n")):
        balas = "XXX"
    return balas

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"[SERVER] Mulai menangani koneksi dari {self.address}")
        while True:
            data = self.connection.recv(32)
            if data:
                request_s = data.decode()
                logging.warning(f"[SERVER] Diterima dari {self.address}: {request_s.strip()}")
                balas = proses_string(request_s)
                if (balas == "XXX"):
                    logging.warning(f"[SERVER] Menutup koneksi dari {self.address}")
                    self.connection.close()
                    break
                logging.warning(f"[SERVER] Mengirim balasan ke {self.address}: {balas.strip()}")
                self.connection.sendall(balas.encode())
            else:
                logging.warning(f"[SERVER] Tidak ada data dari {self.address}, menutup koneksi")
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("[SERVER] Menunggu koneksi di port 45000 ...")
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"[SERVER] Koneksi masuk dari {self.client_address}")
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()

