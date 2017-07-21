#!/usr/bin/python

import time
import serial
import sys, getopt

def help():
    print("Start command=================")
    print 'For RS232 >> main.py -r <port number>'
    print 'For VCOM >> main.py -u <port number>'
    print("Control command=================")
    print("quit")
    print("image")

def main(argv):
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
            ##RS232
            port = "COM" + arg
            baud = 115200
        elif opt in ("-u", "--port"):
            ##Virtual COM port
            port = "COM" + arg
            baud = 921600

    print("baud rate: " + str(baud))
    print("port: " + port)

    ser = serial.Serial(port, baud, timeout=1)
    if ser.isOpen():
        print(ser.name + ' is open...')

    while True:
        cmd = raw_input("Enter command or 'exit':")
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
                if(len(temp)==0):
                    break;
                out += temp
            print(out)

    print("exit......");

if __name__ == "__main__":
   main(sys.argv[1:])