#include <Stepper.h>
#define STEPS 100
Stepper stepper(STEPS, 8, 9, 10, 11);
int previous = 0;
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
void setup()
{
    stepper.setSpeed(30);
    Serial.begin(9600);
    if (!mag.begin())
    {
        Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
        while (1)
            ;
    }
}

void loop()
{
    sensors_event_t event;
    mag.getEvent(&event);
    Serial.print("X: ");
    Serial.print(event.magnetic.x);
    Serial.print(" ");
    Serial.print("Y: ");
    Serial.print(event.magnetic.y);
    Serial.print(" ");
    Serial.print("Z: ");
    Serial.print(event.magnetic.z);
    Serial.print(" ");
    Serial.println("uT");
    float heading = atan2(event.magnetic.y, event.magnetic.x);
    float declinationAngle = 0.22;
    heading += declinationAngle;
    if (heading < 0)
    {
        heading += 2 * PI;
    }
    if (heading > 2 * PI)
    {
        heading -= 2 * PI;
        float headingDegrees = heading * 180 / M_PI;
        Serial.print("Heading (degrees): ");
        Serial.println(headingDegrees);
        delay(500);
    }

    int val = analogRead(0);
    stepper.step(val - previous);
    previous = val;
}
