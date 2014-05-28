import binascii
import socket
import struct
import sys
import time
import serial


SetPoint = 50
lpTm = 1
errSum = errLast = seqNum = err = effort = Pos = OldPos = velIn = 0
#serial connection with Arduino
ser = serial.Serial('/dev/tty.usbmodem641', 9600)
# Create a TCP/IP socket
TCP_IP = '127.0.0.1' #'cpid.io'
TCP_PORT = 5005

###############################
############CPID###############
###############################
print('Setup Complete')


while True:
    start_time = time.time()
    #write effort to Arduino
    #hacky error catching and negative number byte send
    negflag = 1
    if (effort<0):
        negflag = 2
    if(abs(effort)>255):
        effort = 255
    ser.write(chr(negflag))
    ser.write(chr(abs(effort)))
    ser.flushOutput()
    #read in position from Arduino
    if ser.inWaiting()>2:
        print('Reading New Position')
        neg = ser.read()
        Pos = ser.read()
        Pos = ord(Pos)+ord(ser.read())*256
        if ord(neg) == 1: Pos = -Pos
        ser.flushInput()
        print 'Position: ' + str(Pos)
        velIn = (OldPos - Pos)/(10*lpTm)
        print 'Velocity: ' + str(velIn)
        OldPos = Pos

    err = SetPoint - velIn
    print 'Setpoint: ' + str(SetPoint)
    print 'Error: ' + str(err)
    #read in position from Arduino here
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    #pack error, time code, sequence number into a struct to simplify send
    values = (err, errSum, errLast, lpTm, seqNum)
    packer = struct.Struct('5f')
    packed_data = packer.pack(*values)
    unpacker = struct.Struct('1f')


    try:
        #send data
        print >>sys.stderr, 'sending...'
        sock.send(packed_data)
        #recieve data
        data = sock.recv(unpacker.size);
        effort = unpacker.unpack(data)
        effort = int(effort[0])
        print 'Control Effort: ' + str(effort)
        
    except:
        print >>sys.stderr, 'closing socket'
        sock.close()
    seqNum += 1
    print 'Sequence Number: ' + str(seqNum)
    errLast = err
    lpTm = time.time() - start_time
    errSum += (err*lpTm)
    print 'Loop Time: ' + str(lpTm), "seconds"
