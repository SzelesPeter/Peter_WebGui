import serial
import time

import numpy as np
import _tkinter as Tk

from serial.tools.list_ports import comports

import sys
sys.path.append('/home/peter/Documents/Python/Projects/TestBeam/Graph/')

import Graph



xpoints = []
y1points = []
y2points = []
y3points = []
y4points = []
y5points = []
y6points = []

for p in (comports()):
    print(p.name)

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyS0'
ser.timeout = 10
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_TWO
ser.dsrdtr = True
ser.rtscts = False
ser.xonxoff = False
ser.open()
time.sleep(1)
command = b'*IDN?' + b'\r\n'
ser.write(command)     # write a string
time.sleep(1)
line = ser.readline(400)   # read a '\n' terminated line
print(line)


command = b'ROUTe:SCAN (@101:106)' + b'\r\n'
ser.write(command)     # write a string
command = b'TRIGger:SOURce IMMediate' + b'\r\n'
ser.write(command)     # write a string
command = b'TRIGger:COUNt 10' + b'\r\n'
ser.write(command)     # write a string
command = b'INITiate' + b'\r\n'
ser.write(command)     # write a string

time.sleep(5)

command = b'DATA:POINts?' + b'\r\n'
ser.write(command)     # write a string
line = ser.readline(400)   # read a '\n' terminated line
print(line)
lenght = int(line.decode("utf-8"))
for x in range(int(lenght/6)):
    command = b'DATA:REMove? 6' + b'\r\n'
    ser.write(command)     # write a string
    line = ser.readline(40000)   # read a '\n' terminated line
    #print(line)
    print(line)
    data0 = float(line.decode("utf-8").split(',')[0])
    data1 = float(line.decode("utf-8").split(',')[1])
    data2 = float(line.decode("utf-8").split(',')[2])
    data3 = float(line.decode("utf-8").split(',')[3])
    data4 = float(line.decode("utf-8").split(',')[4])
    data5 = float(line.decode("utf-8").split(',')[5])

    xpoints.append(x)
    y1points.append(data0)
    y2points.append(data1)
    y3points.append(data2)
    y4points.append(data3)
    y5points.append(data4)
    y6points.append(data5)

ser.close()

trace1 = [xpoints, y1points]
trace2 = [xpoints, y2points]
trace3 = [xpoints, y3points]
trace4 = [xpoints, y4points]
trace5 = [xpoints, y5points]
trace6 = [xpoints, y6points]

plot1 = [trace1, trace2, trace3, trace4, trace5, trace6]

Graph2 = Graph.Graph_horizontal("HP34970A")
Graph2.add_subplot("CH101", plot1, "Mérési pontok", "Feszültség [V]")
Graph2.show()



"""
import serial
import time


time.sleep(1)
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM7 '
ser.timeout = 1
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.dsrdtr = False
ser.rtscts = False
ser.xonxoff = False
ser.open()
command = "*IDN?\r\n"
ser.write(command.encode(encoding="ascii",errors="ignore"))     # write a string

#time.sleep(1)
s = ser.readline(100)       # read up to one hundred bytes
print(s)
"""