import socket
import os
import string
import hw1_utils
# from pdfminer import high_level

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888


def validate_http(http_dict, conn):
    # TODO return erros status
    pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            print(f"Connected to {addr}")

            with conn:
                data = conn.recv(4096)
                if not data:
                    # TODO: add error message
                    conn.close()
                    continue
                conn.sendall(data)
            http_dict = hw1_utils.decode_http(data)
            if not validate_http(http_dict, conn):
                conn.close()
                continue
            request = http_dict['Request']
            print(f"Request: {request}")
            conn.close()


if __name__ == "__main__":
    main()

