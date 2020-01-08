#include <LiquidCrystal.h> // includes the LiquidCrystal Library 
  LiquidCrystal lcd(2, 3, 4, 5, 6, 7); // Creates an LC object. Parameters: (rs, enable, d4, d5, d6, d7) 
  
void setup() {
  // put your setup code here, to run once:
  Serial3.begin(9600);
  Serial.begin(9600);
  Serial2.begin(9600);
  analogWrite(51, 255);
  analogWrite(52, 0);
  analogWrite(53, 0);
  lcd.begin(16, 2);
 
  
  while (Serial3.available()==0)
  {
    
  }
  analogWrite(51, 0);
  analogWrite(52, 0);
  analogWrite(53, 255);

}
//A14 = temperature
//A15 = gas                     
//A13 = humidity   
                             
void loop() {   
  Serial.println("test");                 
  // put your main code here, to run repeatedly: 
  //Serial1.print(Serial2.readString());                             
  String s = "";  
  s+=(analogRead(A15)/120.0);
  s+=",";                                                 
  delay(50);                              
float e = analogRead(A13);

while (e>50)
{
 e-=5.0;
}
s+=e;
s+=",";
  delay(50);
  int d = analogRead(A14)-27;
  //d =;
  delay(50);
  s += d;
  Serial3.println(s);
  Serial.println(s);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(d);
  lcd.print( "C");
  lcd.setCursor(0, 1);
  lcd.print("Humidity: ");
  lcd.print(e);
  lcd.print("%");
  delay(5000);
}