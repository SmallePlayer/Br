import socket
import struct
import time
from ip import now_ip

HOST = now_ip() #local host
HOST_esp = '192.168.1.62' #esp32-c3 address
PORT = 3333 #port number

def send_info_path(path, angle):
    print("TCP Server is running...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:# созданием самого сокета с ipv4 и tcp
        print("Socket created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT)) #привязка сокета к адресу и порту
        print("Socket bind complete")
        s.listen() #прослушивание входящих подключений
        print("Socket is listening")
        conn, addr = s.accept() #принятие входящего подключения
        while True:
        #with conn: #работа с подключением
            print('Connected by', addr) 
            
            data = struct.pack('2f', path, angle)  #данные для отправки
            conn.send(data) #отправка данных клиенту
            
            time.sleep(1)
            
