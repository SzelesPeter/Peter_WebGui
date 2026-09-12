#Imports for Serial communication to work:
import serial
from serial.tools.list_ports import comports




        
class RS232:
    def __init__(self):

        self.ser = serial.Serial()
        self.Port = "ttyS1"
        self.Baud = "9600" #["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        self.Flow = "NONE" #["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        self.Parity = "NONE" #["NONE", "ODD", "EVEN"]
        self.Timeout = 0.01

    def Get_Port(self):
        return self.Port
    def Set_Port(self, Port):
        self.Port = Port
    def Get_Possible_Ports(self):
        Possible_Ports = []
        for p in (comports()):
            Possible_Ports.append(p.name)
        return(Possible_Ports)

    def Get_Baud(self):
        return self.Baud
    def Set_Baud(self, Baud):
        self.Baud = Baud
    def Get_Possible_Bauds(self):
        Possible_Bauds = ["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        return Possible_Bauds

    def Get_Flow(self):
        return self.Flow
    def Set_Flow(self, Flow):
        self.Flow = Flow
    def Get_Possible_Flows(self):
        Possible_Flows = ["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        return Possible_Flows

    def Get_Parity(self):
        return self.Parity
    def Set_Parity(self, Parity):
        self.Parity = Parity
    def Get_Possible_Paritys(self):
        Possible_Paritys = ["NONE", "ODD", "EVEN"]
        return Possible_Paritys

    def Get_Timeout(self):
        return self.Timeout
    def Set_Timeout(self, Timeout):
        self.Timeout = Timeout

    def Open(self):
        Error = None
        if(self.ser.is_open):
            Error = "Serial port is already open"
        else:
            self.ser.port = '/dev/' + self.Port
            self.ser.baudrate = self.Baud
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.dsrdtr = False
            self.ser.rtscts = False
            self.ser.xonxoff = False
            if(self.Flow == "Dsr/Dtr"):
                self.ser.dsrdtr = True
            elif(self.Flow == "Rts/Cts"):
                self.ser.rtscts = True
            elif(self.Flow == "Xon/Xoff"):
                self.ser.xonxoff = True
            if(self.Parity == "NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(self.Parity == "ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(self.Parity == "EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = self.Timeout
            try:
                self.ser.open()
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant be opened!"
            print(self.ser.is_open)
            print(self.ser.port)
        return Error

    def Close(self):
        Error = None
        if(self.ser.is_open):
            self.ser.close()
        else:
            Error = "Port: " + '/dev/' + self.Port + " Cant be closed, was already closed."
        return Error

    def Write(self, text):
        Error = None
        if(self.ser.is_open):
            try:
                self.ser.write(text.encode("utf-8"))
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant transmit!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant transmit, because port is not open!"
        return Error

    def Write_Line(self, text):
        Error = None
        if(self.ser.is_open):
            try:
                self.ser.write((text + "\r\n").encode("utf-8"))
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant transmit!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant transmit, because port is not open!"
        return Error

    def Read(self):
        Error = None
        Text = ""
        if(self.ser.is_open):
            try: 
                Text = self.ser.read().decode("utf-8")
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant recive, because port is not open!"
        return Error, Text

    def Read_Line(self):
        Error = None
        Text = ""
        if(self.ser.is_open):
            try: 
                Text = self.ser.readline().decode("utf-8")
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant recive, because port is not open!"
        if Text != "":
            return Text[0:-1]
        else:
            return ""