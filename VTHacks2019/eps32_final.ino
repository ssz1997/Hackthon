#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>

// Set these to run example.
#define FIREBASE_HOST "ricecooker-5ea62.firebaseio.com"
#define FIREBASE_AUTH "aT20OxgUKQd24EnNbYntEooTBSzTQUbPVppIq4yU"
#define WIFI_SSID "AndroidAPB670"
#define WIFI_PASSWORD "mlpy6496"

int channel = 0;
int freq = 2000;
int resolution = 8;
void setup() {
  Serial.begin(9600);
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(12, channel);
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

int n = 0;

void loop() {

  // get value 
  Serial.print("number: ");
  int num = Firebase.getFloat("number");
  if (num) {
    ledcWriteTone(channel, 2000);
    for (int dutyCycle = 100; dutyCycle < 100+10*num; dutyCycle=dutyCycle+10){
 
      Serial.println(dutyCycle);
 
      ledcWrite(channel, dutyCycle);
      delay(500);
      ledcWrite(channel, 0);
      delay(500);
  }
    // update value
    Firebase.setFloat("number", 0);
    // handle error
    if (Firebase.failed()) {
        Serial.print("setting /number failed:");
        Serial.println(Firebase.error());  
        return;
    }
    delay(1000);
  }
  Serial.println(Firebase.getFloat("number"));
  delay(1000);

 
  

}
