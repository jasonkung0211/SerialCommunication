#!/usr/bin/python

import time
import serial
import sys
import getopt
from matplotlib import pyplot as plt
import numpy as np
import binascii


def help():
    print("Start command=================")
    print 'For RS232 >> main.py -r <port number>'
    print 'For VCOM >> main.py -u <port number>'
    print("Control command=================")
    print("quit")
    print("image")

def main(argv):
    firstConn = True
    try:
        opts, args = getopt.getopt(argv, "hru:", ["port="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-r", "--port"):
            # RS232
            port = "COM" + arg
            baud = 115200
        elif opt in ("-u", "--port"):
            # Virtual COM port
            port = "COM" + arg
            baud = 921600

    print("baud rate: " + str(baud))
    print("port: " + port)

    ser = serial.Serial(port, baud, timeout=1)
    if ser.isOpen():
        print(ser.name + ' is open...')

    # Z5212
    image = np.empty((1280, 720), np.ubyte)

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
        else:
            ser.write(cmd.encode('ascii') + '\r\n')
            out = ""
            while True:
                temp = ser.readline()
                if len(temp) == 0: ## or temp == '<EOF>':
                    break
                out += temp
            if cmd == 'image':
                print(len(out))
                # print binascii.hexlify(out)
                # image.data[:] = out
                # plt.imshow(image)
                # plt.show()
            else:
                #if(out == '>>>update>>>version>>>light>>>Shutter>>>Gain>>>image>>>quit'):
                firstConn = False
                print(out)
                sys.stdout.flush()

    print("exit......")
    ser.close()
    exit()

if __name__ == "__main__":
    main(sys.argv[1:])
