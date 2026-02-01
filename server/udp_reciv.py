import socket
import struct
import cv2
import numpy as np

from ip import now_ip
from sockets import create_udp_socket as create_socket
from sockets import bind_socket

HOST = 'localhost' #now_ip()  # IP адрес сервера
PORT = 3333      # порт сервера


def recive_video(s):
    data, addr = s.recvfrom(70000)
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    
    cv2.imshow('Stream', frame)
    print(f"Кадр получен: {len(data)} байт")
                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)


def receive_data(s):
    data, addr = s.recvfrom(20)
    values = struct.unpack('2f', data)# получение данных от сервера
    print('Received', values, 'from', addr)  # вывод полученных данных


s = create_socket()
bind_socket(s, HOST, PORT)

while True:    
    receive_data(s)