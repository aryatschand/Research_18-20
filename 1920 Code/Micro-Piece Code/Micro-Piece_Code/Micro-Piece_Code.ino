/*
 WiFiEsp example: WebClient
 This sketch connects to google website using an ESP8266 module to
 perform a simple web search.
 For more details see: http://yaab-arduino.blogspot.com/p/wifiesp-example-client.html
*/

#include "WiFiEsp.h"
#include <Servo.h>

// Emulate MySerial on pins 6/7 if not present
#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(19, 18); // RX, TX
#endif

char ssid[] = "3xA Wi-Fi";            // your network SSID (name)
char pass[] = "parwan123";        // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status

const IPAddress server(192,168,86,32);

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0; 

// Initialize the Ethernet client object
WiFiEspClient client;

void setup()
{
  // initialize serial for debugging
  myservo.attach(9);
  Serial.begin(115200);
  // initialize serial for ESP module
  Serial1.begin(115200);
  // initialize ESP module
  WiFi.init(&Serial1);

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  // you're connected now, so print out the data
  Serial.println("You're connected to the network");

  printWifiStatus();

  Serial.println();
  Serial.println("Starting connection to server...");
  // if you get a connection, report back via serial
}

void loop()
{
  makeCall();
  //delay(200);
  //while (client.connected() || client.available())
  String result = "";
  for (int x = 0; x<10; x++)
{
  if (client.available())
  {
    String line = client.readStringUntil('\n');
    if (line.substring(0,6)=="return"){
      result=line;
    }
    Serial.println(line);
  }
  delay(1);
}
int comma = result.indexOf(",");
float volume = result.substring(6,comma-1).toFloat()*10;
if (volume > 0){
  Serial.println(volume);
  for (pos = 0; pos <= volume; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  myservo.write(90);
}
delay(2000);
  // if the server's disconnected, stop the client
  //if (!client.connected()) {
  //  Serial.println();
  //  Serial.println("Disconnecting from server...");
  //  client.stop();

    // do nothing forevermore
    //while (true);
  //}
}

void makeCall() {
  Serial.println("makeCall");
  if (client.connect(server, 5000)) {
    Serial.println("Connected to server");
    // Make a HTTP request
    client.println("GET / HTTP/1.1");
    client.println("Host: 192.168.86.32:5000");
    client.println("Connection: Keep-Alive");
    client.println();    
  }
}


void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
