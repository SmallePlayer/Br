import socket
import struct
import time
import cv2
import numpy as np


#функция по отправке данных по udp
def send_data(s, HOST_recv, PORT_recv, list_variable, delay=0.05):
    data = struct.pack(f"{len(list_variable)}f", *list_variable)  #упаковка данных в байты
    s.sendto(data, (HOST_recv, PORT_recv)) #отправка данных клиенту
    time.sleep(delay)
    return True
     
