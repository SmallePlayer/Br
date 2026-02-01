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

cap = config.open_camera(0)
config.configure_camera(cap, '720')
config.start_camera_threaded(cap)
frame_id = 0
all_time = 0
while True:
    start_time = time.time()

    frame = config.get_frame_threaded()
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
    if frame_id >= 30:
        print(f"all_time: {all_time}")
        config.stop_camera_thread()
        break
    else:
        print(f"Кадр:{frame_id} | time:{end_time - start_time} sec")
    
cap.release()
s.close()