import cv2
import numpy as np

# Инициализация захвата видео с камеры (по умолчанию — первая камера)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Ошибка: не удалось открыть камеру.")
    exit()

while True:
    # Чтение кадра с камеры
    ret, frame = cap.read()
    if not ret:
        print("Ошибка: не удалось получить кадр.")
        break

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Детектор границ Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Создание маски: белые линии на чёрном фоне
    # Расширяем линии, чтобы они были толще и заметнее
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # Создаём копию исходного кадра
    result = frame.copy()

    # Наносим белые линии на исходный кадр
    # Где edges_dilated != 0 — ставим белый цвет (255, 255, 255)
    result[edges_dilated != 0] = [255, 255, 255]

    # Отображение исходного кадра и результата
    cv2.imshow('Исходный кадр', frame)
    cv2.imshow('Линии (белёные)', result)

    # Выход по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
