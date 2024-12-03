import socket
import threading
import ssl


class ProxyServer:
    def __init__(self, host='0.0.0.0', port=9090):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"VPN server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

    def handle_client(self, client_socket, addr):
        try:
            request = client_socket.recv(1024).decode()
            method, path, version = request.split('\r\n')[0].split()

            if method == "CONNECT":
                # Обработка HTTPS соединений
                https_host, https_port = path.split(':')
                https_host = https_host.strip('/')

                ssl_context = ssl.create_default_context()
                ssl_socket = ssl_context.wrap_socket(client_socket)

                https_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                https_socket.connect((https_host, int(https_port)))

                https_request = f"{method} /{path} HTTP/{version}\r\nHost: {https_host}\r\n\r\n"
                https_socket.sendall(bytes(https_request, 'utf-8'))

                https_response = bytes(https_socket.recv(4096))
                https_socket.close()

                client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

                # Перенаправление данных между клиентом и HTTPS соединением
                while True:
                    data = ssl_socket.recv(4096)
                    if not data:
                        break
                    https_socket.send(data)

                    data = https_socket.recv(4096)
                    if not data:
                        break
                    ssl_socket.send(data)
            else:
                # Обычное HTTP соединение
                response = b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello from VPN!"
                client_socket.sendall(response)
        finally:
            client_socket.close()


if __name__ == "__main__":
    proxy_server = ProxyServer(port=9090)
    proxy_server.start()