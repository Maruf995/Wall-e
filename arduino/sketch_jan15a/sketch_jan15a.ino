#include "Servo.h"

Servo servo; // Объект для работы с серво
int angle; // Переменная для угла поворота серво

void setup() {
  servo.attach(11); // Пин для подключения серво
  Serial.begin(9600); // Для получения команд из Python
}

void loop() {
  if (Serial.available() > 0) {
    angle = Serial.parseInt(); // Получаем угол из Python
    if (angle >= 0 && angle <= 180) { // Проверка на допустимые значения угла
      servo.write(angle); // Поворачиваем серво на указанный угол
      delay(20); // Ждем, пока серво выполнит команду
    }
  }
}
