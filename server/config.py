import cv2 
import numpy as np
import struct
import threading
from collections import deque


def open_camera(index=0, os = 'win'):
    WEB_API = None
    if os == 'win':
        WEB_API = cv2.CAP_DSHOW
    elif os == 'linux':
        WEB_API = cv2.CAP_V4L2
    elif os == 'macos':
        WEB_API = cv2.CAP_AVFOUNDATION
    cap = cv2.VideoCapture(index)
    return cap


def configure_camera(cap, permission='720', buffer=1):
    if permission == '720':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   
    elif permission == '1080':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    elif permission == '2k':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)   
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
    elif permission == '4k':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)   
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer) 
    
    
def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

def capture_grab_frame(cap):
    grab_frame = cap.read()
    if not grab_frame:
        return None
    return grab_frame

def compress_jpeg(frame, quality=60):
    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    success, compressed = cv2.imencode('.jpg', frame, encode_params)
    if not success:
        raise ValueError("Ошибка сжатия JPEG")
    return compressed.tobytes()

def compress_web(frame, quality=70):
    encode_params = [cv2.IMWRITE_WEBP_QUALITY, quality]
    success, compressed = cv2.imencode('.webp', frame, encode_params)
    if not success:
        raise ValueError("Ошибка сжатия JPEG")
    return compressed.tobytes()

def decompress_frame(data):
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame


# Threaded camera capture
_camera_frame = None
_camera_lock = threading.Lock()
running = True
_camera_thread = None

def capture_threaded_loop_frame(cap):
    global _camera_frame, running
    while running:
        ret, frame = cap.read()
        if ret:
            with _camera_lock:
                _camera_frame = frame
                
def start_camera_threaded(cap):
    global _camera_thread, running
    running = True
    _camera_thread = threading.Thread(target=capture_threaded_loop_frame, args=(cap,))
    _camera_thread.start()
    
def get_frame_threaded():
    global _camera_frame
    with _camera_lock:
                return _camera_frame.copy() if _camera_frame is not None else None

def stop_camera_thread():
    global _camera_running
    _camera_running = False
    if _camera_thread is not None:
        _camera_thread.join(timeout=1.0)
