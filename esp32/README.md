# ESP32 Robot Client

Код для ESP32 микроконтроллера для управления роботом.

## Структура

- `src/` - исходный код
- `include/` - заголовочные файлы
- `platformio.ini` - конфигурация PlatformIO

## Настройка

1. Отредактируйте WiFi credentials в `src/main.cpp`
2. Укажите IP адрес сервера

## Сборка и загрузка

```bash
cd esp32
pio run -e esp32dev -t upload
pio device monitor
```

## Требования

- PlatformIO
- ESP32 development board
