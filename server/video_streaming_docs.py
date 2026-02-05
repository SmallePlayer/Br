"""
================================================================================
                    ПОЛНАЯ ДОКУМЕНТАЦИЯ ПО OPENCV И СЕТЕВОЙ ПЕРЕДАЧЕ ВИДЕО
================================================================================

Автор: [Ваше имя]
Дата: 2026
Версия: 1.0

Содержание:
    1. ЗАХВАТ ВИДЕО С КАМЕРЫ (OpenCV VideoCapture)
    2. ОПЕРАЦИИ С КАДРАМИ (обработка изображений)
    3. СЖАТИЕ ИЗОБРАЖЕНИЙ (JPEG, PNG, WebP)
    4. СПОСОБЫ ОТПРАВКИ ПО СЕТИ:
        4.1. UDP - простая отправка (маленькие кадры)
        4.2. UDP - отправка с разбиением на куски (большие кадры, 4K)
        4.3. TCP - надежная отправка (гарантия доставки)
        4.4. TCP - потоковая отправка (для больших объемов)
    5. СРАВНЕНИЕ МЕТОДОВ (таблица производительности)
    6. РЕКОМЕНДАЦИИ ПО ВЫБОРУ МЕТОДА

================================================================================
"""

# ============================================================================
#                           ЧАСТЬ 1: ЗАХВАТ ВИДЕО С КАМЕРЫ
# ============================================================================
"""
OpenCV VideoCapture - основной класс для захвата видео.
Поддерживает: веб-камеры, IP-камеры, видеофайлы, изображения.
"""

import cv2
import numpy as np

# ----------------------------------------------------------------------------
# 1.1. ОТКРЫТИЕ ИСТОЧНИКА ВИДЕО
# ----------------------------------------------------------------------------

def open_camera_examples():
    """
    Примеры открытия разных источников видео.
    """
    
    # --- Веб-камера по индексу ---
    # 0 = первая камера (обычно встроенная)
    # 1 = вторая камера (обычно USB)
    # 2, 3... = дополнительные камеры
    cap = cv2.VideoCapture(0)
    
    # --- Веб-камера с указанием API ---
    # CAP_DSHOW - DirectShow (Windows, быстрее)
    # CAP_MSMF - Media Foundation (Windows)
    # CAP_V4L2 - Video4Linux (Linux)
    # CAP_AVFOUNDATION - AVFoundation (macOS)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Рекомендуется для Windows
    
    # --- Видеофайл ---
    cap = cv2.VideoCapture("video.mp4")
    cap = cv2.VideoCapture("C:/Videos/my_video.avi")
    
    # --- IP камера (RTSP поток) ---
    cap = cv2.VideoCapture("rtsp://192.168.1.100:554/stream")
    cap = cv2.VideoCapture("rtsp://admin:password@192.168.1.100:554/h264")
    
    # --- HTTP поток (MJPEG) ---
    cap = cv2.VideoCapture("http://192.168.1.100:8080/video")
    
    # --- Последовательность изображений ---
    cap = cv2.VideoCapture("frames/frame_%04d.jpg")  # frame_0001.jpg, frame_0002.jpg...
    
    return cap


# ----------------------------------------------------------------------------
# 1.2. НАСТРОЙКА ПАРАМЕТРОВ КАМЕРЫ
# ----------------------------------------------------------------------------

def configure_camera(cap):
    """
    Настройка параметров захвата видео.
    
    Параметры:
        cap: cv2.VideoCapture - объект захвата видео
        
    Возвращает:
        dict - словарь с текущими настройками
    """
    
    # ========== РАЗРЕШЕНИЕ ==========
    # Популярные разрешения:
    #   640x480   (VGA)      - ~0.3 MP, быстро, мало данных
    #   1280x720  (HD/720p)  - ~0.9 MP, баланс качества/скорости
    #   1920x1080 (FHD/1080p)- ~2.1 MP, хорошее качество
    #   2560x1440 (QHD/2K)   - ~3.7 MP, высокое качество
    #   3840x2160 (UHD/4K)   - ~8.3 MP, максимальное качество
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Ширина в пикселях
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Высота в пикселях
    
    # ========== ЧАСТОТА КАДРОВ (FPS) ==========
    # 15 FPS - минимум для видео
    # 24 FPS - кино
    # 30 FPS - стандарт
    # 60 FPS - плавное видео
    # 120+ FPS - замедленная съемка
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # ========== ФОРМАТ ПИКСЕЛЕЙ ==========
    # MJPG - сжатый формат, меньше нагрузка на USB
    # YUYV - несжатый, лучше качество
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    
    # ========== ПАРАМЕТРЫ ИЗОБРАЖЕНИЯ ==========
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)     # Яркость (0-255)
    cap.set(cv2.CAP_PROP_CONTRAST, 128)       # Контраст (0-255)
    cap.set(cv2.CAP_PROP_SATURATION, 128)     # Насыщенность (0-255)
    cap.set(cv2.CAP_PROP_HUE, 0)              # Оттенок
    cap.set(cv2.CAP_PROP_GAIN, 0)             # Усиление
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)        # Экспозиция (отрицательные = авто)
    
    # ========== БУФЕРИЗАЦИЯ ==========
    # Уменьшение буфера = меньше задержка, но возможны пропуски кадров
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)       # Размер буфера (1-10)
    
    # ========== АВТОФОКУС ==========
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)        # 1 = вкл, 0 = выкл
    cap.set(cv2.CAP_PROP_FOCUS, 0)            # Ручной фокус (если автофокус выкл)
    
    # ========== ПОЛУЧЕНИЕ ТЕКУЩИХ ЗНАЧЕНИЙ ==========
    settings = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'brightness': cap.get(cv2.CAP_PROP_BRIGHTNESS),
        'contrast': cap.get(cv2.CAP_PROP_CONTRAST),
        'exposure': cap.get(cv2.CAP_PROP_EXPOSURE),
        'fourcc': int(cap.get(cv2.CAP_PROP_FOURCC)),
    }
    
    return settings


# ----------------------------------------------------------------------------
# 1.3. ЗАХВАТ КАДРОВ
# ----------------------------------------------------------------------------

def capture_frame(cap):
    """
    Захват одного кадра с камеры.
    
    Параметры:
        cap: cv2.VideoCapture - объект захвата
        
    Возвращает:
        tuple: (success: bool, frame: np.ndarray или None)
        
    Структура frame:
        - Тип: numpy.ndarray
        - Форма: (height, width, channels) например (720, 1280, 3)
        - Dtype: uint8 (значения 0-255)
        - Цветовое пространство: BGR (не RGB!)
    """
    
    # Метод 1: Простой захват
    ret, frame = cap.read()
    # ret = True если успешно, False если ошибка
    # frame = numpy массив с изображением или None
    
    if not ret:
        print("Ошибка захвата кадра")
        return False, None
    
    return True, frame


def capture_frame_methods(cap):
    """
    Разные методы захвата кадров.
    """
    
    # Метод 1: read() - захват + декодирование (стандартный)
    ret, frame = cap.read()
    
    # Метод 2: grab() + retrieve() - раздельный захват
    # Полезно для синхронизации нескольких камер
    grabbed = cap.grab()      # Только захват (быстро)
    ret, frame = cap.retrieve()  # Декодирование (медленнее)
    
    # Метод 3: Пропуск кадров (для уменьшения задержки)
    cap.grab()  # Пропускаем старый кадр
    cap.grab()  # Пропускаем еще один
    ret, frame = cap.read()  # Читаем свежий кадр
    
    return frame


# ============================================================================
#                           ЧАСТЬ 2: ОПЕРАЦИИ С КАДРАМИ
# ============================================================================
"""
Основные операции обработки изображений в OpenCV.
"""

# ----------------------------------------------------------------------------
# 2.1. ИЗМЕНЕНИЕ РАЗМЕРА
# ----------------------------------------------------------------------------

def resize_frame(frame, target_width=None, target_height=None, scale=None):
    """
    Изменение размера кадра.
    
    Параметры:
        frame: np.ndarray - исходное изображение
        target_width: int - целевая ширина (опционально)
        target_height: int - целевая высота (опционально)
        scale: float - масштаб (0.5 = уменьшить вдвое)
        
    Методы интерполяции (cv2.INTER_*):
        INTER_NEAREST  - ближайший сосед (быстро, низкое качество)
        INTER_LINEAR   - билинейная (баланс, по умолчанию)
        INTER_AREA     - лучше для уменьшения
        INTER_CUBIC    - бикубическая (медленнее, лучше качество)
        INTER_LANCZOS4 - Ланцош (самое высокое качество, медленно)
    """
    
    if scale is not None:
        # Масштабирование
        resized = cv2.resize(frame, None, fx=scale, fy=scale, 
                            interpolation=cv2.INTER_LINEAR)
    elif target_width and target_height:
        # Точный размер
        resized = cv2.resize(frame, (target_width, target_height),
                            interpolation=cv2.INTER_LINEAR)
    elif target_width:
        # Пропорциональное по ширине
        ratio = target_width / frame.shape[1]
        target_height = int(frame.shape[0] * ratio)
        resized = cv2.resize(frame, (target_width, target_height))
    else:
        resized = frame
    
    return resized


# ----------------------------------------------------------------------------
# 2.2. КОНВЕРТАЦИЯ ЦВЕТОВЫХ ПРОСТРАНСТВ
# ----------------------------------------------------------------------------

def convert_color_space(frame, conversion):
    """
    Конвертация между цветовыми пространствами.
    
    Параметры:
        frame: np.ndarray - изображение
        conversion: int - код конвертации cv2.COLOR_*
        
    Популярные конвертации:
        COLOR_BGR2RGB   - BGR в RGB (для matplotlib, PIL)
        COLOR_BGR2GRAY  - в градации серого
        COLOR_BGR2HSV   - в HSV (для определения цвета)
        COLOR_BGR2LAB   - в LAB (для коррекции цвета)
        COLOR_BGR2YUV   - в YUV (для видео)
    """
    
    # BGR -> RGB (OpenCV использует BGR, большинство библиотек - RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # BGR -> Grayscale (черно-белое)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # BGR -> HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    return cv2.cvtColor(frame, conversion)


# ----------------------------------------------------------------------------
# 2.3. ОБРЕЗКА (CROP)
# ----------------------------------------------------------------------------

def crop_frame(frame, x, y, width, height):
    """
    Обрезка области изображения.
    
    Параметры:
        frame: np.ndarray - изображение
        x, y: int - координаты верхнего левого угла
        width, height: int - размеры области
        
    Возвращает:
        np.ndarray - обрезанное изображение
    """
    
    # NumPy slicing: [y:y+h, x:x+w]
    # ВАЖНО: сначала Y (строки), потом X (столбцы)!
    cropped = frame[y:y+height, x:x+width]
    
    return cropped


# ----------------------------------------------------------------------------
# 2.4. ПОВОРОТ И ОТРАЖЕНИЕ
# ----------------------------------------------------------------------------

def rotate_and_flip(frame):
    """
    Поворот и отражение изображения.
    """
    
    # Поворот на 90° по часовой
    rotated_90 = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    # Поворот на 90° против часовой
    rotated_90_ccw = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    # Поворот на 180°
    rotated_180 = cv2.rotate(frame, cv2.ROTATE_180)
    
    # Отражение по горизонтали (зеркало)
    flipped_h = cv2.flip(frame, 1)  # 1 = горизонтально
    
    # Отражение по вертикали
    flipped_v = cv2.flip(frame, 0)  # 0 = вертикально
    
    # Отражение по обеим осям
    flipped_both = cv2.flip(frame, -1)  # -1 = обе оси
    
    return rotated_90


# ----------------------------------------------------------------------------
# 2.5. РИСОВАНИЕ НА ИЗОБРАЖЕНИИ
# ----------------------------------------------------------------------------

def draw_on_frame(frame):
    """
    Рисование фигур и текста на изображении.
    Все функции модифицируют frame на месте!
    """
    
    # Копируем чтобы не изменять оригинал
    img = frame.copy()
    
    # --- Линия ---
    # line(img, pt1, pt2, color, thickness, lineType)
    cv2.line(img, (0, 0), (100, 100), (0, 255, 0), 2)
    
    # --- Прямоугольник ---
    # rectangle(img, pt1, pt2, color, thickness)
    # thickness=-1 для заливки
    cv2.rectangle(img, (50, 50), (200, 150), (255, 0, 0), 2)
    
    # --- Круг ---
    # circle(img, center, radius, color, thickness)
    cv2.circle(img, (300, 200), 50, (0, 0, 255), -1)  # -1 = заливка
    
    # --- Текст ---
    # putText(img, text, org, fontFace, fontScale, color, thickness)
    cv2.putText(img, "Hello!", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Шрифты:
    # FONT_HERSHEY_SIMPLEX - обычный
    # FONT_HERSHEY_PLAIN - тонкий
    # FONT_HERSHEY_DUPLEX - двойной
    # FONT_HERSHEY_COMPLEX - сложный
    # FONT_HERSHEY_SCRIPT_SIMPLEX - рукописный
    
    return img


# ============================================================================
#                           ЧАСТЬ 3: СЖАТИЕ ИЗОБРАЖЕНИЙ
# ============================================================================
"""
Методы сжатия для передачи по сети.
Важно: размер влияет на скорость передачи!
"""

import struct

# ----------------------------------------------------------------------------
# 3.1. JPEG СЖАТИЕ (с потерями, маленький размер)
# ----------------------------------------------------------------------------

def compress_jpeg(frame, quality=80):
    """
    Сжатие в JPEG формат.
    
    Параметры:
        frame: np.ndarray - изображение (BGR)
        quality: int - качество 1-100
            1-30:   низкое качество, очень маленький размер
            31-60:  среднее качество, маленький размер
            61-80:  хорошее качество, средний размер (рекомендуется)
            81-95:  высокое качество, большой размер
            96-100: максимум, почти без потерь
            
    Возвращает:
        bytes - сжатые данные
        
    Примерные размеры для 1280x720:
        quality=50:  ~15-25 KB
        quality=70:  ~25-40 KB
        quality=80:  ~35-50 KB
        quality=90:  ~60-90 KB
    """
    
    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    success, compressed = cv2.imencode('.jpg', frame, encode_params)
    
    if not success:
        raise ValueError("Ошибка сжатия JPEG")
    
    return compressed.tobytes()


# ----------------------------------------------------------------------------
# 3.2. PNG СЖАТИЕ (без потерь, большой размер)
# ----------------------------------------------------------------------------

def compress_png(frame, compression=3):
    """
    Сжатие в PNG формат (без потерь).
    
    Параметры:
        frame: np.ndarray - изображение
        compression: int - уровень сжатия 0-9
            0: без сжатия (быстро, большой файл)
            1-3: быстрое сжатие (рекомендуется)
            4-6: среднее сжатие
            7-9: максимальное сжатие (медленно)
            
    Возвращает:
        bytes - сжатые данные
        
    Примерные размеры для 1280x720:
        compression=0: ~2.7 MB
        compression=3: ~1.5-2 MB
        compression=9: ~1.2-1.5 MB
    """
    
    encode_params = [cv2.IMWRITE_PNG_COMPRESSION, compression]
    success, compressed = cv2.imencode('.png', frame, encode_params)
    
    if not success:
        raise ValueError("Ошибка сжатия PNG")
    
    return compressed.tobytes()


# ----------------------------------------------------------------------------
# 3.3. WEBP СЖАТИЕ (современный формат, хороший баланс)
# ----------------------------------------------------------------------------

def compress_webp(frame, quality=80):
    """
    Сжатие в WebP формат.
    
    Параметры:
        frame: np.ndarray - изображение
        quality: int - качество 1-100
            1-100: с потерями (как JPEG, но лучше)
            
    Возвращает:
        bytes - сжатые данные
        
    Преимущества WebP:
        - Меньше размер чем JPEG при том же качестве
        - Поддержка прозрачности
        - Современные браузеры поддерживают
    """
    
    encode_params = [cv2.IMWRITE_WEBP_QUALITY, quality]
    success, compressed = cv2.imencode('.webp', frame, encode_params)
    
    if not success:
        raise ValueError("Ошибка сжатия WebP")
    
    return compressed.tobytes()


# ----------------------------------------------------------------------------
# 3.4. ДЕКОДИРОВАНИЕ СЖАТЫХ ДАННЫХ
# ----------------------------------------------------------------------------

def decompress_image(data):
    """
    Декодирование сжатого изображения.
    
    Параметры:
        data: bytes - сжатые данные (JPEG, PNG, WebP)
        
    Возвращает:
        np.ndarray - изображение BGR
        
    Флаги чтения (cv2.IMREAD_*):
        IMREAD_COLOR      - цветное BGR (по умолчанию)
        IMREAD_GRAYSCALE  - черно-белое
        IMREAD_UNCHANGED  - как есть (с альфа-каналом)
    """
    
    # Создаем numpy массив из байтов
    nparr = np.frombuffer(data, np.uint8)
    
    # Декодируем изображение
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        raise ValueError("Ошибка декодирования изображения")
    
    return frame


# ============================================================================
#               ЧАСТЬ 4: СПОСОБЫ ОТПРАВКИ ПО СЕТИ
# ============================================================================

import socket
import time

# ============================================================================
#           4.1. UDP ПРОСТАЯ ОТПРАВКА (для маленьких кадров < 60KB)
# ============================================================================
"""
Самый БЫСТРЫЙ способ, но:
- Ограничение ~65KB на пакет
- Нет гарантии доставки
- Пакеты могут прийти не по порядку

Подходит для:
- Низкое разрешение (640x480, 320x240)
- Высокое сжатие (quality < 50)
- Локальная сеть
"""

# --- ОТПРАВИТЕЛЬ (простой UDP) ---

def udp_simple_sender(host, port, jpeg_quality=50):
    """
    Простая UDP отправка кадров.
    Для кадров размером < 60KB.
    
    Параметры:
        host: str - IP адрес получателя
        port: int - порт получателя
        jpeg_quality: int - качество JPEG (1-100)
    """
    
    # Создаем UDP сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Открываем камеру с низким разрешением
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_id = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Сжимаем кадр
        data = compress_jpeg(frame, jpeg_quality)
        
        # Проверяем размер
        if len(data) > 60000:
            print(f"Предупреждение: кадр слишком большой ({len(data)} байт)")
            continue
        
        # Добавляем заголовок с ID кадра (4 байта)
        header = struct.pack('!I', frame_id)
        packet = header + data
        
        # Отправляем одним пакетом
        sock.sendto(packet, (host, port))
        
        print(f"Кадр {frame_id}: {len(data)} байт")
        frame_id += 1
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    sock.close()


# --- ПОЛУЧАТЕЛЬ (простой UDP) ---

def udp_simple_receiver(host, port):
    """
    Простой UDP приемник кадров.
    
    Параметры:
        host: str - IP для прослушивания ('0.0.0.0' = все интерфейсы)
        port: int - порт для прослушивания
    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.settimeout(5.0)
    
    print(f"Слушаю на {host}:{port}")
    
    while True:
        try:
            data, addr = sock.recvfrom(65535)
            
            # Извлекаем заголовок
            frame_id = struct.unpack('!I', data[:4])[0]
            jpeg_data = data[4:]
            
            # Декодируем
            frame = decompress_image(jpeg_data)
            
            cv2.imshow('UDP Simple', frame)
            print(f"Кадр {frame_id} от {addr}")
            
            if cv2.waitKey(1) == ord('q'):
                break
                
        except socket.timeout:
            print("Таймаут")
            continue
    
    sock.close()
    cv2.destroyAllWindows()


# ============================================================================
#           4.2. UDP С РАЗБИЕНИЕМ НА КУСКИ (для больших кадров, 4K)
# ============================================================================
"""
Для передачи кадров больше 60KB.
Кадр разбивается на куски, каждый кусок отправляется отдельным пакетом.

Подходит для:
- Высокое разрешение (1080p, 4K)
- Высокое качество JPEG (quality > 70)
- Требуется скорость важнее надежности
"""

# --- ОТПРАВИТЕЛЬ (UDP с кусками) ---

def udp_chunked_sender(host, port, width=1920, height=1080, jpeg_quality=80):
    """
    UDP отправка с разбиением на куски.
    
    Параметры:
        host: str - IP адрес получателя
        port: int - порт получателя
        width: int - ширина кадра
        height: int - высота кадра
        jpeg_quality: int - качество JPEG
        
    Формат заголовка пакета (12 байт):
        frame_id:   4 байта (I) - ID кадра
        chunk_idx:  2 байта (H) - индекс куска
        num_chunks: 2 байта (H) - всего кусков
        data_size:  4 байта (I) - полный размер данных
    """
    
    CHUNK_SIZE = 60000  # Размер одного куска
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    frame_id = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Сжимаем
        data = compress_jpeg(frame, jpeg_quality)
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
            
            sock.sendto(packet, (host, port))
        
        print(f"Кадр {frame_id}: {data_size/1024:.1f} KB, {num_chunks} кусков")
        frame_id += 1
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    sock.close()


# --- ПОЛУЧАТЕЛЬ (UDP с кусками) ---

def udp_chunked_receiver(host, port):
    """
    UDP приемник с поддержкой кусков.
    
    Параметры:
        host: str - IP для прослушивания
        port: int - порт для прослушивания
    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.settimeout(5.0)
    
    current_frame_id = -1
    chunks = {}
    expected_chunks = 0
    
    print(f"Слушаю на {host}:{port}")
    
    while True:
        try:
            data, addr = sock.recvfrom(65535)
            
            if len(data) < 12:
                continue
            
            # Распаковываем заголовок
            frame_id, chunk_idx, num_chunks, data_size = struct.unpack('!IHHI', data[:12])
            chunk_data = data[12:]
            
            # Новый кадр - сбрасываем старый
            if frame_id > current_frame_id:
                current_frame_id = frame_id
                chunks = {}
                expected_chunks = num_chunks
            
            # Старый кадр - игнорируем
            if frame_id < current_frame_id:
                continue
            
            # Сохраняем кусок
            chunks[chunk_idx] = chunk_data
            
            # Собрали все куски?
            if len(chunks) == expected_chunks:
                # Собираем кадр
                full_data = b''.join(chunks[i] for i in range(expected_chunks))
                
                # Декодируем
                frame = decompress_image(full_data)
                
                if frame is not None:
                    cv2.imshow('UDP Chunked', frame)
                    print(f"Кадр {frame_id}: {len(full_data)/1024:.1f} KB")
                
                chunks = {}
            
            if cv2.waitKey(1) == ord('q'):
                break
                
        except socket.timeout:
            continue
    
    sock.close()
    cv2.destroyAllWindows()


# ============================================================================
#           4.3. TCP НАДЕЖНАЯ ОТПРАВКА (гарантия доставки)
# ============================================================================
"""
TCP гарантирует:
- Доставку всех данных
- Правильный порядок
- Целостность данных

Недостатки:
- Медленнее UDP
- Задержки при потере пакетов
- Нужно устанавливать соединение

Подходит для:
- Запись видео (нельзя терять кадры)
- Нестабильная сеть (WiFi, интернет)
- Важнее качество чем скорость
"""

# --- СЕРВЕР TCP (отправитель) ---

def tcp_server_sender(host, port, width=1280, height=720, jpeg_quality=80):
    """
    TCP сервер - отправляет кадры подключившемуся клиенту.
    
    Параметры:
        host: str - IP для прослушивания
        port: int - порт сервера
        width, height: int - разрешение
        jpeg_quality: int - качество JPEG
        
    Протокол:
        1. Отправляем размер данных (4 байта, big-endian)
        2. Отправляем данные
    """
    
    # Создаем TCP сокет
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(1)  # Максимум 1 клиент в очереди
    
    print(f"TCP сервер на {host}:{port}, ожидание подключения...")
    
    # Ждем подключения клиента
    client_sock, client_addr = server_sock.accept()
    print(f"Клиент подключен: {client_addr}")
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    frame_id = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Сжимаем
            data = compress_jpeg(frame, jpeg_quality)
            
            # Отправляем размер (4 байта)
            size_bytes = struct.pack('!I', len(data))
            client_sock.sendall(size_bytes)
            
            # Отправляем данные
            client_sock.sendall(data)
            
            print(f"Кадр {frame_id}: {len(data)/1024:.1f} KB отправлен")
            frame_id += 1
            
            cv2.imshow('TCP Sending', frame)
            if cv2.waitKey(1) == ord('q'):
                break
                
    except (ConnectionResetError, BrokenPipeError):
        print("Клиент отключился")
    
    finally:
        cap.release()
        client_sock.close()
        server_sock.close()
        cv2.destroyAllWindows()


# --- КЛИЕНТ TCP (получатель) ---

def tcp_client_receiver(host, port):
    """
    TCP клиент - получает кадры от сервера.
    
    Параметры:
        host: str - IP сервера
        port: int - порт сервера
    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    print(f"Подключено к {host}:{port}")
    
    frame_id = 0
    
    def recv_exactly(sock, size):
        """Получить ровно size байт."""
        data = b''
        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Соединение закрыто")
            data += chunk
        return data
    
    try:
        while True:
            # Получаем размер (4 байта)
            size_bytes = recv_exactly(sock, 4)
            data_size = struct.unpack('!I', size_bytes)[0]
            
            # Получаем данные
            data = recv_exactly(sock, data_size)
            
            # Декодируем
            frame = decompress_image(data)
            
            if frame is not None:
                cv2.imshow('TCP Received', frame)
                print(f"Кадр {frame_id}: {len(data)/1024:.1f} KB получен")
            
            frame_id += 1
            
            if cv2.waitKey(1) == ord('q'):
                break
                
    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")
    
    finally:
        sock.close()
        cv2.destroyAllWindows()


# ============================================================================
#           4.4. TCP ПОТОКОВАЯ ОТПРАВКА (для 4K и больших объемов)
# ============================================================================
"""
Оптимизированная TCP передача для больших кадров.
Использует буферизацию и потоковую передачу.

Особенности:
- Увеличенные буферы сокета
- Отключен алгоритм Nagle (TCP_NODELAY)
- Эффективнее для больших данных
"""

# --- ПОТОКОВЫЙ TCP СЕРВЕР (для 4K) ---

def tcp_streaming_server(host, port, width=3840, height=2160, jpeg_quality=85):
    """
    TCP сервер для потоковой передачи 4K видео.
    
    Параметры:
        host: str - IP для прослушивания
        port: int - порт
        width, height: int - разрешение (3840x2160 = 4K)
        jpeg_quality: int - качество JPEG
        
    Оптимизации:
        - Большой буфер отправки (1 MB)
        - TCP_NODELAY - отключает алгоритм Nagle
        - SO_REUSEADDR - быстрый перезапуск сервера
    """
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сокета для производительности
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)  # 1 MB буфер
    server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Без задержки
    
    server_sock.bind((host, port))
    server_sock.listen(1)
    
    print(f"4K TCP сервер на {host}:{port}...")
    
    client_sock, client_addr = server_sock.accept()
    client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
    
    print(f"Клиент: {client_addr}")
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Минимальный буфер камеры
    
    # Проверяем реальное разрешение
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Реальное разрешение: {actual_w}x{actual_h}")
    
    frame_id = 0
    fps_start = time.time()
    fps_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Сжимаем
            t_start = time.time()
            data = compress_jpeg(frame, jpeg_quality)
            t_encode = time.time() - t_start
            
            # Заголовок: размер (4 байта) + ID кадра (4 байта)
            header = struct.pack('!II', len(data), frame_id)
            
            # Отправляем
            t_start = time.time()
            client_sock.sendall(header + data)
            t_send = time.time() - t_start
            
            # FPS
            fps_count += 1
            elapsed = time.time() - fps_start
            if elapsed >= 1.0:
                fps = fps_count / elapsed
                print(f"Кадр {frame_id}: {len(data)/1024:.1f} KB | "
                      f"Сжатие: {t_encode*1000:.1f}ms | "
                      f"Отправка: {t_send*1000:.1f}ms | "
                      f"FPS: {fps:.1f}")
                fps_start = time.time()
                fps_count = 0
            
            frame_id += 1
            
            if cv2.waitKey(1) == ord('q'):
                break
                
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        cap.release()
        client_sock.close()
        server_sock.close()


# --- ПОТОКОВЫЙ TCP КЛИЕНТ (для 4K) ---

def tcp_streaming_client(host, port):
    """
    TCP клиент для приема 4K видео.
    
    Параметры:
        host: str - IP сервера
        port: int - порт сервера
    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024)  # 1 MB буфер
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    sock.connect((host, port))
    print(f"Подключено к {host}:{port}")
    
    fps_start = time.time()
    fps_count = 0
    
    def recv_exactly(sock, size):
        """Получить ровно size байт."""
        data = b''
        while len(data) < size:
            chunk = sock.recv(min(size - len(data), 1024*1024))  # Читаем по 1 MB
            if not chunk:
                raise ConnectionError("Соединение закрыто")
            data += chunk
        return data
    
    try:
        while True:
            # Получаем заголовок (8 байт)
            header = recv_exactly(sock, 8)
            data_size, frame_id = struct.unpack('!II', header)
            
            # Получаем данные
            t_start = time.time()
            data = recv_exactly(sock, data_size)
            t_recv = time.time() - t_start
            
            # Декодируем
            t_start = time.time()
            frame = decompress_image(data)
            t_decode = time.time() - t_start
            
            if frame is not None:
                # Для 4K уменьшаем для отображения
                display = cv2.resize(frame, (1280, 720))
                cv2.imshow('4K Stream', display)
                
                # FPS
                fps_count += 1
                elapsed = time.time() - fps_start
                if elapsed >= 1.0:
                    fps = fps_count / elapsed
                    print(f"Кадр {frame_id}: {data_size/1024:.1f} KB | "
                          f"Прием: {t_recv*1000:.1f}ms | "
                          f"Декод: {t_decode*1000:.1f}ms | "
                          f"FPS: {fps:.1f} | "
                          f"Размер: {frame.shape}")
                    fps_start = time.time()
                    fps_count = 0
            
            if cv2.waitKey(1) == ord('q'):
                break
                
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        sock.close()
        cv2.destroyAllWindows()


# ============================================================================
#               ЧАСТЬ 5: СРАВНЕНИЕ МЕТОДОВ
# ============================================================================
"""
ТАБЛИЦА СРАВНЕНИЯ МЕТОДОВ ПЕРЕДАЧИ:

┌─────────────────────┬──────────────┬─────────────┬────────────┬─────────────┐
│ Метод               │ Скорость     │ Надежность  │ Задержка   │ Применение  │
├─────────────────────┼──────────────┼─────────────┼────────────┼─────────────┤
│ UDP простой         │ ★★★★★     │ ★★☆☆☆     │ ★★★★★   │ 480p, LAN   │
│ UDP с кусками       │ ★★★★☆     │ ★★★☆☆     │ ★★★★☆   │ 1080p-4K    │
│ TCP простой         │ ★★★☆☆     │ ★★★★★     │ ★★★☆☆   │ 720p-1080p  │
│ TCP потоковый       │ ★★★★☆     │ ★★★★★     │ ★★★☆☆   │ 4K, запись  │
└─────────────────────┴──────────────┴─────────────┴────────────┴─────────────┘

РЕКОМЕНДАЦИИ ПО РАЗРЕШЕНИЮ:

┌─────────────────┬──────────────┬─────────────┬─────────────────────────────┐
│ Разрешение      │ Размер JPEG  │ Метод       │ Настройки                   │
├─────────────────┼──────────────┼─────────────┼─────────────────────────────┤
│ 320x240         │ 5-15 KB      │ UDP простой │ quality=50-70               │
│ 640x480         │ 15-40 KB     │ UDP простой │ quality=60-80               │
│ 1280x720 (HD)   │ 30-80 KB     │ UDP/TCP     │ quality=70-85               │
│ 1920x1080 (FHD) │ 80-200 KB    │ UDP куски   │ quality=75-90, chunks       │
│ 2560x1440 (2K)  │ 150-350 KB   │ TCP поток   │ quality=80-90               │
│ 3840x2160 (4K)  │ 300-800 KB   │ TCP поток   │ quality=80-95, большой буфер│
└─────────────────┴──────────────┴─────────────┴─────────────────────────────┘
"""


# ============================================================================
#               ЧАСТЬ 6: ПОЛЕЗНЫЕ УТИЛИТЫ
# ============================================================================

def get_optimal_settings(resolution, network_type='lan'):
    """
    Получить оптимальные настройки для заданного разрешения и типа сети.
    
    Параметры:
        resolution: str - '480p', '720p', '1080p', '4k'
        network_type: str - 'lan' (локальная), 'wifi', 'internet'
        
    Возвращает:
        dict - рекомендуемые настройки
    """
    
    settings = {
        '480p': {
            'width': 640, 'height': 480,
            'lan': {'method': 'udp_simple', 'quality': 70},
            'wifi': {'method': 'udp_simple', 'quality': 60},
            'internet': {'method': 'tcp', 'quality': 50},
        },
        '720p': {
            'width': 1280, 'height': 720,
            'lan': {'method': 'udp_simple', 'quality': 80},
            'wifi': {'method': 'udp_chunked', 'quality': 70},
            'internet': {'method': 'tcp', 'quality': 60},
        },
        '1080p': {
            'width': 1920, 'height': 1080,
            'lan': {'method': 'udp_chunked', 'quality': 85},
            'wifi': {'method': 'tcp', 'quality': 75},
            'internet': {'method': 'tcp_streaming', 'quality': 65},
        },
        '4k': {
            'width': 3840, 'height': 2160,
            'lan': {'method': 'tcp_streaming', 'quality': 90},
            'wifi': {'method': 'tcp_streaming', 'quality': 80},
            'internet': {'method': 'tcp_streaming', 'quality': 70},
        },
    }
    
    res_settings = settings.get(resolution, settings['720p'])
    net_settings = res_settings.get(network_type, res_settings['lan'])
    
    return {
        'width': res_settings['width'],
        'height': res_settings['height'],
        'method': net_settings['method'],
        'jpeg_quality': net_settings['quality'],
    }


def benchmark_compression(frame, qualities=[30, 50, 70, 80, 90, 95]):
    """
    Тест производительности сжатия.
    
    Параметры:
        frame: np.ndarray - тестовый кадр
        qualities: list - уровни качества для теста
        
    Возвращает:
        list - результаты теста
    """
    
    results = []
    
    for q in qualities:
        # JPEG
        t_start = time.time()
        jpg_data = compress_jpeg(frame, q)
        t_jpg = time.time() - t_start
        
        results.append({
            'quality': q,
            'size_kb': len(jpg_data) / 1024,
            'time_ms': t_jpg * 1000,
        })
    
    # Вывод таблицы
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТА СЖАТИЯ")
    print("=" * 50)
    print(f"Исходный размер: {frame.shape[0]}x{frame.shape[1]}")
    print("-" * 50)
    print(f"{'Качество':^10} | {'Размер (KB)':^12} | {'Время (ms)':^12}")
    print("-" * 50)
    
    for r in results:
        print(f"{r['quality']:^10} | {r['size_kb']:^12.1f} | {r['time_ms']:^12.2f}")
    
    print("=" * 50)
    
    return results


# ============================================================================
#               ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == '__main__':
    print("""
    ================================================================================
                        ДОКУМЕНТАЦИЯ ПО OPENCV И СЕТЕВОЙ ПЕРЕДАЧЕ
    ================================================================================
    
    Примеры запуска:
    
    1. UDP простой (маленькие кадры):
       Терминал 1: python -c "from video_docs import *; udp_simple_receiver('localhost', 3333)"
       Терминал 2: python -c "from video_docs import *; udp_simple_sender('localhost', 3333)"
    
    2. UDP с кусками (большие кадры):
       Терминал 1: python -c "from video_docs import *; udp_chunked_receiver('localhost', 3333)"
       Терминал 2: python -c "from video_docs import *; udp_chunked_sender('localhost', 3333)"
    
    3. TCP (надежная передача):
       Терминал 1: python -c "from video_docs import *; tcp_server_sender('localhost', 3333)"
       Терминал 2: python -c "from video_docs import *; tcp_client_receiver('localhost', 3333)"
    
    4. TCP потоковый (4K):
       Терминал 1: python -c "from video_docs import *; tcp_streaming_server('localhost', 3333)"
       Терминал 2: python -c "from video_docs import *; tcp_streaming_client('localhost', 3333)"
    
    5. Тест сжатия:
       cap = cv2.VideoCapture(0)
       ret, frame = cap.read()
       benchmark_compression(frame)
       cap.release()
    
    ================================================================================
    """)
