
boolean isExecuted = false;
const short maxValue = 0;
const short minValue = 1000;
unsigned short lowerThreshold = 50;
unsigned short upperThreshold = 100;
unsigned long count_time_now = 0;
boolean autoAdaptLight = false;
unsigned long adaptTime = 0;
static bool state = LOW;
unsigned short counter = 0; // counter for impulse

unsigned long previousMillis = 0;  
const long interval = 1000;   

const int pResistor = A0;
void setup()
{
  Serial.begin(9600);
  Serial.print("Started");
}

void loop()
{
  unsigned short analogValue = analogRead(pResistor);
  if (millis() <= 60000 && autoAdaptLight == false)
  {
    autoAdapt(analogValue);

    if(millis()<=10000){
      Serial.print("7");
    }
  }
  else {
    isExecuted = false;
    if (state == HIGH) {
      if (analogValue < lowerThreshold + (upperThreshold - lowerThreshold) / 2) {
        state = LOW;
        Serial.print("1kwh\n");
      }
    } else {
      if (analogValue > upperThreshold - (upperThreshold - lowerThreshold) / 2) {
        state = HIGH;
      }
    }
  }
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Serial.print("777");
  
  }
  
  delay(3);
}
void autoAdapt(unsigned short analogValue) {
  if (!isExecuted)
  {
    upperThreshold = maxValue;
    lowerThreshold = minValue;
    isExecuted = true;
  }

  if (upperThreshold < analogValue)
  {
    upperThreshold = analogValue;
  }

  if (lowerThreshold > analogValue)
  {
    lowerThreshold = analogValue;
  }
}
