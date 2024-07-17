import logging
import socket
import threading
from queue import Queue

# Configuration
HOST = '192.168.0.7'  # The server's IP address
PORT = 65432          # The port used by the server

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Server:
    def __init__(self):
        self.server_socket = None
        self.is_running = False
        self.connections = []
        self.connection_queue = Queue()
        self.lock = threading.Lock()

    def start_server(self):
        if self.is_running:
            logging.debug("Server is already running")
            return  # Server is already running
        self.is_running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        logging.info(f"Server started on {HOST}:{PORT}")
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()

    def accept_connections(self):
        while self.is_running:
            try:
                conn, addr = self.server_socket.accept()
                with self.lock:
                    self.connections.append((conn, addr))
                client_name = self.get_client_name(addr[0])
                logging.info(f"Connected by {addr} ({client_name})")
                self.connection_queue.put((addr[0], client_name))  # Notify GUI to update connections
                connection_thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
                connection_thread.start()
            except Exception as e:
                logging.error(f"Error accepting connections: {e}")

    def handle_connection(self, conn, addr):
        while self.is_running:
            try:
                data = conn.recv(1024)
                if not data:
                    break  # Exit the loop if the client closes the connection
                logging.debug(f"Received from {addr}: {data.decode()}")
                response = f"Server received: {data.decode()}"
                conn.sendall(response.encode())
            except ConnectionResetError:
                logging.warning(f"Connection reset by {addr}")
                break
            except Exception as e:
                logging.error(f"Error handling connection from {addr}: {e}")
                break
        with self.lock:
            self.connections = [c for c in self.connections if c[1] != addr]
        conn.close()
        logging.info(f"Connection closed: {addr}")
        self.connection_queue.put(None)  # Notify GUI to update connections

    def get_client_name(self, ip):
        try:
            host_name, _, _ = socket.gethostbyaddr(ip)
            return host_name
        except socket.herror:
            return "Unknown"

    def stop_server(self):
        if not self.is_running:
            logging.debug("Server is not running")
            return  # Server is not running
        self.is_running = False
        self.server_socket.close()
        self.accept_thread.join()
        with self.lock:
            for conn, _ in self.connections:
                conn.close()
        self.connections.clear()
        logging.info("Server stopped")

    def get_connections(self):
        with self.lock:
            connections = [(addr[0], self.get_client_name(addr[0])) for _, addr in self.connections]
            # Do not log empty connections
            if connections:
                logging.debug(f"Current connections: {connections}")
            return connections

# Create a global instance of the Server class
server_instance = Server()
