#include <Stepper.h>
const int stepsPerRevolution = 2048;
const int trigPin = 5;
const int echoPin = 18;
const int buzzer = 23;
#define IN1 25
#define IN2 33
#define IN3 32
#define IN4 35
#define SOUND_SPEED 0.034

Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

long duration;
float distance;

void setup()
{
    Serial.begin(115200);     // Starts the serial communication
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT);  // Sets the echoPin as an Input
    pinMode(buzzer, OUTPUT);
    digitalWrite(buzzer, HIGH);

    myStepper.setSpeed(5);
}

void loop()
{
    // int steps = Serial.parseInt();
    // motor.step(steps);
    myStepper.step(stepsPerRevolution);
    // delay(50);

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * SOUND_SPEED / 2;

    Serial.print("Distance (cm): ");
    Serial.println(distance);
    // delay(0);

    if (distance > 200)
    {
        Serial.println("_");
    }
    else if (200 >= distance > 100)
    {
        Serial.println("Far");
        digitalWrite(buzzer, LOW);
        delay(500);
        digitalWrite(buzzer, HIGH);
        delay(500);
    }
    else if (100 >= distance > 50)
    {
        Serial.println("Middle");
        digitalWrite(buzzer, LOW);
        delay(500);
        digitalWrite(buzzer, HIGH);
        delay(500);
    }
    else if (distance <= 50)
    {
        Serial.println("Near");
        digitalWrite(buzzer, LOW);
        delay(500);
        digitalWrite(buzzer, HIGH);
        delay(500);
    }
    // delay(100);
}