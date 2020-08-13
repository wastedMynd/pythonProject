# Server implementation

import socket
import threading
from enum import Enum
import cv2 as camera_vision
import pickle

# WINDOW DIMENSIONS
WINDOW_WIDTH = 50
WINDOW_HEIGHT = 50

# WEB CAMERA PROPERTIES
WEB_CAMERA_WIDTH_PROPERTY = 3
WEB_CAMERA_HEIGHT_PROPERTY = 4
WEB_CAMERA_DEVICE_ID_PROPERTY = 0
WEB_CAMERA_BRIGHTNESS_PROPERTY = 10

# SETUP CAPTURED VIDEO STREAM
captured_video_stream = camera_vision.VideoCapture(WEB_CAMERA_DEVICE_ID_PROPERTY)
captured_video_stream.set(WEB_CAMERA_WIDTH_PROPERTY, WINDOW_WIDTH)
captured_video_stream.set(WEB_CAMERA_HEIGHT_PROPERTY, WINDOW_HEIGHT)
captured_video_stream.set(WEB_CAMERA_BRIGHTNESS_PROPERTY, 50)


class SocketConnectionStatus(Enum):
    PENDING = 0
    RUNNING = 1
    STOPPED = 2


class Server:
    # connection port
    __SERVER_PORT = 1989

    # local server's IPv4 ADDRESS
    __SERVER_IP_ADDRESS = socket.gethostbyname(socket.gethostname())

    # Server Socket
    __server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Server Connection BINDER
    __SERVER_CONNECTION_BINDER = (__SERVER_IP_ADDRESS, __SERVER_PORT)

    # Bind server_socket
    __server_socket.bind(__SERVER_CONNECTION_BINDER)

    # Protocol Bytes Accepted.
    __PROTOCOL_BYTES_ACCEPTED = 4096  # 1 Kilo Byte of information, is accepted; by this Server.

    # Protocol Communication Format.
    __PROTOCOL_FORMAT = "unicode_escape"  # "utf-8"

    # Disconnect Message
    __DISCONNECT_MESSAGE = "!DISCONNECT_MESSAGE"

    def __init__(self):
        self.display_server_connection_info()
        self.server_socket_connection_status = SocketConnectionStatus.PENDING
        self.display_socket_connection_status()
        pass

    def __set_server_socket_connection_status(self, to_socket_connection_status):
        self.server_socket_connection_status = to_socket_connection_status
        pass

    def get_server_socket_connection_status(self):
        return self.server_socket_connection_status

    def display_socket_connection_status(self):
        print()
        print(f"[SERVER SOCKET CONNECTION STATUS] {self.get_server_socket_connection_status().name.lower()}...")
        pass

    def display_server_connection_info(self):
        print()
        print(f"[SERVER CONNECTION INFO] {self.__SERVER_IP_ADDRESS}:{self.__SERVER_PORT}")
        pass

    def __initiate_client_connection(self, client_connection, client_address):

        print()

        print(f"[NEW CLIENT CONNECTED TO SERVER] {client_address}:{client_connection}")

        self.display_active_client_connection_count()

        print()

        is_client_connected = True

        # Server listens, to incoming client Messages.
        while is_client_connected:

            print()

            client_message_length = int(
                client_connection.recv(self.__PROTOCOL_BYTES_ACCEPTED).decode(self.__PROTOCOL_FORMAT))

            if client_message_length:

                client_message = client_connection.recv(client_message_length).decode(self.__PROTOCOL_FORMAT)

                print(f"[CLIENT {client_address}, SENT A MESSAGE TO SERVER; THAT READS] {client_message}")

                client_connection.send(f"eho, {client_message}".encode(self.__PROTOCOL_FORMAT))

                # When the client sends the self.__DISCONNECT_MESSAGE,
                # Server must stop listening; to client's messages.
                if client_message == self.__DISCONNECT_MESSAGE:
                    is_client_connected = False
                    client_connection.close()
                elif client_message == "s":
                    try:
                        success, image_stream = captured_video_stream.read()
                        if success:
                            for data in image_stream:
                                client_connection.send(pickle.dumps(data).decode(encoding=bytes))
                    finally:
                        if camera_vision.waitKey(1) & 0xFF == ord('z'):
                            break
            pass
        pass

    def start_server_connection_to_clients(self):
        # set server_socket_connection_status to SocketConnectionStatus.RUNNING
        self.__set_server_socket_connection_status(SocketConnectionStatus.RUNNING)

        # display_socket_connection_status
        self.display_socket_connection_status()

        # Start listening to clients; caution, this operation is Blocking.
        self.__server_socket.listen()

        # Server will remain connected to its Clients; until Connection is Stopped.
        while self.get_server_socket_connection_status() == SocketConnectionStatus.RUNNING:

            try:
                # Server will now accept, new Client Connection.
                client_connection, client_address = self.__server_socket.accept()

                if client_connection and client_address:
                    # Spawn a thread, that connects a client; to this Server.
                    threading.Thread(target=self.__initiate_client_connection(client_connection, client_address),
                                     args=(client_connection, client_address)).start()

            except KeyboardInterrupt:
                self.stop_server_connection_to_clients()
        pass

    def display_active_client_connection_count(self):
        print()
        if threading:
            active_client_count = threading.activeCount()
            if active_client_count >= 1:
                print(f"[ACTIVE CLIENTS ON SERVER SOCKET CONNECTION] {active_client_count}")
            else:
                print("[NO ACTIVE CLIENT ON SERVER SOCKET CONNECTION]")
        pass

    def stop_server_connection_to_clients(self):
        self.__set_server_socket_connection_status(SocketConnectionStatus.STOPPED)
        self.display_active_client_connection_count()
        self.display_socket_connection_status()
        pass

    pass


class ServerApp:
    def __init__(self):
        self.server = Server()
        self.server.start_server_connection_to_clients()
        pass

    pass


serverApp = ServerApp()
