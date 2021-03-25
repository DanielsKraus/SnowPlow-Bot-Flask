//#include <SD.h>
#include  <Wire.h>
#include  <Adafruit_MotorShield.h>
#include  <Servo.h>
#include <Arduino_LSM6DS3.h>

/*
 * Created by: Daniel Kraus 
 * Date: 23Feb2021
 * Note: SD card shield not installed commented out lines.
*/
// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *motorL = AFMS.getMotor(1); // track motor left
Adafruit_DCMotor *motorR = AFMS.getMotor(2); // track motr right

Servo standard;  //standard high torque servo
Servo micro;     // micro high torque servo

//File plowData;   // data from plowbot to be saved

int pos = 20;    // nuetral position up/down plow
int pos2 = 86;   // nuetral position left/right plow
int offset = 13; // positional adjustment for plow
String movement;

void setup() {
  Serial.begin(9600);   
  
  init_motorshield();
  init_LSM6DS3();
  micro.attach(9);
  standard.attach(10);
  
  // put servos in nuetral
  standard.write(pos);
  micro.write(pos2);    
  delay(1000);   
}
void init_motorshield(){
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  Serial.print("Testing motors");
  motorL->setSpeed(200);  // Set speed 0-255
  motorL->run(RELEASE);
  
  Serial.print(".");
  
  motorR->setSpeed(200);  // Set speed 0-255
  motorR->run(RELEASE);
  
  Serial.print(".");
  Serial.println(".");
  Serial.println("Motor test complete");
  Serial.println("\n");
}
void init_LSM6DS3(){
   if (!IMU.begin()) 
   {
    Serial.println("Failed to initialize IMU!");
    while (1);
   }
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(IMU.gyroscopeSampleRate());
}
/*
void save_file(String action) // uncomment for saving data to file
{
  plowData = SD.open("plow_data.txt", FILE_APPEND);   
  if(plowData){
    Serial.println("Initializing SD");
  else{
    Serial.println("Failed to initialize SD");
  }
  plowData.println(action + "," + "accel: " + IMU.accelerationSampleRate() + "," + "gyro: " + IMU.gyroscopeSampleRate());
  plowData.close();    
}
*/
void Forward(){
  Serial.println("moving forward");
  motorL->run(FORWARD);
  motorR->run(FORWARD);
  delay(1000);
}
void Reverse(){
  Serial.println("moving backward");
  motorL->run(BACKWARD);
  motorR->run(BACKWARD);
  delay(1000);
}
void Left(){
  Serial.println("turning left");
  motorL->run(BACKWARD);
  motorR->run(FORWARD);
  delay(1000);
}
void Right(){
  Serial.println("turning right");
  motorL->run(FORWARD);
  motorR->run(BACKWARD);
  delay(1000);
}
void Stop(){
  Serial.println("Stopped moving");
  motorL->run(RELEASE);
  motorR->run(RELEASE);
  delay(100);
}
void lifter_p_up(){
  Serial.println("raising plow");
  standard.attach(10);
  standard.write(pos);              
  delay(1000);                       
}
void lifter_p_low(){
  Serial.println("lowering plow");
  standard.detach();          
  delay(1000);                       
}
void turn_p_L(){
  Serial.println("plow left"); 
  micro.write(pos2-offset);              
  delay(1000);                       
}
void turn_p_R(){
  Serial.println("plow right");
  micro.write(pos2+offset);              
  delay(1000);                       
}
void turn_p_C(){
  Serial.println("plow nuetral");
  micro.write(pos2);              
  delay(1000);                       
}
void loop() {
  if(Serial.available() > 0)
  {
    String input = Serial.readStringUntil("\n");
    Serial.println(input);
    
    input.trim();
    
    if(input.equals("forward")) // move forward
    {
      movement = "move: forward";
      Forward();
    } 
    else if(input.equals("backward")) // move in reverse
    {
      movement = "move: reverse";
      Reverse();
    }
    else if(input.equals("right"))  // turn right
    {
      movement = "move: right";
      Right();
    }
    else if(input.equals("left")) // turn left
    {
      movement = "move: left";
      Left(); 
    }
    else if(input.equals("plow up")) // raise plow
    {
      movement = "plow: up";
      lifter_p_up();   
    }
    else if(input.equals("plow down"))  // lower plow
    {
      movement = "plow: down";
      lifter_p_low();
    }
    else if(input.equals("plow left")) // turn plow left
    {
      movement = "plow: left";
      turn_p_L();
    }
    else if(input.equals("plow right"))// turn plow right
    {
      movement = "plow: right";
      turn_p_R();
    }
    else if(input.equals("plow center"))// turn plow to nuetral position  
    {
      movement = "plow: center";
      turn_p_C();
    }
    else
    {
      movement = "move: stop";
      Stop();
    }
    //save_file(movement);
   }
}
