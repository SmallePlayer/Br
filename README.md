# BattleBot Robot Control System

Система управления роботом с алгоритмами поиска пути и ESP32 клиентом.

## 📁 Структура проекта

```
br/
├── esp32/                   # ESP32 код (C++)
│   ├── src/                # Исходники
│   │   └── main.cpp       # Главный файл ESP32
│   ├── include/           # Заголовочные файлы
│   ├── platformio.ini     # Конфигурация PlatformIO
│   └── README.md          # Документация ESP32
│
├── server/                  # TCP сервер (Python)
│   ├── tcp_server.py      # Основной сервер
│   └── README.md          # Документация сервера
│
├── algorithms/              # Алгоритмы поиска пути
│   ├── evklid.py          # Евклидово расстояние
│   ├── manhed.py          # Манхэттенское расстояние
│   └── README.md          # Документация алгоритмов
│
├── br/                      # Модули pathfinding и robot
│   ├── pathfinding/       # A* и эвристики
│   ├── robot/             # Управление роботом
│   └── utils/             # Утилиты
│
├── tests/                   # Тесты
├── Dockerfile              # Docker конфигурация
└── README.md              # Этот файл
```

## 🚀 Быстрый старт

### ESP32 (C++)

```bash
cd esp32
# Отредактируйте WiFi настройки в src/main.cpp
pio run -e esp32dev -t upload
pio device monitor
```

### TCP Сервер (Python)

```bash
python server/tcp_server.py
```

### Алгоритмы

```python
from algorithms.evklid import evklid_distance
from algorithms.manhed import manhed_distance
```


## 📝 Компоненты

### ESP32 Client (`esp32/`)
- Код на C++ для ESP32
- Подключение к WiFi
- TCP клиент для связи с сервером
- См. [esp32/README.md](esp32/README.md)

### TCP Server (`server/`)
- Python сервер для коммуникации с ESP32
- Прием и отправка команд
- См. [server/README.md](server/README.md)

### Algorithms (`algorithms/`)
- Алгоритмы вычисления расстояний
- Используются для поиска пути
- См. [algorithms/README.md](algorithms/README.md)

### BattleBot Module (`br/`)
- Pathfinding: A* алгоритм
- Robot: управление движением
- Utils: вспомогательные функции

## 💻 Разработка

### Установка зависимостей

```bash
# Python
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install numpy opencv-python

# ESP32 (PlatformIO)
pip install platformio
```

### Запуск тестов

```bash
python tests/test_matrix.py
python tests/test_line.py
```


## 🔧 Конфигурация

### ESP32 (`esp32/src/main.cpp`)
```cpp
static const char* WIFI_SSID = "YOUR_WIFI_SSID";
static const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
static const char* SERVER_IP = "192.168.1.143";
```

### TCP Server (`server/tcp_server.py`)
```python
HOST = '0.0.0.0'
PORT = 3333
```

## 📚 Документация

- [ESP32 Client](esp32/README.md)
- [TCP Server](server/README.md)
- [Algorithms](algorithms/README.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## 🤝 Разработка

Проект разделен на независимые компоненты:
- **ESP32**: Работа с микроконтроллером
- **Server**: Сетевая коммуникация
- **Algorithms**: Математические алгоритмы
- **br/**: Основная логика робота

Каждый компонент имеет свой README с деталями.

## 🐳 Docker

```bash
docker build -t battlebot .
docker run battlebot
```

См. [README_DOCKER.md](README_DOCKER.md) для деталей.

