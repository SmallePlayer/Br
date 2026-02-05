import config
import socket
import struct
import time 

from sockets import create_udp_socket

#функция для отправки видео по udp с максимальным размером в 60000 байт.
def send__small_video(sock, HOST, PORT, data, frame_id):
    header = struct.pack('!I',  frame_id)
    packet = header + data
    sock.sendto(packet, (HOST, PORT))
    
# функция для отправки видео по udp с поддержкой разбиения на куски при размере кадра более 60000 байт.  
def send_big_video(sock, HOST, PORT, data, frame_id):
    CHUNK_SIZE = 60000
    
    data_size = len(data)
        
    # Считаем куски
    num_chunks = (data_size + CHUNK_SIZE - 1) // CHUNK_SIZE
        
    # Отправляем каждый кусок
    for chunk_idx in range(num_chunks):
        start = chunk_idx * CHUNK_SIZE
        end = min(start + CHUNK_SIZE, data_size)
        chunk = data[start:end]
        
        # Заголовок: frame_id (I) + chunk_idx (H) + num_chunks (H) + data_size (I)
        header = struct.pack('!IHHI', frame_id, chunk_idx, num_chunks, data_size)
        packet = header + chunk
        
        try:
            sock.sendto(packet, (HOST, PORT))
            # Небольшая задержка между отправкой пакетов для предотвращения потерь
            time.sleep(0.001)  # 1мс задержка
        except Exception as e:
            print(f"Ошибка отправки chunk {chunk_idx} для frame {frame_id}: {e}")
            break
        