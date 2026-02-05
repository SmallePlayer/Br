import cv2 
import numpy as np
import struct
import threading

# Функция для сжатия кадра в JPEG формат
def compress_jpeg(frame, quality=60):
    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    success, compressed = cv2.imencode('.jpg', frame, encode_params)
    if not success:
        raise ValueError("Ошибка сжатия JPEG")
    return compressed.tobytes()

#функция для декодирования кадра из JPEG формата
def decompress_frame(data):
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame

        
# Класс многопоточного захвата с камеры
class CameraThread:
    def __init__(self, index=0, premission='720', buffer=1): # Инициализация камеры и параметров захвата
        self.cap = self.open_camera(index)
        self.configure_camera(premission, buffer)
        self.frame = None
        self._lock = threading.Lock()
        self._running = True
        self._thread = None
        
    def start(self): # Запуск потока захвата
        self._thread = threading.Thread(target=self.capture_loop)
        self._thread.start()
        
    def open_camera(self, index=0): # Открытие камеры по индексу
        return cv2.VideoCapture(index)
        
    def configure_camera(self,  permission='720', buffer=1): # Настройка параметров камеры
        if permission == '720':
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   
        elif permission == '1080':
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        elif permission == '2k':
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)   
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        elif permission == '4k':
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)   
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer) 
        
    def capture_loop(self): # Основной цикл захвата кадров
        while self._running:
            ret, frame = self.cap.read()
            if ret:
                with self._lock:
                    self.frame = frame
                    
    def get_frame(self): # Получение текущего кадра
        with self._lock:
            return self.frame.copy() if self.frame is not None else None
        
    def stop(self): # Остановка потока захвата
        self._running = False
        self._thread.join(timeout=1.0)
        self.cap.release()
            