import socket
import struct
import time
import cv2
import numpy as np

from ip import now_ip
from sockets import create_udp_socket as create_socket

HOST = 'localhost' #now_ip() #local host
PORT = 3333 #port number

HOST_recv = 'localhost' #now_ip() # IP адрес сервера
PORT_recv = 3333      # порт сервера


def send_video(s, HOST_recv, PORT_recv, frame):
    _, compressed = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    data = compressed.tobytes()
    if len(data) < 60000:  # Меньше 60KB
        s.sendto(data, (HOST_recv, PORT_recv))


def send_data(s, HOST_recv, PORT_recv, delay=0.05):
    data = struct.pack('2f', 2.0, 3.0)  #упаковка данных в байты
    s.sendto(data, (HOST_recv, PORT_recv)) #отправка данных клиенту
    time.sleep(delay)
     
     
s = create_socket()
while True:     
    send_data(s, HOST_recv, PORT_recv)