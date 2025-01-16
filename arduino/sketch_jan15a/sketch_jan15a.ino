#include "Servo.h"

Servo servo; // Объект для работы с серво
int angle = 90; // Начальное положение серво
bool isStopped = false; // Флаг для остановки

void setup() {
  servo.attach(11); // Пин для подключения серво
  servo.write(angle); // Устанавливаем начальное положение
  Serial.begin(9600); // Для получения команд из Python
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Считываем команду до конца строки

    if (command == "STOP") { // Специальная команда для остановки
      isStopped = true; // Устанавливаем флаг
      return; // Выходим из loop
    }

    angle = command.toInt(); // Конвертируем команду в угол
    if (angle >= 0 && angle <= 180) { // Проверка на допустимые значения угла
      isStopped = false; // Сбрасываем флаг остановки
      servo.write(angle); // Поворачиваем серво на указанный угол
      delay(20); // Ждем, пока серво выполнит команду
    }
  }
}
