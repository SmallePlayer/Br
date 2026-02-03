import config
import cv2
import socket
import struct
import numpy as np
import time

import sockets

HOST = 'localhost'
PORT = 3333

s = sockets.create_udp_socket()
sockets.bind_socket(s, HOST, PORT)
s.settimeout(5.0)

def recv_small_video(sock, data):
    
    frame_id = struct.unpack('!I', data[:4])[0]
    jpeg_data = data[4:]
    return config.decompress_frame(jpeg_data), frame_id

def reciv_big_video(sock, data):
    # Статические переменные для сохранения состояния между вызовами
    if not hasattr(reciv_big_video, 'current_frame_id'):
        reciv_big_video.current_frame_id = -1
        reciv_big_video.chunks = {}
        reciv_big_video.expected_chunks = 0
    
    if len(data) < 12:
        return None
        
    # Распаковываем заголовок
    frame_id, chunk_idx, num_chunks, data_size = struct.unpack('!IHHI', data[:12])
    chunk_data = data[12:]
        
    # Новый кадр - сбрасываем старый
    if frame_id > reciv_big_video.current_frame_id:
        reciv_big_video.current_frame_id = frame_id
        reciv_big_video.chunks = {}
        reciv_big_video.expected_chunks = num_chunks
        
    # Старый кадр - игнорируем
    if frame_id < reciv_big_video.current_frame_id:
        return None
        
    # Сохраняем кусок для текущего кадра
    if frame_id == reciv_big_video.current_frame_id:
        reciv_big_video.chunks[chunk_idx] = chunk_data
            
        # Собрали все куски?
        if len(reciv_big_video.chunks) == reciv_big_video.expected_chunks:
            # Собираем кадр в правильном порядке
            full_data = b''.join(reciv_big_video.chunks[i] for i in range(reciv_big_video.expected_chunks))
            frame = config.decompress_frame(full_data)
            if frame is not None:
                cv2.imshow('UDP Chunked', frame)
                print(f"Кадр {frame_id}: {len(full_data)/1024:.1f} KB")
            
            # Очищаем буфер для следующего кадра
            reciv_big_video.chunks = {}
            return frame
    
    return None
    
    

while True:
    data, addr = s.recvfrom(65535)
    
    frame = reciv_big_video(s, data)
    
    #frame, frame_id = recv_small_video(s, data)
    
    #cv2.imshow('UDP Simple', frame)
    # print(f"Кадр {frame_id} получен")
            
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    

