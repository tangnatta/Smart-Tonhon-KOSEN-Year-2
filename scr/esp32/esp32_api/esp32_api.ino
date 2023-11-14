#include <FreeRTOS.h>
#include <Wire.h>
#include <QMC5883LCompass.h>
#include <Stepper.h>
#include "UltrasonicV2.hpp"

#define Declination -0.00669

#define IN1 25
#define IN2 33
#define IN3 32
#define IN4 35
#define stepsPerRevolution 2048

Stepper stepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

const int trigPin = 5;
const int echoPin = 18;
Ultrasonic ultrasonic = Ultrasonic(echoPin, trigPin);

const int buzzer = 23;

QMC5883LCompass compass;

int changeAngle = 0;
double heading = 0;
double distance = 0;

enum
{
    STOP,
    FAST,
    NORMAL,
    SLOW
} buzzerState = STOP;

double getHeading()
{
    int x, y, z;

    // Read compass values
    compass.read();

    x = compass.getX();
    y = compass.getY();
    z = compass.getZ();

    // Serial.print("X: ");
    // Serial.print(x);
    // Serial.print("   Y: ");
    // Serial.print(y);
    // Serial.print("   Z: ");
    // Serial.println(z);

    double Heading = atan2((double)y, (double)x) + Declination;
    if (Heading > 2 * PI) /* Due to declination check for >360 degree */
        Heading = Heading - 2 * PI;
    if (Heading < 0) /* Check for sign */
        Heading = Heading + 2 * PI;

    Heading = Heading * 180 / PI;

    // Serial.print("Heading");
    // Serial.println(Heading);
    return Heading;
}

void updateBuzzer(void *parameter)
{
    for (;;)
    {
        switch (buzzerState)
        {
        case STOP:
            digitalWrite(buzzer, HIGH);
            break;

        case FAST:
            digitalWrite(buzzer, LOW);
            vTaskDelay(250 / portTICK_PERIOD_MS);
            digitalWrite(buzzer, HIGH);
            break;

        case NORMAL:
            digitalWrite(buzzer, LOW);
            vTaskDelay(250 / portTICK_PERIOD_MS);
            digitalWrite(buzzer, HIGH);
            vTaskDelay(1000 / portTICK_PERIOD_MS);
            break;

        case SLOW:
            digitalWrite(buzzer, LOW);
            vTaskDelay(250 / portTICK_PERIOD_MS);
            digitalWrite(buzzer, HIGH);
            vTaskDelay(2000 / portTICK_PERIOD_MS);
            break;

        default:
            digitalWrite(buzzer, HIGH);
            break;
        }

        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}

void updateSensor()
{
    distance = ultrasonic.getDistance();

    heading = getHeading();

    // Serial.print("distance: ");
    // Serial.println(distance);

    // Serial.print("heading: ");
    // Serial.println(heading);

    // Serial.println("-------");
}

void updateSensorData(void *parameter)
{
    updateSensor();

    vTaskDelay(1000 / portTICK_PERIOD_MS);
}

void setup_task()
{
    // xTaskCreate(
    //     updateSensorData,   // Function that should be called
    //     "Read sensor data", // Name of the task (for debugging)
    //     2000,               // Stack size (bytes)
    //     NULL,               // Parameter to pass
    //     2,                  // Task priority
    //     NULL                // Task handle
    // );

    xTaskCreate(
        updateBuzzer,    // Function that should be called
        "Update Buzzer", // Name of the task (for debugging)
        1000,            // Stack size (bytes)
        NULL,            // Parameter to pass
        1,               // Task priority
        NULL             // Task handle
    );
}

void setup()
{
    Serial.begin(115200);

    // Initialize the Buzzer.
    pinMode(buzzer, OUTPUT);

    // Initialize I2C.
    Wire.begin();
    // Initialize the Compass.
    compass.init();

    stepper.setSpeed(12);

    setup_task();
}

void loop()
{
    if (Serial.available() > 0)
    {
        char c = Serial.read();
        switch (c)
        {
        case 'B':
            c = Serial.parseInt();
            switch (c)
            {
            case 1:
                buzzerState = FAST;
                Serial.println("FAST");
                break;

            case 2:
                buzzerState = NORMAL;
                Serial.println("NORMAL");
                break;

            case 3:
                buzzerState = SLOW;
                Serial.println("SLOW");
                break;

            case 0:
                buzzerState = STOP;
                Serial.println("STOP");
                break;

            default:
                break;
            }
            break;

        case 'S':
            changeAngle = Serial.parseInt();
            stepper.step(changeAngle);
            Serial.println(changeAngle);
            break;

        case 'D':
            updateSensor();
            Serial.println(distance);
            break;

        case 'H':
            updateSensor();
            Serial.println(heading);
            break;

        case 'I':
            Serial.println("Starting communication");
            break;

        default:
            break;
        }
    }
}