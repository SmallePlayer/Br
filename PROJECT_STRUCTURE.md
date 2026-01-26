# Структура проекта

```
br/
├── pathfinding/              # Модуль с реализацией A* и эвристик
│   ├── __init__.py         # Инициализация модуля
│   ├── a_star.py           # Реализация A* алгоритма
│   └── heuristics.py       # Эвристики (Манхэттен, Евклид)
└── robot/                   # Логика движения робота и карта
    ├── __init__.py
    ├── controller.py       # Интерфейс A* для робота
    ├── bren.py             # Специфичный алгоритм движения (Brent)
    └── map_info.py         # Описание карты и примеры использования
│
├── tests/                   # Модуль с тестами
│   ├── __init__.py         # Инициализация модуля
│   ├── test_line.py        # Тест обработки видео и линий
│   └── test_matrix.py      # Тест работы с матрицами
│
├── A.py                     # Главный скрипт (A* алгоритм)
├── Dockerfile              # Docker конфигурация
├── README.md               # Основная документация
├── README_DOCKER.md        # Документация Docker
└── PROJECT_STRUCTURE.md    # Этот файл

```

## Зависимости между файлами

### A.py (главный скрипт)
- **Зависит от:**
  - `algorithms.evklid` - для расчета евклидова расстояния
  - `algorithms.manhed` - для расчета расстояния Манхэттена
  - `numpy` - для работы с матрицами

### tests/test_matrix.py
- **Зависит от:**
  - `algorithms.evklid` - для расчета расстояния между точками
  - `numpy` - для создания матриц

### tests/test_line.py
- **Зависит от:**
  - `cv2` (OpenCV) - для обработки видео
  - `numpy` - для работы с массивами пикселей

### algorithms/evklid.py
- **Независимый модуль**
- Использует: `math`

### algorithms/manhed.py
- **Независимый модуль**
- Использует: `math`

## Как запустить

### Главный скрипт (A* алгоритм)
```bash
python A.py
```

### Тесты
```bash
python tests/test_matrix.py    # Тест матриц
python tests/test_line.py      # Тест видео (требует камеру)
```

### Docker
```bash
docker build -t astar .
docker run astar
```
