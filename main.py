#!/usr/bin/python


#### -m PyInstaller --onefile

import time
import serial
import sys
import os
import ConfigParser
###from PIL import Image


# version, light, Shutter, Gain, image, quit

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


if __name__ == "__main__":

    firstConn = True
    Config = ConfigParser.ConfigParser()
    Config.read(os.getcwd() + '/config.ini')

    baud = ConfigSectionMap("Default")['baud']
    port = ConfigSectionMap("Default")['port']
    light = ConfigSectionMap("Default")['light']
    Shutter = ConfigSectionMap("Default")['shutter']
    Gain = ConfigSectionMap("Default")['gain']

    isRs232 = baud <= 115200

    print("baud rate: " + str(baud))
    print("port: " + port)

    ser = serial.Serial(port, baud, timeout=1)
    if ser.isOpen():
        print(ser.name + ' is open...')

    while True:
        if firstConn == False:
            cmd = raw_input("Enter command or 'exit': \b")
            if cmd == '':
                cmd = 'image85'
        else:
            cmd = 'Hello'
        # for Python 2
        # cmd = input("Enter command or 'exit':")
        # for Python 3
        if cmd == 'exit':
            ser.close()
            exit(0)
        elif cmd.startswith('image'):
            ser.write(cmd.encode('ascii') + '\r\n')
            out = ""
            startindex = -1
            while True:
                if not isRs232:
                    tmp = ser.read(8192)
                else:
                    tmp = ser.read(4096)
                if len(tmp) == 0:
                    continue

                if tmp.find('<<start>>') != -1:
                    startindex = out.find('<<start>>') + 18
                    out = tmp[startindex:]
                    continue

                if tmp.find('<<EOF>>') != -1:
                    out += tmp[:tmp.find('<<EOF>>')]
                    print 'OK'
                    break

                if startindex != -1:
                    out += tmp
                    print len(out)

            filename = "Capture.jpg"
            nf = open(filename, "wb+")
            nf.write(bytearray(out))
            nf.flush()
            nf.close()
            os.startfile(filename)
        else:
            ser.write(cmd.encode('ascii') + '\r\n')
            timeout = 6
            while True:
                out = ser.readline()
                if len(out) == 0 and timeout > 0:
                    timeout -= 1
                    continue
                break
            if timeout == 0:
                print 'Devices No response.'
                firstConn = True
            elif len(out) > 0:
                print out
                if firstConn:
                    cmd = 'Shutter' + Shutter
                    ser.write(cmd.encode('ascii') + '\r\n')
                    time.sleep(0.3)
                    out = ser.read_all()
                    print out
                    cmd = 'Gain' + Gain
                    ser.write(cmd.encode('ascii') + '\r\n')
                    time.sleep(0.3)
                    out = ser.read_all()
                    print out
                    cmd = 'light' + light
                    ser.write(cmd.encode('ascii') + '\r\n')
                    time.sleep(0.3)
                    out = ser.read_all()
                    print out
                    firstConn = False
            sys.stdout.flush()

    print("exit......")
    ser.close()
    exit()
