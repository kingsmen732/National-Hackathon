#include <Arduino.h>

#include <Adafruit_Fingerprint.h>

HardwareSerial serialPort(2);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&serialPort);

int getFingerprintIDez();
void printHex(int num, int precision);
uint8_t downloadFingerprintTemplate(uint16_t id);

void setup()
{
  while (!Serial)
    ;
  Serial.begin(9600);
  Serial.println("Fingerprint template extractor");

  finger.begin(57600);

  if (finger.verifyPassword())
  {
    Serial.println("Found fingerprint sensor!");
  }
  else
  {
    Serial.println("Did not find fingerprint sensor :(");
    while (1)
      ;
  }

  for (int finger = 1; finger < 10; finger++)
  {
    downloadFingerprintTemplate(finger);
  }
}

uint8_t downloadFingerprintTemplate(uint16_t id)
{
  Serial.println("------------------------------------");
  Serial.print("Attempting to load #");
  Serial.println(id);
  uint8_t p = finger.loadModel(id);
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.print("Template ");
    Serial.print(id);
    Serial.println(" loaded");
    break;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  default:
    Serial.print("Unknown error ");
    Serial.println(p);
    return p;
  }


  Serial.print("Attempting to get #");
  Serial.println(id);
  p = finger.getModel();
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.print("Template ");
    Serial.print(id);
    Serial.println(" transferring:");
    break;
  default:
    Serial.print("Unknown error ");
    Serial.println(p);
    return p;
  }

  uint8_t bytesReceived[534]; 
  memset(bytesReceived, 0xff, 534);

  uint32_t starttime = millis();
  int i = 0;
  while (i < 534 && (millis() - starttime) < 20000)
  {
    if (serialPort.available())
    {
      bytesReceived[i++] = serialPort.read();
    }
  }
  Serial.print(i);
  Serial.println(" bytes read.");
  Serial.println("Decoding packet...");

  uint8_t fingerTemplate[512]; // the real template
  memset(fingerTemplate, 0xff, 512);

  // filtering only the data packets
  int uindx = 9, index = 0;
  memcpy(fingerTemplate + index, bytesReceived + uindx, 256); 
  uindx += 256;                                               
  uindx += 2;                                                 
  uindx += 9;                                                 
  index += 256;                                               
  memcpy(fingerTemplate + index, bytesReceived + uindx, 256); 

  for (int i = 0; i < 512; ++i)
  {

    printHex(fingerTemplate[i], 2);

  }
  Serial.println("\ndone.");

  return p;


}

void printHex(int num, int precision)
{
  char tmp[16];
  char format[128];

  sprintf(format, "%%.%dX", precision);

  sprintf(tmp, format, num);
  Serial.print(tmp);
}

void loop()
{
}
