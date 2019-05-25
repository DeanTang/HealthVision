int photosensor = A0;//light sensor connected to A0


// Declaring variables
int analogvalue;  
char light[30];


void setup() {

	Serial.begin();
    
    pinMode(D6, OUTPUT);
    pinMode(D7, OUTPUT);

	//Particle.variable("AnalogData", analogvalue);

    Particle.variable("light", light);

    Particle.subscribe("hook-response/light", myHandler, MY_DEVICES);
    
    Particle.function("led", led);
}

void myHandler(const char *event, const char *data) {

}

int led(String arg)
{
    if (arg == "ON")
    {
        digitalWrite(D6, HIGH);
        digitalWrite(D7, HIGH);
    }
    if (arg== "OFF")
    {
        digitalWrite(D6, LOW);
        digitalWrite(D7, LOW);
    }
    if (arg=="blink")
    {
        digitalWrite(D6, HIGH);
        digitalWrite(D7, HIGH);
        
        delay(5000);
        
        digitalWrite(D6, LOW);
        digitalWrite(D7, LOW);
    }
    return 0;
}

void loop() {

    //Reading light value
	analogvalue = analogRead(photosensor);
	//Converting light value into string for particle.publish()
    sprintf(light,"%d", analogvalue);
    
    
    //Publishing to thinkspeak
	Particle.publish("light", light, PRIVATE);


	delay(2000);
}
