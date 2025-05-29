#define vPot A0  // Potentiometer connected to A0
#define APot A1
#define IO 4 //turn on or off the function
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

  TXT = "\nV:" + String(analogRead(vPot)) +
        ",\nW:" + String(analogRead(APot)) + 
        ",\nShift:" + String(digitalRead(ShiftBot)) + 
        ",\nS:" + String(digitalRead(Breaker)) + 
        ",\nH:" + String(digitalRead(HornBot)) + 
        ",\nVAngle:" + String(map(analogRead(vPot), 0, 1023, 0 ,360)) +
        ",\nIO:" + String(digitalRead(IO));

  
  Serial.println(TXT);
    /*
    Serial.println(serialRead);

    Serial.print("V");
    Serial.println(analogRead(vPot)); // volante

    Serial.print("W");
    Serial.println(analogRead(APot)); // accelerator
    
    Serial.print("Shift");
    Serial.println(digitalRead(ShiftBot));
    
    Serial.print("S");
    Serial.println(digitalRead(Breaker));
    
    Serial.print("H");
    Serial.println(digitalRead(HornBot));
    */
}
