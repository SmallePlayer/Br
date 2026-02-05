import socket


# Функция для создания UDP сокета
def create_udp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Функция для привязки сокета к адресу и порту
def create_tcp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Функция для привязки сокета к адресу и порту
def bind_socket(s, HOST, PORT):
    s.bind((HOST, PORT))