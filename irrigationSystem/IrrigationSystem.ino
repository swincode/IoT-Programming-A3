//DHT library
#include <DHT.h>
#define type DHT22
int sensor =3;
  
DHT HT(sensor,type);

//automation
bool LEDisAutomated=true;
bool pumpisAutomated=true;

//temp & humidity sensor variable
float hum;
float temp;


//water level sensor var
int moistSensorPin= A1;
int moistValue= 0;

//lEDs pins
int lEDsPin =2;


// photo resistor sensor var
int photoRpin= A4;
int lightValue= 0;


//DC motor(water pump) variables
int dcMotorIn1=5;
int dcMotorIn2=6;
int power =9;
 
void setup() {
 HT.begin();
 pinMode(moistSensorPin,INPUT);
 pinMode(photoRpin,INPUT);
 pinMode(lEDsPin, OUTPUT);
 pinMode(dcMotorIn1, INPUT);
 pinMode(dcMotorIn2, INPUT);
 pinMode(power, OUTPUT);
analogWrite(power,255);
 Serial.begin(9600);
}


void loop() {

   //Check if there is serial input data available 
   if (Serial.available()>0)
   {
    //getting input from web
      //Read serial input
      int value = Serial.read();
      if (value == '1')
      {       
        digitalWrite(lEDsPin,HIGH); 
        LEDisAutomated=false;      
      }
      else if (value == '2')
      {
        LEDisAutomated =true;
        digitalWrite(lEDsPin,LOW);  
      }
       else if (value == '3')
      {
        pumpisAutomated=false;
        digitalWrite(dcMotorIn1,HIGH);
        digitalWrite(dcMotorIn2,LOW);
      }
      
       else if (value == '4')
      {
      digitalWrite(dcMotorIn1,LOW);
      digitalWrite(dcMotorIn2,LOW);
       pumpisAutomated =true;
      }
   }
   
 //photo resistor 
lightValue = analogRead(photoRpin);
 Serial.println(lightValue);
 delay(500);
 
 if(LEDisAutomated==true){
if(lightValue < 350)
{
  digitalWrite(lEDsPin,HIGH);
}

else if(lightValue >= 350)
{
  digitalWrite(lEDsPin,LOW);
}
else{
    digitalWrite(lEDsPin,LOW);
  }
 }

// water level 
moistValue = analogRead(moistSensorPin);
 Serial.println(moistValue);
delay(500);
// water pump
  if(pumpisAutomated==true){
if(moistValue < 100)
{
   digitalWrite(dcMotorIn1,HIGH);
   digitalWrite(dcMotorIn2,LOW);
}

else if(moistValue>= 200)
{
   digitalWrite(dcMotorIn1,LOW);
   digitalWrite(dcMotorIn2,LOW);
}
else{
  digitalWrite(dcMotorIn1,LOW);
  digitalWrite(dcMotorIn2,LOW);
  }
 }


hum = HT.readHumidity();
temp = HT.readTemperature();
Serial.println(hum);
delay(500);
Serial.println(temp);
delay(500);

}
