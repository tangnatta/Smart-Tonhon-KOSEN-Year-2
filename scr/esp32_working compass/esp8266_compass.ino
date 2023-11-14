
/*
  GY-271 Compass
  modified on 02 Sep 2020
  by Mohammad Reza Akbari @ Electropeak
  Home
*/

// I2C Library
#include <Wire.h>
// QMC5883L Compass Library
#include <QMC5883LCompass.h>

#define Declination -0.00669

QMC5883LCompass compass;

void setup()
{
    // Initialize the serial port.
    Serial.begin(115200);
    // Initialize I2C.
    Wire.begin();
    // Initialize the Compass.
    compass.init();
}

void loop()
{
    int x, y, z;

    // Read compass values
    compass.read();

    x = compass.getX();
    y = compass.getY();
    z = compass.getZ();

    Serial.print("X: ");
    Serial.print(x);
    Serial.print("   Y: ");
    Serial.print(y);
    Serial.print("   Z: ");
    Serial.println(z);

    double Heading = atan2((double)y, (double)x) + Declination;
    if (Heading > 2 * PI) /* Due to declination check for >360 degree */
        Heading = Heading - 2 * PI;
    if (Heading < 0) /* Check for sign */
        Heading = Heading + 2 * PI;

    Serial.print("Heading");
    Serial.println(Heading * 180 / PI);

    delay(300);
}