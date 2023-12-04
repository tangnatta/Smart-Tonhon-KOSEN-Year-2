from communication import ArduinoCommunication
from enum import Enum


class buzzer_mode(Enum):
    STOP = 0
    FAST = 1
    NORMAL = 2
    SLOW = 3


esp32 = ArduinoCommunication()
esp32.clear_input()


def getDistance():
    return float(esp32.write_read('D')[0])


def getHeading():
    return float(esp32.write_read('H')[0])


def changeStepper(angle: int):
    step = angle * 2048 * 2 / 360
    return float(esp32.write_read('S ' + str(step))[0])


def setBuzzer(mode: buzzer_mode):
    return str(esp32.write_read('B ' + str(mode.value))[0])


if __name__ == "__main__":
    import time

    print(getDistance())
    print(getHeading())
    print(changeStepper(180))
    # print(setBuzzer(buzzer_mode.SLOW))

    # time.sleep(5)

    print(getDistance())
    print(getHeading())
    # print(changeStepper(90))
    # print(setBuzzer(buzzer_mode.STOP))
