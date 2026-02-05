import socket
import struct

def receive_data(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # подключение к серверу
        while True:
            data = s.recv(20)
            values = struct.unpack('iiiii', data)# получение данных от сервера
            print('Received', values)  # вывод полученных данных