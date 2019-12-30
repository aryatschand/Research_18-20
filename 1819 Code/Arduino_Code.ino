//Written by Arya Tschand
//11/17/18 - 11/18/18, Updated 3/29/19 - 3/31/19

//Define libraries used
#include "MeOrion.h"
#include <SoftwareSerial.h>
#include <Wire.h>
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8

//Define variables and arrays
int frequency = 0;
int dirPin = mePort[PORT_2].s1;
int stpPin = mePort[PORT_2].s2;
int motorSpeed = 200;
int waterTimeConversion = 2000;
long plantTime;
String printString;
bool messageGiven = false;
bool narrowDone = false;
long ColorArray[12];
long HealthArray[12];
float colorData [12][100];
float waterData [12][100];
long TotalWater[12] = {};
long CalculatedArray[12] = {};
long waterForPlant[12] = {};
long updatingCalculatedArray[12] = {};
float averageArray[12] = {};
long updatedWaterArray[12] = {};
long topWater = 0;
long topNumber = 0;
float average = 0;
int narrowedWater = 0;
int narrowedHSV = 0;
int minColor = 0;
bool dataPassed = false;
String StringColor [12];
String StringHealth [12];
float yintercept;
double Area = 0;
boolean doDemo = false;
boolean demoDone = false;
MeUltrasonicSensor ultraSensor(PORT_6);

//Program runs through setup once in the beginning of the program
void setup() {
  
  //Define pins of outputs and inputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stpPin, OUTPUT);
  pinMode(sensorOut, INPUT);

  //Turn on color sensor
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
  //Begin program at 96600 baud
  Serial.begin(9600);
  
  //Collect information from database
    if (Serial.available() > 0) {
       String input = Serial.readString();
      //Sort input into arrays
       for (int x = 0; x<12; x++) {
          if (input.charAt(3) == ' ') {
              ColorArray[x] = input.substring(0,1).toInt();
              HealthArray[x] = input.substring(2, 3).toInt();
              input = input.substring(4);
          } else if (input.charAt(4) == ' ') {
              ColorArray[x] = input.substring(0,2).toInt();
              HealthArray[x] = input.substring(3, 4).toInt();
              input = input.substring(5);
          } else {
              ColorArray[x] = input.substring(0,3).toInt();
              HealthArray[x] = input.substring(4, 5).toInt();
              input = input.substring(6);
          } 
       }
   }

  //Use regression algorithm to find preliminary average change
  averageChange(ColorArray, 12);

  //Perform preliminary functions (defined later in program)
  minColor = minimumColor(12);
  minimumWater(ColorArray, HealthArray, 12);
  findTop(CalculatedArray, 12);
  findWater(topWater);
  
  //Populate data arrays with preliminary data
  for (int x = 0; x<12; x++) {
    for (int y = 0; y<12; y++) {
      colorData[x][y] = ColorArray[y];
      waterData[x][y] = 2*y + 4;
    }
    for (int y = 12; y<100; y++) {
      colorData[x][y] = 0;
      waterData[x][y] = 0;
    }
  }
}

//Used to make stepper motor turn a desired distance
void step(boolean dir,int steps)
{
  digitalWrite(dirPin,dir);
  delay(50);
  
  for(int i=0;i<steps;i++)
  {
    digitalWrite(stpPin, HIGH);
    delayMicroseconds(3200);
    digitalWrite(stpPin, LOW);
    delayMicroseconds(3200); 
  }
  
}

//Used to populate the CalculatedArray (Quantifies plants' performance by weighing color, health, and water amount)
void minimumWater( long color[], long health[], int Arraysize) 
{
  for (int a = 0; a < Arraysize; a++) 
  {
    CalculatedArray[a] = ((2*a + 6))*(health[a])*(color[a]);
  }
}

//Used to find the average color of all the healthy plants
int minimumColor(int Arraysize) 
{
  int combined = 0;
  int counter = 0;
  
  //Look for healthy plants
  for (int a = 0; a<Arraysize; a++) 
  {
    if (HealthArray[a] == 1) 
    {
      combined = combined + ColorArray[a];
      counter++;
    }
  }

  //Calculate value
  combined = combined/counter;
  return combined;
}

//Used to find the average color gained per mL of water added of original plants (AI implementation using dynamic linear regression)
void averageChange(long colorInput[], int n){
  //Define variables needed for dynamic linear regression function
  long waterInput[] = {6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28};
  long sumx = 0;
  long sumy = 0;
  long sumxy = 0;
  long sumxsquared = 0;
  float slope = 0;
  float yint = 0; 
   
  //Populate variables with current data set
  for (int i=0; i<n; i++){
    sumx+=waterInput[i];
    sumy+=colorInput[i];
    sumxy+=(waterInput[i]*colorInput[i]);
    sumxsquared+=(waterInput[i]*waterInput[i]);
  }

  //Use variables to calculate y-intercept and slope of function
  yint = (((sumy*sumxsquared)-(sumx*sumxy))/((n*sumxsquared)-(sumx*sumx)));
  slope = (((n*sumxy)-(sumx*sumy))/((n*sumxsquared)-(sumx*sumx)));
  
  average = slope;
  yintercept = yint;
  for (int x = 0; x<12; x++) {
    averageArray[x] = slope;
  }
}


//Used to find ideal volume water to give plants based on data in CalculatedArray
void findTop(long calculated[], int ArraySize)
{
  if (calculated[0] != 0) 
  {
    topWater = 6;
    topNumber = 0;
  } else 
  {
    topWater = 0;
    topNumber = 0;
  }
  
  //Look through all the plants to find lowest calculated value
  for (int c = 1; c<ArraySize; c++) 
  {
    if (calculated[c] != 0) 
    {
       if (calculated[c]<calculated[topNumber]) 
       {
            topWater = 2*c + 6;
            topNumber = c;
       }
    }
  }
}

//Used to define how much water to give each plants at first (will eventually narrow)
void findWater(int water)
{
  waterForPlant[0] = water;
  waterForPlant[1] = water-2;
  waterForPlant[2] = water-1;
  waterForPlant[3] = water;
  waterForPlant[4] = water+1;
  waterForPlant[5] = water+2;
  waterForPlant[6] = water-2;
  waterForPlant[7] = water-1;
  waterForPlant[8] = water;
  waterForPlant[9] = water+1;
  waterForPlant[10] = water+2;
  waterForPlant[11] = water;
}

//Sends message to VB.net program to find color of plant using webcam and color summarizer
int colorCheck()
{
  Serial.println("Color");
  while (dataPassed == false) {
    if (Serial.available() > 0) {
      dataPassed = true;
      return Serial.readString().toInt();
    }
  }
}

//Water Cycle with no input from color sensor (used with colorInput function)
void waterCycle() 
{
  //Repeat for 12 plants
  for (int i=0;i<12;i++) 
  {
    //Give water
    analogWrite(5, motorSpeed);
    plantTime = waterForPlant[i];
    TotalWater[i] += waterForPlant[i];
    plantTime *= 2000;
    plantTime = plantTime/10;
    delay(500);
    delay(plantTime);
    analogWrite(5, LOW);  
    
    //Turn to next plant 
    step(0,3200/12);
    delay(500);
  }
  
  //Turn back 360 degrees after 1 revolution
  step(1, 3130);
}

//Water Cycle that checks color and updates before watering each plant
void compareWaterCycle() 
{
  //Repeat for 12 plants
  for (int i=0;i<12;i++) 
  {
    //Wait and check color
    delay(10000);
    int changingColor = colorCheck();
    
    //Process result - update linear regression function and volume of water to give each plant 
    compare(changingColor, i);
    
    //Print message for VB.net and mySQL use
    printString+="Update ";
    printString+=i;
    printString+=" ";
    printString+=changingColor;
    printString+=" ";
    printString+=updatedWaterArray[i];
    printString+=" ";
    printString+=ultraSensor.distanceInch();
    Serial.println(printString);
    
    //Give water
    analogWrite(5, motorSpeed);
    plantTime = updatedWaterArray[i];
    TotalWater[i] += waterForPlant[i];
    plantTime *= 2000;
    plantTime = plantTime/10;
    delay(500);
    delay(plantTime);
    analogWrite(5, LOW);  

    //Turn to next plant 
    step(0,3200/12);
    delay(500);
  }
  
  //Turn back 360 degrees after 1 revolution
  step(1, 3130);
}

//Cycle where color is documented for each plant (used with waterCycle function)
void colorInput() 
{
  //Repeat for 12 plants
  for (int i=0;i<12;i++) 
  {
    //Wait and check color
    int color = 0;
    delay(10000);
    color = colorCheck();
    
    //Check to make sure inputted color is valid. If it is, add to updatingCalculatedArray
    if (color >= 40 && color <= 80) 
    {
      updatingCalculatedArray[i] = color*waterForPlant[i]  ;
    } else if (updatingCalculatedArray[i] != 0) 
    {
      
    } else 
    {
      updatingCalculatedArray[i] = (ColorArray[topNumber])*waterForPlant[i];
    }

    //Turn to next plant
    step(0,3200/12);
    delay(500);
  }
  
  //Turn back 360 degrees after 1 revolution
  step(1, 3130);
}

//Used after waterCycle/colorInput to narrow to single watering volume
void narrow() 
{
  //Average values of plants receiving same volume of water
  int calculated_2;
  int calculated_1;
  int calculated0;
  int calculated1;
  int calculated2;
  calculated_2 = (updatingCalculatedArray[1] + updatingCalculatedArray[6])/2;
  calculated_1 = (updatingCalculatedArray[2] + updatingCalculatedArray[7])/2;
  calculated0 = (updatingCalculatedArray[0] + updatingCalculatedArray[3]+ updatingCalculatedArray[8] + updatingCalculatedArray[11])/4;
  calculated1 = (updatingCalculatedArray[4] + updatingCalculatedArray[9])/2;
  calculated2 = (updatingCalculatedArray[5] + updatingCalculatedArray[10])/2;

  //Find ideal watering volume, using lesser volume as tie-breaker if needed
  if (calculated_2 >= calculated_1 && calculated_2 >= calculated0 && calculated_2 >= calculated1 && calculated_2 >= calculated2) 
  {
    narrowedWater = topWater-2;
    narrowedHSV = calculated_2/(topWater-2);
  } else if (calculated_1 >= calculated0 && calculated_1 >= calculated1 && calculated_1 >= calculated2) 
  {
    narrowedWater = topWater-1;
    narrowedHSV = calculated_1/(topWater-1);
  } else if (calculated0 >= calculated1 && calculated0 >= calculated2) 
  {
    narrowedWater = topWater;
    narrowedHSV = calculated0/(topWater);
  } else if (calculated1 >= calculated2) 
  {
    narrowedWater = topWater+1;
    narrowedHSV = calculated1/(topWater+1);
  } else 
  {
    narrowedWater = topWater+2;
    narrowedHSV = calculated2/(topWater+2);
  }

  //populate updatedWaterArray (will gradually update)
  for (int i=0;i<12;i++) 
  {
    updatedWaterArray[i] = narrowedWater;
  }
}

//Used with compareWaterCycle. Compares color read with ideal color and updates watering volume if needed
void compare(int color, int plantNumber) 
{
  long difference;

  //update average change for each plant using AI method
  averageArray[plantNumber] = updateAverageChange(plantNumber, color, updatedWaterArray[plantNumber], sizeof(updatedWaterArray));

  Serial.println("Distance");

  //Waits for response from VB.net program with total area of plant
  while (dataPassed == false) {
    if (Serial.available() > 0) {
       Area = Serial.readString().toInt();
       Area=Area/1000;
       dataPassed = true;
    }
  } 
  
  //If color is + or - 5% away from ideal color, update watering volume based on average change
  if (color >= 120 && color <= 200) 
  {
    if (color > (narrowedHSV * 1.05)) 
    {
      difference = color-narrowedHSV;
      updatedWaterArray[plantNumber] = updatedWaterArray[plantNumber]-(difference*averageArray[plantNumber]);
    } else if (color < (narrowedHSV * 0.95)) 
    {
      difference = narrowedHSV-color;
      updatedWaterArray[plantNumber] = updatedWaterArray[plantNumber]+(difference*averageArray[plantNumber]);
    }
  }
  //Set updated watering volume * area of plant conversion
  updatedWaterArray[plantNumber] = updatedWaterArray[plantNumber]*(2*Area);
}

//Send message to VB.net program to analyze the full data set and create a regression function (AI Implementation using dynamic linear regression)
//Based off averageChange method but includes more points as data set grows
float updateAverageChange(int plantNumber, int newColor, int newWater, int n){
  String printString;
  printString += "Average ";
  printString += plantNumber;
  printString += " ";
  printString += newColor;
  printString += " ";
  printString += newWater;
  printString += " ";
  printString += n;
  Serial.println(printString);
  
  //Wait for response from VB.net program with slope of function
  while (dataPassed == false) {
    if (Serial.available() > 0) {
      return Serial.readString().toInt();
      dataPassed = true;
    }
  }
}

//Program runs through loop infinitely
void loop() 
{
  //Check to see if Demo is needed
  while (dataPassed == false) {
    if (Serial.available() > 0) {
      String input = Serial.readString();
       if (input.equals("Demo")) {
         doDemo = true;
         demoDone = false;
       }
       dataPassed = true;
     }
  }
  
  if (doDemo == false) {
  //Fill tube when program is first run
    if (messageGiven == false) 
    {
      delay(5000);
      analogWrite(5, motorSpeed);
      delay(20000);
      analogWrite(5, LOW);
      messageGiven = true;
      delay(5000);
    }
  
    //Run colorInput and waterCycle for 4 days 10x daily
    if (narrowDone == false) 
    {
      for (int x = 0; x<4; x++) 
      {
        for (int a = 0; a<10; a++) 
        {
          delay(5000);
          colorInput();
          delay(5000);
          waterCycle();
          long DelayTime;
          DelayTime = 86400000/10-5800-(10000*12);
          delay(DelayTime);
        }
      }
    narrow();
    narrowDone = true;
    }

    //After 4 days, run compareWaterCycle 10x daily until user stops program
    for (int a = 0; a<10; a++) 
    {
      compareWaterCycle();
      long DelayTime;
      DelayTime = 86400000/10-5800-(10000*12);
      delay(DelayTime);
    }

    //Print total water given to each plant
    for (int q = 0; q<10; q++) 
    {
      Serial.println(TotalWater[q]);
    }
    
  } else if (doDemo == true && demoDone == false){
      //Run for 2 plants
      for (int x = 0; x<2; x++) {
        step(1,3200/12);
        delay(500);
        
        //Collect distance from ultrasonic sensor
        double Distance;
        Distance = ultraSensor.distanceInch();
        if (Distance > 100) {
          Distance = ultraSensor.distanceInch();
        }
        
        //Send message to VB.program to continue Demo
        Serial.print("demoStart ");
        Serial.print(Distance);
        Serial.print(" ");
        Serial.print(x);
        dataPassed = false;
        
        //Wait for response for how much to water plants
        while (dataPassed == false) {
          if (Serial.available() > 0) {
            int input = Serial.readString().toInt();
            analogWrite(5, motorSpeed);
            delay(input*2000);
            analogWrite(5, LOW);
            dataPassed = true;
          }
        }
      }
    demoDone = true;
  } 
}
