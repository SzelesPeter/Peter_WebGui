#Imports for Serial communication to work:
import serial
from serial.tools.list_ports import comports

Windows = False


        
class RS232:
    def __init__(self, Port: str="ttyS1", Baud: str="9600", Flow: str="NONE", Parity: str="NONE", Timeout: float=1):

        self.ser = serial.Serial()
        self.Port = Port
        self.Baud = Baud #["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        self.Flow = Flow #["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        self.Parity = Parity #["NONE", "ODD", "EVEN"]
        self.Timeout = Timeout

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
        self.ser.timeout = self.Timeout

    def Open(self):
        Error = None
        if(self.ser.is_open):
            Error = "Serial port is already open"
        else:
            if Windows:
                self.ser.port = self.Port
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
            if Text[-1] == '\n':
                Text = Text[0:-1]
            if Text[-1] == '\r':
                Text = Text[0:-1]
            return Text
        else:
            return ""

    def Find_IDE(self, maker, name, no):
        self.Close()
        Com_ports = self.Get_Possible_Ports()
        timeout = self.Get_Timeout()
        self.Set_Timeout(1)
        for port in Com_ports:
            self.Set_Port(port)
            if self.Open() == None:
                self.Write_Line('*IDN?')
                instrument_IDE = self.Read_Line()
                if instrument_IDE != '':
                    instrument_IDE = instrument_IDE.split(',')
                    if len(instrument_IDE) == 4:
                        if no != None:
                            if (maker == instrument_IDE[0]) and (name == instrument_IDE[1]) and (str(no) == instrument_IDE[2]):
                                self.Set_Timeout(timeout)
                                self.Close()
                                return port, instrument_IDE
                        else:
                            if (maker == instrument_IDE[0]) and (name == instrument_IDE[1]):
                                self.Set_Timeout(timeout)
                                self.Close()
                                return port, instrument_IDE
                self.Close()
        self.Set_Timeout(timeout)
        return None, None


from nicegui import ui
import WebGui_Visuals as WGV

class RS232_GUI:
    def __init__(self,name: str, RS232: RS232):
        self.RS232 = RS232
        with WGV.Card(name= name, width= 310, height= 450):
            with ui.row(): # column with no spaceing:
                self.L_Port = WGV.Create_Label_Right('Port:', font_size= 20, width= 80)
                self.DDC_Port = WGV.Create_Dropdown_Card(options=self.RS232.Get_Possible_Ports(), function_to_call=self.__DDC_Port_Function_internal, width= 160)
                self.DDC_Port.set_value(self.RS232.Get_Port())
            with ui.row():
                self.L_Baud = WGV.Create_Label_Right('Baud:', font_size= 20, width= 80)
                self.DDC_Baud = WGV.Create_Dropdown_Card(options=self.RS232.Get_Possible_Bauds(), function_to_call=self.__DDC_Baud_Function_internal, width= 160)
                self.DDC_Baud.set_value(self.RS232.Get_Baud())
            with ui.row():
                self.L_Parity = WGV.Create_Label_Right('Parity:', font_size= 20, width= 80)
                self.DDC_Parity = WGV.Create_Dropdown_Card(options=self.RS232.Get_Possible_Paritys(), function_to_call=self.__DDC_Parity_Function_internal, width= 160)
                self.DDC_Parity.set_value(self.RS232.Get_Parity())
            with ui.row():
                self.L_Flow = WGV.Create_Label_Right('Flow:', font_size= 20, width= 80)
                self.DDC_Flow = WGV.Create_Dropdown_Card(options=self.RS232.Get_Possible_Flows(), function_to_call=self.__DDC_Flow_Function_internal, width= 160)
                self.DDC_Flow.set_value(self.RS232.Get_Flow())
            with ui.row():
                self.L_Timeout = WGV.Create_Label_Right('Timeout:', font_size= 20, width= 80)
                self.NI_Timeout = WGV.Number_input(number_function = self.__NI_Timeout_Function_internal, text_width = 0, number_width = 100, default_value = self.RS232.Get_Timeout(), min = 0, max = 9999)
            with ui.row():
                self.B_Connect = WGV.Button(lambda: self.B_Connect_Function(), name='Connect', width= 120,background_color = '#B12C2C')
                self.B_Disconnect = WGV.Button(lambda: self.B_Disconnect_Function(), name='Disconnect', width= 120)
            with ui.row():
                self.L_Connected = WGV.Create_Label_Left('Not Connected', font_size= 20, width = 200)
                
    def Update_DDC_Port_list(self):
        self.DDC_Port.set_options(self.RS232.Get_Possible_Ports())

    def __DDC_Port_Function_internal(self, port: str):
        self.RS232.Set_Port(port)
        self.Update_DDC_Port_list()

    def __DDC_Baud_Function_internal(self, baud: str):
        self.RS232.Set_Baud(baud)

    def __DDC_Parity_Function_internal(self, parity: str):
        self.RS232.Set_Parity(parity)

    def __DDC_Flow_Function_internal(self, flow: str):
        self.RS232.Set_Flow(flow)

    def __NI_Timeout_Function_internal(self, timeout: float):
        self.RS232.Set_Timeout(timeout)

    def DDC_Port_Function(self, port: str):
        self.RS232.Set_Port(port)
        self.Update_DDC_Port_list()
        self.DDC_Port.set_value(port)

    def DDC_Baud_Function(self, baud: str):
        self.RS232.Set_Baud(baud)
        self.DDC_Baud.set_value(baud)

    def DDC_Parity_Function(self, parity: str):
        self.RS232.Set_Parity(parity)
        self.DDC_Parity.set_value(parity)

    def DDC_Flow_Function(self, flow: str):
        self.RS232.Set_Flow(flow)
        self.DDC_Flow.set_value(flow)

    def NI_Timeout_Function(self, timeout: float):
        self.RS232.Set_Timeout(timeout)
        self.NI_Timeout.Number_input_element.set_value(timeout)

    def B_Connect_Function(self):
        if self.RS232.Open() == None:
            self.L_Connected.set_text('Connected')

    def B_Disconnect_Function(self):
        if self.RS232.Close() == None:
            self.L_Connected.set_text('Not Connected')