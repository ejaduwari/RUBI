#include <AccelStepper.h>

AccelStepper s1(1, D4, D3);
AccelStepper s2(1, D2, D1);
AccelStepper s3(1, D5, D6);

void setup() {
  s1.setMaxSpeed(1000);
  s1.setAcceleration(2000);
  s1.setCurrentPosition(0);

  s2.setMaxSpeed(1000);
  s2.setAcceleration(2000);
  s2.setCurrentPosition(0);

  s3.setMaxSpeed(1000);
  s3.setAcceleration(2000);
  s3.setCurrentPosition(0);


  delay(2000);
}

void loop() {
  s1.moveTo(-52);
  s1.runToPosition();
  delay(2000);

  s2.moveTo(53);
  s2.runToPosition();
  delay(2000);

   s1.moveTo(0);
  s1.runToPosition();
  delay(2000);

  s2.moveTo(0);
  s2.runToPosition();
  delay(2000);

  
}

/**

**/