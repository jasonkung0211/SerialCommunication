#!/usr/bin/python

import datetime
import serial
import sys
import getopt
import os




# def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
#     img_stream.seek(0)
#     img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
#     return cv2.imdecode(img_array, cv2_img_flag)

# def create_opencv_image_from_url(url, cv2_img_flag=0):
#     request = urlopen(url)
#     img_array = np.asarray(bytearray(request.read()), dtype=np.uint8)
#     return cv2.imdecode(img_array, cv2_img_flag)



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

    ser = serial.Serial(port, baud, timeout=0)
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
                    print out
                    continue

                if tmp.find('<<EOF>>') != -1:
                    out += tmp[:tmp.find('<<EOF>>')]
                    break

                if startindex != -1:
                    out += tmp
            filename = datetime.datetime.now().strftime("%m-%d_%H-%M-%S")+".jpg"
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

if __name__ == "__main__":
    main(sys.argv[1:])
