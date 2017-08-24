#!/usr/bin/python
# -*- coding: UTF-8 -*-

#### -m PyInstaller --onefile

import serial
import sys
import glob
import os
import ConfigParser


class Config:
    def __init__(self, model):
        if '' == model:
            model = 'Default'
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.getcwd() + '/config.ini')
        self.baud = self.ConfigSectionMap(model)['baud']
        self.port = self.ConfigSectionMap(model)['port']
        self.light = self.ConfigSectionMap(model)['light']
        self.Shutter = self.ConfigSectionMap(model)['shutter']
        self.Gain = self.ConfigSectionMap(model)['gain']

        self.light_max = self.ConfigSectionMap(model)['light_max']
        self.shutter_max = self.ConfigSectionMap(model)['shutter_max']
        self.gain_max = self.ConfigSectionMap(model)['gain_max']

        self.timeout = self.ConfigSectionMap(model)['timeout']

        self.isRs232 = int(self.baud) - 115200 <= 0

    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def dump(self):
        print(', '.join("%s: %s" % item for item in vars(self).items()))


def connect(config):
    if config.isRs232:
        ser = serial.Serial(config.port, config.baud, timeout=int(config.timeout))
    else:
        ser = serial.Serial(config.port, config.baud, timeout=int(config.timeout), xonxoff=True)

    if ser.isOpen():
        ser.flushInput()  # flush input buffer, discarding all its contents
        ser.flushOutput()  # flush output buffer, aborting current output
        # and discard all that is in buffer
        print(ser.name + ' is open...')
    else:
        print ser.name + ' can not open...'

    return ser


def handshake(ser):
    ser.write('Hello'.encode('ascii') + '\r\n')
    count = 10
    while True:
        out = ser.readline()
        if len(out) == 0 and count > 0:
            count -= 1
            continue
        break
    if len(out) > 0:
        print out
    else:
        print 'Devices No response.'

    return len(out) > 0


def setDefault(config, ser):
    setShutter(config.Shutter, ser)
    setGain(config.Gain, ser)
    setLight(config.light, ser)


def setGain(ev, ser):
    print sendComm('Gain' + str(ev), ser)


def setShutter(m_time, ser):
    print sendComm('Shutter' + str(m_time), ser)


def setLight(level, ser):
    print sendComm('light' + str(level), ser)


def showVersion(ser):
    print sendComm('version', ser)


def setDevicesDefault(ser):
    sendComm('quit', ser)


def sendComm(command, ser):
    ser.write(command.encode('ascii') + '\r\n')

    if command == 'quit':
        return
    timeoutCount = 5
    while True:
        out = ser.readline()
        if len(out) == 0 and timeoutCount > 0:
            timeoutCount -= 1
            continue
        break
    sys.stdout.flush()
    return out


def getImage(quality, ser, rs232):
    if '' == quality:
        quality = 'image85'
    ser.write(quality.encode('ascii') + '\r\n')
    buf = ""
    starting = -1
    while True:
        if rs232:
            tmp = ser.read(8192)
        else:
            tmp = ser.read_all()
        if len(tmp) == 0:
            continue

        if tmp.find('<<start>>') != -1:
            if rs232:
                starting = buf.find('<<start>>') + 10
            else:
                starting = buf.find('<<start>>') + 18
            buf = tmp[starting:]
            continue

        if tmp.find('<<EOF>>') != -1:
            buf += tmp[:tmp.find('<<EOF>>')]
            print 'OK'
            break

        if starting != -1:
            buf += tmp
            print len(buf)

    ser.flushInput()
    ser.flushOutput()
    filename = "Capture.jpg"
    nf = open(filename, "wb+")
    nf.write(bytearray(buf))
    nf.flush()
    nf.close()


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def serial_devices_name(_ports):
    for port in _ports:
        try:
            s = serial.Serial(port, 115200, timeout=1)
            s.write(bytes('AT+CGMI' + '\r\n'))
            response = s.read_all()
            if response.startswith('update, version, light, Shutter, Gain, image, q'):
                s.close()
                return port
            s.close()
        except (OSError, serial.SerialException):
            pass
    return ''


def serial_baud(_port):
    s = _port[3:len(_port)]
    try:
        number = int(s)
    except ValueError:
        return -1
    if number > 3:
        return 921600
    else:
        return 115200


if __name__ == "__main__":
    #ports = serial_ports()
    #s_port = serial_devices_name(ports)
    #s_baud = serial_baud(s_port)

    #if s_baud == -1:
    #    print s_port
    #    exit(0)

    c = Config('')
    #c.baud = s_baud
    #c.port = s_port
    #c.isRs232 = int(c.baud) - 115200 <= 0
    c.dump()
    serConnector = connect(c)

    Has_response = handshake(serConnector)

    if Has_response:
        setDefault(c, serConnector)

    while Has_response:
        cmd = raw_input("Enter command or 'exit': \b")        # for Python 3
        # cmd = input("Enter command or 'exit':")             # for Python 2
        if cmd == 'exit':
            break
        elif cmd == '':
            getImage(cmd, serConnector, c.isRs232)
            os.startfile("Capture.jpg")
        else:
            sendComm(cmd, serConnector)

    print("exit......")
    serConnector.close()
    exit(0)
