import socket

HOST = '0.0.0.0' #local host
HOST_esp = '192.168.1.62' #esp32-c3 address
PORT = 3333 #port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # созданием самого сокета с ipv4 и tcp
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.bind((HOST, PORT)) #привязка сокета к адресу и порту
    s.listen() #прослушивание входящих подключений
    conn, addr = s.accept() #принятие входящего подключения
    with conn: #работа с подключением
        print('Connected by', addr) 
        while True:
            data = conn.recv(1024) #получение данных от клиента
            if not data:
                break
            conn.sendall(data) #отправка данных обратно клиенту
            
