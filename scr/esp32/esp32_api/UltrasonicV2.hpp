//! HC-SR04 Module ONLY

#include <Arduino.h>

class Ultrasonic
{
private:
    uint8_t ECHO_PIN, TRIG_PIN;
    double ULTRASONIC_SPEED = 0.034; // centimeter per microsecond

public:
    ~Ultrasonic() {}
    Ultrasonic() {}
    Ultrasonic(uint8_t ECHO_PIN, uint8_t TRIG_PIN)
    {
        this->ECHO_PIN = ECHO_PIN;
        this->TRIG_PIN = TRIG_PIN;
        pinMode(this->ECHO_PIN, INPUT);
        pinMode(this->TRIG_PIN, OUTPUT);
    }

    /* Create a new instance of the Ultrasonic class.
     * @param ECHO_PIN (uint8_t) : ECHO PIN (digital pin)
     * @param TRIG_PIN (uint8_t) : TRIG PIN (digital pin)
     * @param ULTRASONIC_SPEED (double) : SPEED OF ULTRASONIC (centimerter per microsecond)
     */
    Ultrasonic(uint8_t ECHO_PIN, uint8_t TRIG_PIN, double ULTRASONIC_SPEED)
    {
        this->ECHO_PIN = ECHO_PIN;
        this->TRIG_PIN = TRIG_PIN;
        this->ULTRASONIC_SPEED = ULTRASONIC_SPEED; // centimeter per microsecond
        pinMode(this->ECHO_PIN, INPUT);
        pinMode(this->TRIG_PIN, OUTPUT);
    }

    /* Get the roundtrip time duration of ultrasonic
     * @return duration (double) : duration in microsecond
     */
    unsigned long getDuration()
    {
        digitalWrite(this->TRIG_PIN, LOW);
        delayMicroseconds(2);
        digitalWrite(this->TRIG_PIN, HIGH);
        delayMicroseconds(10);
        digitalWrite(this->TRIG_PIN, LOW);
        return pulseIn(this->ECHO_PIN, HIGH);
    }

    /* Get the distance of object in front of the sensor
     * @return distance (double) : distance in centimeter
     */
    double getDistance()
    {
        return this->getDuration() * this->ULTRASONIC_SPEED / 2;
    }
};
