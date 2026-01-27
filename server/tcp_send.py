import socket
import struct
import time
# from ip import now_ip

# HOST = now_ip() #local host
# HOST_second = '192.168.1.62'
# PORT = 3333 #port number


def send_data(HOST, PORT, x_self, y_self, angle_self, x_target, y_target, delay=0.05):
    print("TCP Server is running...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Socket created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT)) #привязка сокета к адресу и порту
        print("Socket bind complete")
        s.listen() #прослушивание входящих подключений
        print("Socket is listening")
        conn, addr = s.accept() #принятие входящего подключения
        while True:
            print('Connected by', addr) 
            x_self, y_self, angle_self, x_target, y_target  #данные для отправки
            data = struct.pack('5f', x_self, y_self, angle_self, x_target, y_target)  #упаковка данных в байты
            conn.send(data) #отправка данных клиенту
            time.sleep(delay)
            
