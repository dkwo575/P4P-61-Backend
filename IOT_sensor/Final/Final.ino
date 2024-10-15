#include <analogWrite.h>


#include <Arduino.h>
#include <WiFi.h>


// Import library
#include <dht11.h> // library for temperature and humidity sensor
#include <HTTPClient.h> // library for HTTP client
// #include <LiquidCrystal_I2C.h>
// #include <analogWrite.h>




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
// LiquidCrystal_I2C lcd(0x27,16,2);

const char* ssid = "AndroidHotspot_Jun";  //"AndroidHotspot_Jun"; // Enter wifi name
const char* password = "smartfarm";   //"smartfarm"; // Enter wifi password

String HOST_NAME = "http://192.168.226.33"; // REPLACE WITH YOUR PC's IP ADDRESS //172.20.15.202 //172.23.122.1
String PHP_FILE_NAME = "/iot_sensor_project/insert_data.php"; // Replace with your php file name
String Server_URL = HOST_NAME + PHP_FILE_NAME;


int temperature = 0;
int humidity = 0;
int light = 0;
int waterLevel = 0;
int soilHumidity = 0;
int steam = 0;
// float temperature = 0;
// float humidity = 0;
// float light = 0;
// float waterLevel = 0;
// float soilHumidity = 0;
// float steam = 0;



// WebServer server(80); //Set the server port to 80. Enter the website by IP address rather than the port number.



//char user[] = "root" // Enter MySQL user name
//char password_[] = "smartfarm" // Enter MySQL password

// String Merge_Data(void) {

//   //Define all variable as string
//   String dataBuffer;
//   String Humidity;
//   String Temperature;
//   String Steam;
//   String Light;
//   String SoilHumidity;
//   String WaterLevel;

//     //Acquire values
//   int chk = DHT11.read(DHT11PIN); //Read the temperature and humidity sensor
//   //Steam sensor
//   Steam = String(analogRead(STEAMPIN) / 4095.0 * 100);
//   //Photoresistor
//   Light = String(analogRead(LIGHTPIN));
//   //Soil humidity sensor
//   int shvalue = analogRead(SOILHUMIDITYPIN) / 4095.0 * 100 * 2.3;
//   shvalue = shvalue > 100 ? 100 : shvalue;
//   SoilHumidity = String(shvalue);
//   //Water level sensor
//   int wlvalue = analogRead(WATERLEVELPIN) / 4095.0 * 100 * 2.5;
//   wlvalue = wlvalue > 100 ? 100 : wlvalue;
//   WaterLevel = String(wlvalue);
//   //Temperature
//   Temperature = String(DHT11.temperature);
//   //Humidity
//   Humidity = String(DHT11.humidity);


  
// }

//Initialize the website
// void handleRoot() {
//   //Used to send HTTP to the client-side for response, sending 200 means success.
//   server.send(200, "text/html", "<h1>Hello, World!</h1>");
// }

// setup the code
void setup() {
  Serial.begin(115200);
  delay(500);

  // set pin mode
  pinMode(LEDPIN,OUTPUT);
  pinMode(STEAMPIN,INPUT);
  pinMode(LIGHTPIN,INPUT);
  pinMode(SOILHUMIDITYPIN,INPUT);
  pinMode(WATERLEVELPIN,INPUT);
  // pinMode(RELAYPIN,OUTPUT);
  // pinMode(FANPIN1,OUTPUT);
  // pinMode(FANPIN2,OUTPUT);
  
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

  // server.on("/", handleRoot);
  // //Start server
  // server.begin();
  // Serial.println("Web server started");

}

void loop() {
  
  Load_DHT11_Data();
  Load_Light_Data();

  Load_Wlevel_Data();
 
  Load_Soil_Data();

  Load_Steam_Data();


  String postData = "temperature=" + String(temperature) + " & humidity=" + String(humidity) + " & light=" + String(light) + " & WaterLevel=" + String(waterLevel) +  " & SoilHumidity=" + String(soilHumidity) + " & Steam=" + String(steam);
  // " & WaterLevel=" + String(waterLevel) +  "SoilHumidity=" + String(soilHumidity) + 
  HTTPClient http;
  http.begin(Server_URL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpCode = http.POST(postData);

  String payload = http.getString();

  // server.handleClient();
  if(httpCode > 0) {
    // file found at server
    if(httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
      analogWrite(LEDPIN, HIGH);        // Turn on the led on if the http post succesfully.
      delay(1000);                      // wait for a second
      digitalWrite(LEDPIN, LOW);   // turn the LED off by making the voltage LOW
      delay(1000);
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


  delay(10000); // post data every 10 seconds

  
}

void Load_DHT11_Data(){
  
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

void Load_Light_Data() {

  // Read the value of photoresistor
  // light = String(analogRead(LIGHTPIN));
  light = analogRead(LIGHTPIN);
  
  //=======
  // //check any read fail
  // if (isnan(light)) {
  //   Serial.println("Failed to read from photoresistor sensor!");
  //   light = 0;
  // }
  //----------------

  Serial.println("Light value: " + String(light));
  // delay(500);
}

void Load_Wlevel_Data() {

  int wlvalue = analogRead(WATERLEVELPIN) / 4095.0 * 100 * 2.5;
  // int wlvalue = analogRead(WATERLEVELPIN) / 1023.0 * 100 ;
  wlvalue = wlvalue > 100 ? 100 : wlvalue;
  waterLevel = int (wlvalue);
  Serial.println("Water level value: " + String(waterLevel));
}



void Load_Soil_Data(){
  // Soil humidity sensor
  int shvalue = analogRead(SOILHUMIDITYPIN) / 4095.0 * 100 * 2.3;
  // int shvalue = analogRead(SOILHUMIDITYPIN) / 1023.0 * 100;
  shvalue = shvalue > 100 ? 100 : shvalue;
  soilHumidity = int(shvalue);
  Serial.println("soilHumidity value: " + String(soilHumidity));
}


void Load_Steam_Data(){
  // int steamValue = analogRead(STEAMPIN);
  steam = int(analogRead(STEAMPIN) / 4095.0 * 100);
  // steam = int(analogRead(STEAMPIN) / 1023.0 * 100);
  //=======
  //check any read fail
  // if (isnan(steam)) {
  //   Serial.println("Failed to read from steam sensor!");
  //   steam = 0;
  // }
  //----------------
  Serial.println("Steam value: " + String(steam));
  // delay(500);
}



