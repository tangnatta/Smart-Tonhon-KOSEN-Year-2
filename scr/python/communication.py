import glob
import sys
import serial
import serial.tools.list_ports as COMs
import numpy as np
import time


class ArduinoCommunication:
    def __init__(self):
        self.ports = self.port_search()
        self.ser = serial.Serial()
        self.ser.port = self.ports[0]
        self.ser.baudrate = 115200
        self.ser.open()
        time.sleep(0.1)
        self.ser.reset_output_buffer()  # clear output buffer

    # Search for available ports
    def port_search(self):
        if sys.platform.startswith('win'):  # Windows
            ports = ['COM{0:1.0f}'.format(ii) for ii in range(1, 256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):  # MAC
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Machine Not pyserial Compatible')

        arduinos = []
        for port in ports:  # loop through to determine if accessible
            if len(port.split('Bluetooth')) > 1:
                continue
            try:
                ser = serial.Serial(port)
                ser.close()
                # if we can open it, consider it an arduino
                arduinos.append(port)
            except (OSError, serial.SerialException):
                pass
        return arduinos

    # Just write to the serial port
    def write(self, x):
        self.ser.write(bytes(x, 'utf-8'))

    # Write to the serial port and read the response
    def write_read(self, x):
        self.ser.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = self.ser.readline().decode('utf-8', errors='ignore').rsplit()
        return data

    # clear NULL DATA
    def clear_input(self):
        time.sleep(0.1)
        self.write('I')  # send a character to clear the input buffer
        time.sleep(0.1)
        while True:
            val = self.ser.readline().decode('utf-8', errors='ignore').rsplit()
            print(val)
            if val == ['Starting', 'communication']:
                print('Communication started')
                break


if __name__ == '__main__':
    arduino = ArduinoCommunication()
    arduino.clear_input()

    while True:
        command_terminal = input('Enter command: ')
        response = arduino.write_read(command_terminal)
        print(response)
