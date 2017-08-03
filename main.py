#!/usr/bin/python


#### -m PyInstaller --onefile

import time
import serial
import sys
import os
import ConfigParser


# version, light, Shutter, Gain, image, quit

class Config:
    def __init__(self, model):
        if '' == model:
            model = 'Default'
        Config = ConfigParser.ConfigParser()
        Config.read(os.getcwd() + '/config.ini')
        self.baud = self.ConfigSectionMap(model)['baud']
        self.port = self.ConfigSectionMap(model)['port']

        self.light = self.ConfigSectionMap(model)['light']
        self.Shutter = self.ConfigSectionMap(model)['shutter']
        self.Gain = self.ConfigSectionMap(model)['gain']

        self.light_max = self.ConfigSectionMap(model)['light_max']
        self.shutter_max = self.ConfigSectionMap(model)['shutter_max']
        self.gain_max = self.ConfigSectionMap(model)['gain_max']

        self.timeout = self.ConfigSectionMap(model)['timeout']

        self.isRs232 = self.baud <= 115200

    def ConfigSectionMap(self, section):
        dict1 = {}
        options = c.options(section)
        for option in options:
            try:
                dict1[option] = c.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def dump(self):
        print(', '.join("%s: %s" % item for item in vars(self).items()))


def connect(config):
    serialer = serial.serial_for_url(config.port, config.baud, timeout=config.timeout, xonxoff=True)
    # ser = serial.Serial(config.port, config.baud, timeout=config.timeout, xonxoff=True)
    if serialer.isOpen():
        print(serialer.name + ' is open...')
    else:
        print serialer.name + ' can not open...'

    return serialer


'''    if ser.is_open:
        while True:
            ser.write('Hello'.encode('ascii') + '\r\n')
            timeoutCount = 5
            while True:
                out = ser.readline()
                if len(out) == 0 and timeoutCount > 0:
                    timeoutCount -= 1
                    continue
                break
'''


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


def setDefault(config):
    setShutter(config.Shutter)
    setGain(config.Gain)
    setLight(config.light)


def setGain(ev):
    sendComm('Gain' + str(ev))


def setShutter(m_time):
    sendComm('Shutter' + str(m_time))


def setLight(level):
    sendComm('light' + str(level))


def sendComm(command):
    serConnector.write(command.encode('ascii') + '\r\n')
    while True:
        out = serConnector.readline()
        if len(out) == 0:
            continue
        break
    print out
    sys.stdout.flush()


def getImage(quality):
    if '' == quality:
        quality = 'image85'
    serConnector.write(quality.encode('ascii') + '\r\n')
    buf = ""
    starting = -1
    while True:
        if not c.isRs232:
            tmp = serConnector.read(8192)
        else:
            tmp = serConnector.read(8192)
        if len(tmp) == 0:
            continue

        if tmp.find('<<start>>') != -1:
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

    filename = "Capture.jpg"
    nf = open(filename, "wb+")
    nf.write(bytearray(buf))
    nf.flush()
    nf.close()
    os.startfile(filename)


def _exit():
    print("exit......")
    serConnector.close()
    exit(0)


if __name__ == "__main__":
    c = Config('')
    c.dump()
    serConnector = connect(c)

    Has_response = handshake(serConnector)

    if Has_response:
        setDefault(c)

    while Has_response:
        cmd = raw_input("Enter command or 'exit': \b")
        # for Python 2
        # cmd = input("Enter command or 'exit':")
        # for Python 3
        if cmd == 'exit':
            _exit()
        elif cmd == '':
            getImage(cmd)
        else:
            sendComm(cmd)

    _exit()
