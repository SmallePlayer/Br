#include <Arduino.h>
#include <WiFi.h>

static const char* WIFI_SSID = "Keenetic-8281";  
static const char* WIFI_PASS = "UYy5BHPc"; 

static const char* SERVER_IP = "192.168.1.143";
static const uint16_t SERVER_PORT = 3333;

// Максимальное количество попыток подключения к WiFi (40 * 500ms = 20 секунд)
static const int WIFI_MAX_ATTEMPTS = 40;
// Интервал между попытками переподключения к серверу в миллисекундах (5 секунд)
static const int RECONNECT_INTERVAL = 5000;

// Создаем объект TCP клиента для работы с TCP соединением
WiFiClient client;
// Переменная для сохранения времени последней попытки подключения к серверу
unsigned long lastReconnectTime = 0;

void connectToServer() {
  if (client.connected()) {
    return;
  }

  Serial.print("Connecting to server ");
  Serial.print(SERVER_IP);
  Serial.print(":");
  Serial.println(SERVER_PORT);

  // Пытаемся установить соединение с сервером по указанному IP и порту
  if (client.connect(SERVER_IP, SERVER_PORT)) {
    Serial.println("Connected to server!");
    // Отключаем алгоритм Nagle (немедленная отправка данных без буферизации)
    client.setNoDelay(true);
  } else {
    Serial.println("Failed to connect to server");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("=== ESP32-C3 TCP Echo Client ===");

  // Переводим модуль WiFi в режим "станция" (подключается к роутеру как обычное устройство)
  WiFi.mode(WIFI_STA);
  // Начинаем подключение к WiFi сети с указанным SSID и паролем
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting to WiFi ");
  Serial.print(WIFI_SSID);
  Serial.println("...");

  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < WIFI_MAX_ATTEMPTS) {
    delay(500);
    Serial.print('.');
    attempt++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi Connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("Failed to connect to WiFi");
  }
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected, waiting for reconnection...");
    delay(1000);
    return;
  }

  // Проверяем, подключены ли мы к TCP серверу (логический оператор ! означает "не")
  if (!client.connected()) {
    if (millis() - lastReconnectTime >= RECONNECT_INTERVAL) {
      lastReconnectTime = millis();
      connectToServer();
    }
  } else {

    static unsigned long lastSendTime = 0;
    unsigned long now = millis();
    
    // Проверяем, прошло ли 3 секунды с момента последней отправки сообщения
    // if (now - lastSendTime >= 3000) {
    //   // Сохраняем текущее время как время последней отправки
    //   lastSendTime = now;
      
    //   String message = "Hello from ESP32 - ";
    //   message += now / 1000;
    //   message += " seconds";
      
    //   Serial.print("Sending: ");
  //   Serial.println(message);
      
    //   // Отправляем сообщение на подключенный сервер
    //   client.print(message);
    //   // Отправляем символ новой строки (конец сообщения)
    //   client.print("\n");
    // }

    // Проверяем, есть ли данные для чтения с сервера
    if (client.available()) {
      // Читаем строку данных с сервера до символа новой строки
      String response = client.readStringUntil('\n');
      // Удаляем пробелы и символы новой строки с начала и конца строки
      response.trim();
      
      // Проверяем, что строка не пуста (длина больше 0)
      if (response.length() > 0) {
        Serial.print("Echo response: ");
        Serial.println(response);
      }
    }
  }

  delay(10);
}
