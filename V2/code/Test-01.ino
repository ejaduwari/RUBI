//defines pins
#define stepPin D4
#define dirPin D3
#define enable D8

#define stepPin2 D2
#define dirPin2 D1
#define enable2 D7

#define stepPin3 D5
#define dirPin3 D6
#define enable3 D0

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enable, OUTPUT);

  pinMode(stepPin2,OUTPUT); 
  pinMode(dirPin2,OUTPUT);
  pinMode(enable2, OUTPUT);

  pinMode(stepPin3,OUTPUT); 
  pinMode(dirPin3,OUTPUT);
  pinMode(enable3, OUTPUT);
  
  digitalWrite(enable, HIGH); // disengages the driver FETs (stepper is off)
  digitalWrite(enable2, HIGH); // disengages the driver FETs (stepper is off)
  digitalWrite(enable3, HIGH); // disengages the driver FETs (stepper is off)
  delay(2000);
}

void loop() {

  //step1(50, 800);
  //delay(200);

  for(int i = 0; i < 3; i++){
    step1(-50, 800);
    delay(100);
    
    step1(50, 800);
    delay(100);
  } 
  delay(2000);

  for(int i = 0; i < 3; i++){
    step2(-50, 800);
    delay(100);
    
    step2(50, 800);
    delay(100);
  }
  delay(2000);

  for(int i = 0; i < 3; i++){
    step3(-50, 800);
    delay(100);
    
    step3(50, 800);
    delay(100);
  }
  delay(5000);
  
}

void step1(int a, int speed){
  if(a < 0){
    for(int x = 0; x < abs(a); x++) {
      digitalWrite(dirPin,LOW);
      digitalWrite(enable, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else if(a > 0){
    for(int x = 0; x < a; x++) {
      digitalWrite(dirPin,HIGH);
      digitalWrite(enable, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else{
    digitalWrite(enable, HIGH); // disengages the driver FETs (stepper is off)
    digitalWrite(stepPin, LOW); 
  }
  delayMicroseconds(700);
  digitalWrite(enable, HIGH);
}

void step2(int a, int speed){
  if(a < 0){
    for(int x = 0; x < abs(a); x++) {
      digitalWrite(dirPin2,LOW);
      digitalWrite(enable2, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin2,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin2,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable2, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else if(a > 0){
    for(int x = 0; x < a; x++) {
      digitalWrite(dirPin2,HIGH);
      digitalWrite(enable2, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin2,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin2,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable2, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else{
    digitalWrite(enable2, HIGH); // disengages the driver FETs (stepper is off)
    digitalWrite(stepPin2, LOW); 
  }
  delayMicroseconds(700);
  digitalWrite(enable2, HIGH);
}

void step3(int a, int speed){
  if(a < 0){
    for(int x = 0; x < abs(a); x++) {
      digitalWrite(dirPin3,LOW);
      digitalWrite(enable3, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin3,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin3,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable3, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else if(a > 0){
    for(int x = 0; x < a; x++) {
      digitalWrite(dirPin3,HIGH);
      digitalWrite(enable3, LOW); // engages the driver FETs (stepper is on)
      digitalWrite(stepPin3,HIGH); 
      delayMicroseconds(speed);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin3,LOW); 
      delayMicroseconds(speed); 
      //digitalWrite(enable3, HIGH); // disengages the driver FETs (stepper is off)
    }
  }
  else{
    digitalWrite(enable3, HIGH); // disengages the driver FETs (stepper is off)
    digitalWrite(stepPin3, LOW); 
  }
  delayMicroseconds(700);
  digitalWrite(enable3, HIGH);
}
