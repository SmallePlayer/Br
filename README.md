# A* Pathfinding Algorithm

Реализация алгоритма поиска пути A* (A-star) на Python.

## Описание

Проект реализует алгоритм A* для поиска оптимального пути на сетке с препятствиями. Алгоритм использует эвристику расстояния Манхэттена для эффективного поиска.

## Структура проекта

```
br/
├── algorithms/              # Модуль с алгоритмами
│   ├── evklid.py           # Евклидово расстояние
│   └── manhed.py           # Расстояние Манхэттена
├── tests/                   # Модуль с тестами
│   ├── test_line.py        # Тест обработки видео
│   └── test_matrix.py      # Тест матриц
├── A.py                     # Главный скрипт (A* алгоритм)
├── Dockerfile              # Docker конфигурация
└── README.md               # Этот файл
```

Подробнее см. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Зависимости между файлами

| Файл | Зависит от |
|------|-----------|
| A.py | algorithms.evklid, algorithms.manhed, numpy |
| tests/test_matrix.py | algorithms.evklid, numpy |
| tests/test_line.py | cv2, numpy |
| algorithms/evklid.py | math |
| algorithms/manhed.py | math |

## Использование

### Запустить A* алгоритм
```bash
python A.py
```

Скрипт создает сетку 10x10, отмечает препятствие и находит путь от начальной позиции (0,0) к целевой позиции (7,9).

### Запустить тесты
```bash
python tests/test_matrix.py    # Тест работы с матрицами
python tests/test_line.py      # Тест обработки видео
```

### Параметры (в файле A.py)
- `x_self, y_self` - начальная позиция
- `x_target, y_target` - целевая позиция
- `obstacle` - позиция препятствия

## Визуализация карты

- `0` - пустая клетка
- `1` - препятствие
- `2` - посещенные клетки
- `8` - найденный путь

## Требования

```
numpy
opencv-python (для test_line.py)
```

## Установка

```bash
pip install numpy opencv-python
```

## Docker

```bash
docker build -t astar .
docker run astar
```

Дополнительные сведения см. в [README_DOCKER.md](README_DOCKER.md)
