import serial
text = "1234"
ser = serial.Serial()
ser.port = '/dev/' + 'ttyUSB2'
ser.open()
ser.write(text.encode("utf-8"))