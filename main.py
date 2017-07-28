#!/usr/bin/python

import datetime
import serial
import sys, getopt
import os
import ConfigParser


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

    baud = ''
    port = 'COM'
    firstConn = True
    Config = ConfigParser.ConfigParser()
    Config.read(os.getcwd() + '/config.ini')
    options = Config.options("USB")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:u:", ["port=", "port="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-r", "--port"):
            baud = ConfigSectionMap("RS232")['baud']
            port = ConfigSectionMap("RS232")['port']
            options = Config.options("RS232")
        elif opt in ("-u", "--port"):
            baud = ConfigSectionMap("USB")['baud']
            port = ConfigSectionMap("USB")['port']
            options = Config.options("USB")

    print("baud rate: " + str(baud))
    print("port: " + port)

    # -----



    ser = serial.Serial(port, baud, timeout=1)
    if ser.isOpen():
        print(ser.name + ' is open...')

    while True:
        if firstConn == False:
            cmd = raw_input("Enter command or 'exit': \b")
        else:
            cmd = 'Hello'
        # for Python 2
        # cmd = input("Enter command or 'exit':")
        # for Python 3
        if cmd == 'exit':
            ser.close()
            exit()
        elif cmd == 'image':
            ser.write(cmd.encode('ascii') + '\r\n')
            out = ""
            startindex = -1
            while True:
                tmp = ser.readline()
                if len(tmp) == 0:
                    continue

                if tmp.find('<<start>>') != -1:
                    startindex = out.find('<<start>>') + 18
                    out = tmp[startindex:]
                    continue

                if tmp.find('<<EOF>>') != -1:
                    out += tmp[:tmp.find('<<EOF>>')]
                    break

                if startindex != -1:
                    print len(out)
                    out += tmp
            filename = datetime.datetime.now().strftime("%m-%d_%H-%M-%S") + ".jpg"
            # filename = "pic.jpg"
            nf = open(filename, "wb")
            nf.write(bytearray(out))
            nf.flush()
            nf.close()
            os.startfile(filename)
        else:
            ser.write(cmd.encode('ascii') + '\r\n')
            out = ser.readline()
            print(out)
            firstConn = False
            sys.stdout.flush()

    print("exit......")
    ser.close()
    exit()
