#define vPot A0  // Potentiometer connected to A0
#define APot A5
#define IOp 4 //turn on or off the function
#define ShiftBot 5
#define Breaker 6
#define HornBot 7

String TXT;

String serialRead;

bool runTime = true;


void setup() {
  Serial.begin(9600);  // Start serial communication
  for(int i=1;i>=13;i++){
    pinMode(i, INPUT);
  }
}

void loop() {
  /*if(Serial.available()){
    serialRead = Serial.readStringUntil('\n');  // Read the incoming string until a newline character
    serialRead.trim();  // Remove any extra whitespace or newline characters
  */
    //aValue = map(APot, 0, 1023, 0, 90);

  
  /*
  if(V != analogRead(vPot)){
    V = analogRead(vPot);
    TXT = ",V: " +     String(analogRead(vPot)) +',\n';
    Serial.println(TXT);
  }
  if(Sh != digitalRead(ShiftBot)){
    Sh = digitalRead(ShiftBot);
    TXT = ",Shift: " +     String(digitalRead(ShiftBot)) +',\n';
    Serial.println(TXT);
  }
  if(S != digitalRead(Breaker)){
    S = digitalRead(Breaker);
    TXT = ",S: " +     String(digitalRead(Breaker)) +',\n';
    Serial.println(TXT);
  }
  if(H != digitalRead(HornBot)){
    H = digitalRead(HornBot);
    TXT = ",H: " +     String(digitalRead(HornBot)) +',\n';
    Serial.println(TXT);
  }
  if(W != analogRead(APot)){
    W = analogRead(APot);
    TXT = ",W: " +     String(analogRead(APot)) +',\n';
    Serial.println(TXT);
  }
  if(IO != digitalRead(IOp)){
    IO = digitalRead(IOp);
    TXT = ",IO: " +     String(digitalRead(IOp)) +',\n';
    Serial.println(TXT);
  }*/
  /*
  V = analogRead(vPot);
  Sh = digitalRead(ShiftBot);
  S = digitalRead(Breaker);
  H = digitalRead(HornBot);
  W = analogRead(APot);
  IO =digitalRead(IO);
  */
  /*
  TXT = ",\nV:" +     String(analogRead(vPot)) +',\n' +
        ",\nVAngle:" +String(map(analogRead(vPot), 0, 1023, 0 ,360)) + ',\n' +
        ",\nShift:" + String(digitalRead(ShiftBot)) +',\n' + 
        ",\nS:" +     String(digitalRead(Breaker)) + ',\n' +
        ",\nH:" +     String(digitalRead(HornBot)) + ',\n' +
        ",\nW:" +     String(analogRead(APot)) + ',\n' +
        ",\nIO:" +    String(digitalRead(IOp)) + ',\n';

  */
  //Serial.println(TXT);
  //*/
  
  Serial.println(serialRead);
  Serial.print("V:");
  Serial.println(analogRead(vPot)); // volante
  Serial.print("W:");
  Serial.println(analogRead(APot)); // accelerator
  
  Serial.print("Shift:");
  Serial.println(digitalRead(ShiftBot));
  
  Serial.print("S:");
  Serial.println(digitalRead(Breaker));
  
  Serial.print("H:");
  Serial.println(digitalRead(HornBot));

  Serial.print("IOp:0");
  //Serial.println(digitalRead(IOp));

}
