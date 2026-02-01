import socket

def create_udp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def create_tcp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def bind_socket(s, HOST, PORT):
    s.bind((HOST, PORT))