#include <HTTPClient.h>
#include <Arduino.h>
#include <WiFi.h>
#include <dht11.h>


// #include <MySQL_Connection.h>
// #include <MySQL_Cursor.h>
// #include <MySQL_Encrypt_Sha1.h>
// #include <MySQL_Packet.h>

#define DHT11PIN        17  //Temperature and humiddity sensor pin
#define LED_BUILTIN 27  //LED pins

dht11 DHT11;

const char* ssid = "AndroidHotspot_Jun"; //"AndroidHotspot_Jun"; // Enter wifi name// JJ phone
const char* password = "smartfarm"; //"smartfarm"; // Enter wifi password //1234567890

// Stirng URL = "http:// ip address/project_folder/project_filename.php"
String HOST_NAME = "http://192.168.128.33"; // REPLACE WITH YOUR PC's IP ADDRESS //172.20.15.202 //172.23.122.1
String PHP_FILE_NAME   = "/iot_sensor_project/insert_data.php";  //REPLACE WITH YOUR PHP FILE NAME
String Server_URL = HOST_NAME + PHP_FILE_NAME;
// there is some error which http code show -1, and it happens when esp32 board and computer connect different wifi.
// To figure out this problem, laptop and esp32 board have to connect in same wifi.


int temperature = 0;
int humidity =0;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  delay(100);

  
  Serial.println("DHT11 Test working");
  Serial.print("LIBRARY VERSION : ");
  Serial.println(DHT11LIB_VERSION);

  //Initialize wifi
  
  WiFi.begin(ssid, password);
  //Scan for wifi. If connection fails, stay in connecting, and execute "while" loop
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  //Connected. Print the IP address
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());


}

void loop() {
  // put your main code here, to run repeatedly:

}
