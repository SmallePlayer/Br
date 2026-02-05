import socket
import struct
import cv2
import numpy as np

#функция для получения данных по udp
def receive_data(s, list_variable):
    data, _ = s.recvfrom(20)
    values = list(struct.unpack(f"{len(list_variable)}f", data))# получение данных от сервера
    return values