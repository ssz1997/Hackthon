#include <Servo.h>
int id=99;
int soundSensor = 2;
int numOfPeople = 0;
#include <SoftwareSerial.h>

SoftwareSerial sw(2, 3); // RX, TX


Servo powerservo;
Servo waterservo1;
Servo waterservo2;
//Servo riceOpenServo;


int pos = 0;


void setup() {
  // put your setup code here, to run once:
  //riceOpenServo.attach(8);
  //riceCloseServo.attach(9);
  powerservo.attach(12);
  //waterservo1.attach(2);
  //waterservo2.attach(4);
  pinMode(soundSensor, INPUT);
  
  Serial.begin(115200);
  Serial.println("Interfacfing arduino with nodemcu");
  sw.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
// int sensorData=digitalRead(soundSensor);
// if (sensorData == 1){
//   //numOfPeople ++;
//   Serial.println("HIGH");
// }
// else{
//   Serial.println("LOW");
//   if (numOfPeople != 0){
     
     Serial.println("Sending data to nodemcu");
     int adc=analogRead(A0);
     Serial.print("{\"sensorid\":");
     Serial.print(id);//sensor id
     Serial.print(",");
     Serial.print("\"adcValue\":");
     Serial.print(adc);//offset
     Serial.print("}");
     Serial.println();
     
     sw.print("{\"sensorid\":");
     sw.print(id);//sensor id
     sw.print(",");
     sw.print("\"adcValue\":");
     sw.print(adc);//offset
     sw.print("}");
     sw.println();
     
    //  //pour water
      //waterservo1.write(150);
      //waterservo2.write(75);
      //delay(10000);
    
      //stop pouring water
      //waterservo1.write(60);
      //waterservo2.write(0);
      //delay(2000);
    
      //pour rice
      //riceOpenServo.write(80);
      //riceCloseServo.write(40);
      //delay(10000);
    
      //stop pouring rice
      //riceOpenServo.write(40);
      //riceCloseServo.write(90);
      //delay(2000);
    
      //start cooking
      //powerservo.write(110);

      delay(3000);
      powerservo.write(150);
    
  
      delay(500);
 
  exit(0);
}
