import socket
import time

HOST = '192.168.0.7'  # The server's IP address
PORT = 65432          # The port used by the server

def test_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                try:
                    s.sendall(b'Hello, Server!')
                    data = s.recv(1024)
                    if not data:
                        break  # Break the loop if the connection is closed
                    print('Received', data.decode())
                    time.sleep(5)  # Adjust as necessary for your use case
                except Exception as e:
                    print(f"Client error: {e}")
                    break
    except Exception as e:
        print(f"Client connection error: {e}")

if __name__ == "__main__":
    test_client()
