```const byte ledPins[5] = {18, 19, 21, 22, 23};
const byte buttonPins[5] = {13, 12, 14, 27, 26};

bool ledState[5] = {0,0,0,0,0};
bool lastButtonState[5] = {HIGH,HIGH,HIGH,HIGH,HIGH};

String deviceName[5]={
    "Light 1",
    "Light 2",
    "Light 3",
    "Fan 1",
    "Fan 2"
};

void setup() {

  Serial.begin(115200);

  for(int i=0;i<5;i++)
  {
    pinMode(ledPins[i],OUTPUT);
    digitalWrite(ledPins[i],LOW);

    pinMode(buttonPins[i],INPUT_PULLUP);
  }

  Serial.println("Smart Office Monitoring Started");
}

void loop() {

  for(int i=0;i<5;i++)
  {
    bool current=digitalRead(buttonPins[i]);

    if(lastButtonState[i]==HIGH && current==LOW)
    {
      ledState[i]=!ledState[i];

      digitalWrite(ledPins[i],ledState[i]);

      Serial.print(deviceName[i]);
      Serial.print(" : ");

      if(ledState[i])
        Serial.println("ON");
      else
        Serial.println("OFF");

      delay(200);
    }

    lastButtonState[i]=current;
  }
}```