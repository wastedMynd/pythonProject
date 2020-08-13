# Client implementation

import socket
from enum import Enum
import cv2 as camera_vision
import pickle
import numpy as np

# WINDOW DIMENSIONS
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# WEB CAMERA PROPERTIES
WEB_CAMERA_WIDTH_PROPERTY = 3
WEB_CAMERA_HEIGHT_PROPERTY = 4
WEB_CAMERA_DEVICE_ID_PROPERTY = 0
WEB_CAMERA_BRIGHTNESS_PROPERTY = 10


class SocketConnectionStatus(Enum):
    PENDING = 0
    RUNNING = 1
    STOPPED = 2
    pass


class Client:
    # connection port
    __SERVER_PORT = 1989

    # local server's IPv4 ADDRESS
    __SERVER_IP_ADDRESS = socket.gethostbyname(socket.gethostname())

    # Server Socket
    __client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Protocol Bytes Accepted.
    __PROTOCOL_BYTES_ACCEPTED = 4096  # 1 Kilo Byte of information, is accepted; by this Server.

    # Protocol Communication Format.
    __PROTOCOL_FORMAT = "unicode_escape"  # "utf-8"

    # Disconnect Message
    __DISCONNECT_MESSAGE = "!DISCONNECT_MESSAGE"

    def __init__(self):
        self.display_client_connection_info()
        self.client_socket_connection_status = SocketConnectionStatus.PENDING
        self.display_socket_connection_status()
        pass

    def __set_client_socket_connection_status(self, to_socket_connection_status):
        self.client_socket_connection_status = to_socket_connection_status
        pass

    def get_client_socket_connection_status(self):
        return self.client_socket_connection_status

    def display_socket_connection_status(self):
        print()
        print(f"[CLIENT SOCKET CONNECTION STATUS] {self.get_client_socket_connection_status().name.lower()}...")
        pass

    def display_client_connection_info(self):
        print()
        print(f"[SERVER CONNECTION INFO] {self.__SERVER_IP_ADDRESS}:{self.__SERVER_PORT}")
        pass

    def start_client_connection_to_server(self):
        # Server Connection BINDER
        server_connection_binder = (self.__SERVER_IP_ADDRESS, self.__SERVER_PORT)

        # Connect this Client to Server.
        self.__client_socket.connect(server_connection_binder)

        # set server_socket_connection_status to SocketConnectionStatus.RUNNING
        self.__set_client_socket_connection_status(SocketConnectionStatus.RUNNING)

        # display_socket_connection_status
        self.display_socket_connection_status()

        pass

    def send_message_to_server(self, message):
        client_message_to_server = message.encode(self.__PROTOCOL_FORMAT)

        length_of_client_message_to_server = len(client_message_to_server)

        send_length_of_client_message_to_server = str(length_of_client_message_to_server).encode(self.__PROTOCOL_FORMAT)

        send_length_of_client_message_to_server += \
            b' ' * (self.__PROTOCOL_BYTES_ACCEPTED - len(send_length_of_client_message_to_server))

        self.__client_socket.send(send_length_of_client_message_to_server)

        self.__client_socket.send(client_message_to_server)

        pass

    def receive_message_from_server(self):
        server_message_response = self.__client_socket.recv(self.__PROTOCOL_BYTES_ACCEPTED).decode(self.__PROTOCOL_FORMAT)
        print("[RESPONSE] ", server_message_response)
        print()
        pass

    def stop_client_connection_to_clients(self):
        try:
            self.send_message_to_server(self.__DISCONNECT_MESSAGE)
        finally:
            self.__set_client_socket_connection_status(SocketConnectionStatus.STOPPED)
            self.display_socket_connection_status()
        pass

    pass


class ClientApp:

    def __init__(self):
        self.client = Client()
        self.client.start_client_connection_to_server()
        self.isClientClosed = False
        pass

    def interact_with_server(self):

        print()

        print("[To Quit Type !!]")

        print()

        while not self.isClientClosed:

            try:
                client_message_to_server = str(input("[SEND A MESSAGE TO SERVER] "))

                print()

                if client_message_to_server == "!!":
                    self.__close_connection_to_server()
                else:
                    self.client.send_message_to_server(client_message_to_server)
                    self.client.receive_message_from_server()

            except KeyboardInterrupt:
                self.__close_connection_to_server()

            pass

        pass

    def __close_connection_to_server(self):
        self.isClientClosed = True
        self.client.stop_client_connection_to_clients()
        pass

    pass


app = ClientApp()
app.interact_with_server()
