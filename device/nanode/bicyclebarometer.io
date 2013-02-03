#include <EtherCard.h>
#include <Servo.h> 

Servo myservo;
int pos = 0;    // variable to store the servo position 

// ethernet interface mac address, must be unique on the LAN
static byte mymac[] = { 0x00,0x00,0x00,0x00,0x00,0x00 };

byte Ethernet::buffer[700];
static uint32_t timer;

char website[] PROGMEM = "bicyclebarometer.oftcc.net";

int stringToInt(String value) {
  char valueArray[value.length() + 1];
  value.toCharArray(valueArray, sizeof(valueArray));
  return atoi(valueArray);
}

int parseResponse (const char* response) {
  //convert the char to a string so we can use string functions
  String response_string= "";
  response_string.concat(response);
  
  //split using '#' as a delimiter
  response_string = response_string.substring(response_string.indexOf('#') + 1, response_string.length());  
  
   // convert to an int
   
  return stringToInt(response_string);
}

// called when the client request is complete
static void my_callback (byte status, word off, word len) {
  Serial.println("Server responded");
  Ethernet::buffer[off+len] = 0;
  int value = parseResponse((const char*) Ethernet::buffer + off);
  Serial.print("Setting value to ");
  Serial.println(value);
  
  myservo.attach(9);
  myservo.write(180 - (180.0 / 100.0) * value);
  delay(4000); // allow time to move before detaiching
  myservo.detach();
}


void sweep(){
  myservo.attach(9);
  Serial.println("Start sweep");
  for(pos = 0; pos < 180; pos += 1){                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=1; pos-=1){                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  }
  Serial.println("End sweep");  
  myservo.detach();  
}

void setup () {
  
  sweep();
  
  Serial.begin(57600);
  Serial.println("\n[webClient]");

  if (ether.begin(sizeof Ethernet::buffer, mymac) == 0) 
    Serial.println( "Failed to access Ethernet controller");
  if (!ether.dhcpSetup())
    Serial.println("DHCP failed");

  ether.printIp("IP:  ", ether.myip);
  ether.printIp("GW:  ", ether.gwip);  
  ether.printIp("DNS: ", ether.dnsip);  

  if (!ether.dnsLookup(website))
    Serial.println("DNS failed");
    
  ether.printIp("SRV: ", ether.hisip);
}

void loop () {
  ether.packetLoop(ether.packetReceive());
  if (millis() > timer) {
    timer = millis() + 600000;
    Serial.println("Making request");
    ether.browseUrl(PSTR("/api"), "", website, my_callback);
  }
}
