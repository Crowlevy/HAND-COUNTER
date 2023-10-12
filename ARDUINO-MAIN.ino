const int ledPins[] = {8,9,10,11,12};//AQUI É ONDE ESTÃO OS PINOS E PODE SER ALTERADO
int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

void setup() {
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    int ledNum;

    if (command >= '1' && command <= '5') {//SE FOR MENOS OU MAIS QUE 5 MUDAR ELE
      ledNum = command - '1';
      digitalWrite(ledPins[ledNum], !digitalRead(ledPins[ledNum]));
    } else if (command == 'A' || command == 'a') {
      for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], HIGH);
      }
    } else if (command == 'D' || command == 'd') {
      for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], LOW);
      }
    }
  }
}
