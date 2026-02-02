import config
import socket
import struct
import time 

from sockets import create_udp_socket

HOST = 'localhost'
PORT = 3333

s = create_udp_socket()

def send__small_video(data, frame_id):
    header = struct.pack('!I',  frame_id)
    packet = header + data
    s.sendto(packet, (HOST, PORT))
    

cap1 = config.CameraThread(index=0) # Инициализация многопоточного захвата с камеры
cap1.start() # Запуск захвата с камеры


frame_id = 0
all_time = 0
while True:
    start_time = time.time()

    frame = cap1.get_frame() # Получение кадра с камеры
    if frame is None:
        continue
    data = config.compress_jpeg(frame)
    
    if len(data) > 60000:
        print("Слишком большой кадр!!!")
        break
    
    send__small_video(data, frame_id)
    frame_id += 1
    end_time = time.time()
    all_time += end_time - start_time
    if frame_id >= 100:
        print(f"all_time: {all_time}")
        cap1.stop()
        break
    else:
        print(f"Кадр:{frame_id} | time:{end_time - start_time} sec")
    
