import socket
import logging

logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [CLIENT] %(message)s')

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 45000)
    logging.warning(f"Membuka koneksi ke {server_address}")
    sock.connect(server_address)

    try:
        while True:
            pesan = input("Ketik perintah (TIME / QUIT): ").strip().upper()
            if pesan not in ['TIME', 'QUIT']:
                print("Hanya boleh memasukkan 'TIME' atau 'QUIT'")
                continue

            kirim = pesan + '\r\n'  # Sesuai spesifikasi tugas (char 13 dan 10)
            sock.sendall(kirim.encode())
            logging.warning(f"Mengirim: {pesan}")

            data = sock.recv(64).decode().strip()
            logging.warning(f"Balasan: {data}")

            if pesan == 'QUIT':
                break

    finally:
        logging.warning("Menutup koneksi")
        sock.close()

if __name__ == '__main__':
    kirim_data()

