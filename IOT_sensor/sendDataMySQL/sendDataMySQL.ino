#include <HTTPClient.h>
#include <Arduino.h>
#include <WiFi.h>
#include <dht11.h>


// #include <MySQL_Connection.h>
// #include <MySQL_Cursor.h>
// #include <MySQL_Encrypt_Sha1.h>
// #include <MySQL_Packet.h>

// Pin number
#define DHT11PIN        17  //Temperature and humiddity sensor pin
#define LEDPIN          27  //LED pin
//#define SERVOPIN        26  //Servo pin // we are not using servor pin right now
#define FANPIN1         19  //Fan IN+ pin
#define FANPIN2         18  //Fan IN- pin
#define STEAMPIN        35  //Steam sensor pin
#define LIGHTPIN        34  //Photoresistor pin
#define SOILHUMIDITYPIN 32  //Soil humidity sensor pin
#define WATERLEVELPIN   33  //Water level sensor pin
#define RELAYPIN        25  //Relay pin

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
String light;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  delay(100);

    // set pin mode
  pinMode(LEDPIN,OUTPUT);
  pinMode(STEAMPIN,INPUT);
  pinMode(LIGHTPIN,INPUT);
  // pinMode(SOILHUMIDITYPIN,INPUT);
  // pinMode(WATERLEVELPIN,INPUT);
  // pinMode(RELAYPIN,OUTPUT);
  // pinMode(FANPIN1,OUTPUT);
  // pinMode(FANPIN2,OUTPUT);

  
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

  Load_DHT11_data();

  light = String(analogRead(LIGHTPIN));
  Serial.println("Light value: " + String(light));

  String postData = "temperature=" + String(temperature) + " & humidity=" + String(humidity) + "& light=" + String(light);

  HTTPClient http;
  http.begin(Server_URL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpCode = http.POST(postData);

  String payload = http.getString();


  if(httpCode > 0) {
    // file found at server
    if(httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
    } else {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  
  http.end();  //Close connection
  
  Serial.print("server URL : "); Serial.println(Server_URL);
  Serial.print("Data: "); Serial.println(postData);
  Serial.print("httpCode: "); Serial.println(httpCode);
  Serial.print("payload: "); Serial.println(payload);
  Serial.println("--------------------------------------------------");

  delay(10000);


}


void Load_DHT11_data() {

  int chk = DHT11.read(DHT11PIN);

  //--------------------------
  // read sensor and check any error
  Serial.print("Read sensor: ");
  switch (chk)
  {
    case DHTLIB_OK: 
                Serial.println("OK"); 
                break;
    case DHTLIB_ERROR_CHECKSUM: 
                Serial.println("Checksum error"); 
                break;
    case DHTLIB_ERROR_TIMEOUT: 
                Serial.println("Time out error"); 
                break;
    default: 
                Serial.println("Unknown error"); 
                break;
  }

  temperature = DHT11.temperature;
  humidity = DHT11.humidity;

  //--------------
  // check any read fail
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    temperature = 0;
    humidity = 0;
  }
  //----------------

  Serial.printf("Temperature: %d °C\n", temperature);
  Serial.printf("Humidity: %d %%\n", humidity);

}

