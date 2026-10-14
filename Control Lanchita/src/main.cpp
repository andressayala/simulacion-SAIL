#include <Arduino.h>
#include <ESP32Servo.h>
#include "BluetoothSerial.h"

Servo esc;
Servo servo;
BluetoothSerial SerialBT;

int throttle = 0;

void setup() {
  Serial.begin(9600);
  SerialBT.begin("Lanchita");
  
  
  esc.attach(13, 1000, 2000);
  servo.attach(12);

  Serial.println("--- ESC Serial Control ---");
  Serial.println("Enter a value between 1000 and 2000");
  Serial.println("1000 = Off | 2000 = Full Throttle");
  
  
  Serial.println("Arming ESC...");
  esc.writeMicroseconds(1000);
  servo.write(75);
  delay(2000); 
  Serial.println("ESC Armed and Ready.");
}

void loop() {
  if (SerialBT.available() > 0) {
    // Read the integer from the Serial Monitor
    int input = SerialBT.parseInt();

    // Validate the input range
    if (input >= 1000 && input <= 2000) {
      throttle = input;
      esc.writeMicroseconds(throttle);
      
      Serial.print("Throttle set to: ");
      Serial.println(throttle);
      
      SerialBT.print("Throttle set to: ");
      SerialBT.println(throttle);
    } 
    else if (-75 <= input && input <= 50){
      servo.write(75 + input);
      
      Serial.print("Angle set to: ");
      Serial.println(input);
      
      SerialBT.print("Angle set to: ");
      SerialBT.println(input);
    }
    else if (input != 0) {
      Serial.println("Invalid input.");
      SerialBT.println("Invalid input.");
    }

    while (SerialBT.available() > 0) {
      SerialBT.read(); 
    }

  }
}