
"""
import serial

class RS232:
    def __init__(self):
        self.ser = serial.Serial()
        
    def open(self):
        self.ser.baudrate = "115200"
        self.ser.port = '/dev/ttyS0'
        self.ser.timeout = 1
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.dsrdtr = False
        self.ser.rtscts = False
        self.ser.xonxoff = False
        self.ser.open()     

    def RS232_close(self):
        if(self.ser.is_open):
            self.ser.close()
            self.debug.add_event("Port: " + self.COM_Port_combo_box.get() + " closed.")
        if(self.ser.is_open):
            self.RS232_status_label.configure(text = "Open")
        else:
            self.RS232_status_label.configure(text = "Closed")
        self.update_COM_Port_list()
    
    def Command(self, command):
        #write data
        if(self.ser.is_open):

            self.ser.write((command +"\r\n").encode("utf-8"))



    def Query(self, command):
        self.Command(command)
        #read data

        text = self.ser.readline()

        text = text[:-2]

        return text
 """
# ====================================================== START ======================================================================

import time

class  Instrument_Identification_String:
    def __init__(self, Interface):
        self.Interface = Interface

        self.Manufacturer = ""
        self.Name = ""
        self.Serial_Number = ""
        self.Softvatre_Version = ""
    
    def Read(self):
        text = self.Interface.Query("*IDN?").split(',')
        try:
            self.Manufacturer = text[0] 
            self.Name = text[1] 
            self.Serial_Number = text[2] 
            self.Softvatre_Version = text[3]
        except:
            self.Manufacturer = ""
            self.Name = "" 
            self.Serial_Number = ""
            self.Softvatre_Version = ""
# ============================================================ v Status System v ======================================================

class  Status_Byte_Condition_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Alarm_Condition = '0'    # One or more bits are set in the Alarm Register (bits must be enabled).
        self.Questionable_Data = '0'  # One or more bits are set in the Questionable Data Register (bits must be enabled).
        self.Message_Available = '0'  # Data is available in the instrument’s output buffer.
        self.Standard_Event = '0'     # One or more bits are set in the Standard Event Register (bits must be enabled).
        self.Master_Summary = '0'     # One or more bits are set in the Status Byte Register (bits must be enabled).
        self.Standard_Operation = '0' # One or more bits are set in the Standard Operation Register (bits must be enabled).
    
    def Read(self):
        tmp = format(int(self.Interface.Query("*STB?")), 'b')
        self.Alarm_Condition = tmp[1]
        self.Questionable_Data = tmp[3]
        self.Message_Available = tmp[4]
        self.Standard_Event = tmp[5]
        self.Master_Summary = tmp[6]
        self.Standard_Operation = tmp[7]


class  Status_Byte_Enable_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Alarm_Condition = '0'    # One or more bits are set in the Alarm Register (bits must be enabled).
        self.Questionable_Data = '0'  # One or more bits are set in the Questionable Data Register (bits must be enabled).
        self.Message_Available = '0'  # Data is available in the instrument’s output buffer.
        self.Standard_Event = '0'     # One or more bits are set in the Standard Event Register (bits must be enabled).
        self.Standard_Operation = '0' # One or more bits are set in the Standard Operation Register (bits must be enabled).
    
    def Read(self):
        tmp = format(int(self.Interface.Query("*SRE?")), 'b')
        self.Alarm_Condition = tmp[1]
        self.Questionable_Data = tmp[3]
        self.Message_Available = tmp[4]
        self.Standard_Event = tmp[5]
        self.Standard_Operation = tmp[7]

    def Write(self):
        tmp = []
        tmp.append('0')
        tmp.append(self.Alarm_Condition)
        tmp.append('0')
        tmp.append(self.Questionable_Data)
        tmp.append(self.Message_Available)
        tmp.append(self.Standard_Event)
        tmp.append(self.Master_Summary)
        tmp.append(self.Standard_Operation)
        self.Interface.Command("*SRE " + str(int(tmp, 2)))

class  Questionable_Data_Condition_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Totalizer_Overflow = '0'       # Count overflow on a totalizer channel.
        self.Memory_Overflow = '0'          # Memory is full; 1 or more readings are lost.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:QUES:COND?")), 'b')
        self.Totalizer_Overflow = tmp[11]
        self.Memory_Overflow = tmp[12]

class  Questionable_Data_Event_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Voltage_Overload = '0'         # Range overload on dc or ac volts.
        self.Current_Overload = '0'         # Range overload on dc or ac current.
        self.Resistance_Overload = '0'      # Range overload on 2- or 4-wire resistance.
        self.Temperature_Overload = '0'     # Range overload on temperature.
        self.Totalizer_Overflow = '0'       # Count overflow on a totalizer channel.
        self.Memory_Overflow = '0'          # Memory is full; 1 or more readings are lost.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:QUES:EVENt?")), 'b')
        self.Voltage_Overload = tmp[0]
        self.Current_Overload = tmp[1]
        self.Resistance_Overload = tmp[9]
        self.Temperature_Overload = tmp[10]
        self.Totalizer_Overflow = tmp[11]
        self.Memory_Overflow = tmp[12]

class  Questionable_Data_Enable_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Voltage_Overload = '0'         # Range overload on dc or ac volts.
        self.Current_Overload = '0'         # Range overload on dc or ac current.
        self.Resistance_Overload = '0'      # Range overload on 2- or 4-wire resistance.
        self.Temperature_Overload = '0'     # Range overload on temperature.
        self.Totalizer_Overflow = '0'       # Count overflow on a totalizer channel.
        self.Memory_Overflow = '0'          # Memory is full; 1 or more readings are lost.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:QUES:ENABle?")), 'b')
        self.Voltage_Overload = tmp[0]
        self.Current_Overload = tmp[1]
        self.Resistance_Overload = tmp[9]
        self.Temperature_Overload = tmp[10]
        self.Totalizer_Overflow = tmp[11]
        self.Memory_Overflow = tmp[12]

    def Write(self):
        tmp = []
        tmp.append(self.Voltage_Overload)
        tmp.append(self.Current_Overload)
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append(self.Resistance_Overload)
        tmp.append(self.Temperature_Overload)
        tmp.append(self.Totalizer_Overflow)
        tmp.append(self.Memory_Overflow)
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        self.Interface.Command("STAT:QUES:ENABle " + str(int(tmp, 2)))

class  Standard_Event_Event_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Operation_Complete = '0'       # All commands prior to and including *OPC have been executed.
        self.Query_Error = '0'              # The instrument tried to read the output buffer but it was empty. Or, a new command line was received before a previous query has been read. Or, both the input and output buffers are full.
        self.Device_Error = '0'             # A self-test or calibration error occurred (see error numbers in the -300 range or any positive error number in chapter 6).
        self.Execution_Error = '0'          # An execution error occurred (see error numbers in the -200 range in chapter 6).
        self.Command_Error = '0'            # A command syntax error occurred (see error numbers in the -100 range in chapter 6).
        self.Power_On = '0'                 # Power has been turned off and on since the last time the event register was read or cleared.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("*ESR?")), 'b')
        self.Operation_Complete = tmp[0]       # All commands prior to and including *OPC have been executed.
        self.Query_Error = tmp[2]              # The instrument tried to read the output buffer but it was empty. Or, a new command line was received before a previous query has been read. Or, both the input and output buffers are full.
        self.Device_Error = tmp[3]             # A self-test or calibration error occurred (see error numbers in the -300 range or any positive error number in chapter 6).
        self.Execution_Error = tmp[4]          # An execution error occurred (see error numbers in the -200 range in chapter 6).
        self.Command_Error = tmp[5]            # A command syntax error occurred (see error numbers in the -100 range in chapter 6).
        self.Power_On = tmp[7]                 # Power has been turned off and on since the last time the event register was read or cleared.

class  Standard_Event_Enable_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Operation_Complete = '0'       # All commands prior to and including *OPC have been executed.
        self.Query_Error = '0'              # The instrument tried to read the output buffer but it was empty. Or, a new command line was received before a previous query has been read. Or, both the input and output buffers are full.
        self.Device_Error = '0'             # A self-test or calibration error occurred (see error numbers in the -300 range or any positive error number in chapter 6).
        self.Execution_Error = '0'          # An execution error occurred (see error numbers in the -200 range in chapter 6).
        self.Command_Error = '0'            # A command syntax error occurred (see error numbers in the -100 range in chapter 6).
        self.Power_On = '0'                 # Power has been turned off and on since the last time the event register was read or cleared.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("*ESE?")), 'b')
        self.Operation_Complete = tmp[0]       # All commands prior to and including *OPC have been executed.
        self.Query_Error = tmp[2]              # The instrument tried to read the output buffer but it was empty. Or, a new command line was received before a previous query has been read. Or, both the input and output buffers are full.
        self.Device_Error = tmp[3]             # A self-test or calibration error occurred (see error numbers in the -300 range or any positive error number in chapter 6).
        self.Execution_Error = tmp[4]          # An execution error occurred (see error numbers in the -200 range in chapter 6).
        self.Command_Error = tmp[5]            # A command syntax error occurred (see error numbers in the -100 range in chapter 6).
        self.Power_On = tmp[7]                 # Power has been turned off and on since the last time the event register was read or cleared.

    def Write(self):
        tmp = []
        tmp.append(self.Operation_Complete)
        tmp.append('0')
        tmp.append(self.Query_Error)
        tmp.append('0')
        tmp.append(self.Device_Error)
        tmp.append(self.Execution_Error)
        tmp.append(self.Command_Error)
        tmp.append(self.Power_On)
        self.Interface.Command("*ESE " + str(int(tmp, 2)))

class  Alarm_Condition_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Queue_Empty = '0'       # Alarm queue status (0 = empty, 1 = not empty).

    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:ALARm:COND?")), 'b')
        self.Queue_Empty = tmp[4]

class  Alarm_Event_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Alarm_1 = '0'              # Alarm occurred on Alarm 1.
        self.Alarm_2 = '0'              # Alarm occurred on Alarm 2.
        self.Alarm_3 = '0'              # Alarm occurred on Alarm 3.
        self.Alarm_4 = '0'              # Alarm occurred on Alarm 4.
        self.Totalizer_Overflow = '0'   # Alarm queue status (0 = empty, 1 = not empty).
        self.Queue_Overflow = '0'       # Alarm data lost due to alarm queue overflow.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:ALARm:EVENt?")), 'b')
        self.Alarm_1 = tmp[0]               # Alarm occurred on Alarm 1.
        self.Alarm_2 = tmp[1]               # Alarm occurred on Alarm 2.
        self.Alarm_3 = tmp[2]               # Alarm occurred on Alarm 3.
        self.Alarm_4 = tmp[3]               # Alarm occurred on Alarm 4.
        self.Totalizer_Overflow = tmp[4]    # Alarm queue status (0 = empty, 1 = not empty).
        self.Queue_Overflow = tmp[5]        # Alarm data lost due to alarm queue overflow.

class  Alarm_Enable_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Alarm_1 = '0'              # Alarm occurred on Alarm 1.
        self.Alarm_2 = '0'              # Alarm occurred on Alarm 2.
        self.Alarm_3 = '0'              # Alarm occurred on Alarm 3.
        self.Alarm_4 = '0'              # Alarm occurred on Alarm 4.
        self.Totalizer_Overflow = '0'   # Alarm queue status (0 = empty, 1 = not empty).
        self.Queue_Overflow = '0'       # Alarm data lost due to alarm queue overflow.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:ALARm:ENABle?")), 'b')
        self.Alarm_1 = tmp[0]               # Alarm occurred on Alarm 1.
        self.Alarm_2 = tmp[1]               # Alarm occurred on Alarm 2.
        self.Alarm_3 = tmp[2]               # Alarm occurred on Alarm 3.
        self.Alarm_4 = tmp[3]               # Alarm occurred on Alarm 4.
        self.Totalizer_Overflow = tmp[4]    # Alarm queue status (0 = empty, 1 = not empty).
        self.Queue_Overflow = tmp[5]        # Alarm data lost due to alarm queue overflow.

    def Write(self):
        tmp = []
        tmp.append(self.Alarm_1)
        tmp.append(self.Alarm_2)
        tmp.append(self.Alarm_3)
        tmp.append(self.Alarm_4)
        tmp.append(self.Totalizer_Overflow)
        tmp.append(self.Queue_Overflow)
        tmp.append('0')
        tmp.append('0')

        self.Interface.Command("STAT:ALARm:ENABle " + str(int(tmp, 2)))

class  Standard_Operation_Condition_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Scan_in_Progress = '0'         # Instrument is scanning ( SCAN annunciator is on).
        self.Configuration_Change = '0'     # Channel configuration was changed from the front panel. This bit is cleared when a new scan is initiated.
        self.Memory_Threshold = '0'         # Programmed number of readings have been stored in reading memory.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:OPER:COND?")), 'b')
        self.Scan_in_Progress = tmp[4]
        self.Configuration_ChangeMemory_Overflow = tmp[8]
        self.Memory_Threshold = tmp[9]

class  Standard_Operation_Event_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Scan_in_Progress = '0'         # Instrument is scanning ( SCAN annunciator is on).
        self.Configuration_Change = '0'     # Channel configuration was changed from the front panel. This bit is cleared when a new scan is initiated.
        self.Memory_Threshold = '0'         # Programmed number of readings have been stored in reading memory.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:OPER:EVENt?")), 'b')
        self.Scan_in_Progress = tmp[4]
        self.Configuration_ChangeMemory_Overflow = tmp[8]
        self.Memory_Threshold = tmp[9]

class  Standard_Operation_Enable_Register:
    def __init__(self, Interface):
        self.Interface = Interface
        self.Scan_in_Progress = '0'         # Instrument is scanning ( SCAN annunciator is on).
        self.Configuration_Change = '0'     # Channel configuration was changed from the front panel. This bit is cleared when a new scan is initiated.
        self.Memory_Threshold = '0'         # Programmed number of readings have been stored in reading memory.
    
    def Read(self):
        tmp = format(int(self.Interface.Query("STAT:OPER:ENABle?")), 'b')
        self.Scan_in_Progress = tmp[4]
        self.Configuration_ChangeMemory_Overflow = tmp[8]
        self.Memory_Threshold = tmp[9]

    def Write(self):
        tmp = []
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append(self.Scan_in_Progress)
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append(self.Configuration_ChangeMemory_Overflow)
        tmp.append(self.Memory_Threshold)
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        tmp.append('0')
        self.Interface.Command("STAT:OPER:ENABle " + str(int(tmp, 2)))

class  Status_System:
    def __init__(self, Interface):
        self.Interface = Interface

        self.SCPI_Versoin = ""

        self.Status_Byte_Condition_Register = Status_Byte_Condition_Register(self.Interface)
        self.Status_Byte_Enable_Register = Status_Byte_Enable_Register(self.Interface)
        self.Status_Byte_Condition_ReQuestionable_Data_Condition_Registergister = Questionable_Data_Condition_Register(self.Interface)
        self.Questionable_Data_Event_Register = Questionable_Data_Event_Register(self.Interface)
        self.Questionable_Data_Enable_Register = Questionable_Data_Enable_Register(self.Interface)
        self.Error_Queue = []
        self.Standard_Event_Event_Register = Standard_Event_Event_Register(self.Interface)
        self.Standard_Event_Enable_Register = Standard_Event_Enable_Register(self.Interface)
        self.Alarm_Queue = []
        self.Alarm_Condition_Register = Alarm_Condition_Register(self.Interface)
        self.Alarm_Event_Register = Alarm_Event_Register(self.Interface)
        self.Alarm_Enable_Register = Alarm_Enable_Register(self.Interface)
        self.Data_Points_Treshold = 1
        self.Standard_Operation_Condition_Register = Standard_Operation_Condition_Register(self.Interface)
        self.Standard_Operation_Event_Register = Standard_Operation_Event_Register(self.Interface)
        self.Standard_Operation_Enable_Register = Standard_Operation_Enable_Register(self.Interface)

    def SCPI_Versoin_Read(self):
        self.SCPI_Versoin = self.Interface.Query("SYSTem:VERSion?")

    def Clear(self):
        self.Interface.Command("*CLS")

    def Power_on_Clear_Enable_Register(self):
        self.Interface.Command("*PSC 1")
    
    def Power_on_Dont_Clear_Enable_Register(self):
        self.Interface.Command("*PSC 0")

    def Preset(self):
        self.Interface.Command("STATus:PRESet")

    def Error_Read(self):
        self.Error_Queue.append(self.Interface.Query("SYSTem:ERRor?"))

    def Alarm_Read(self):
        self.Alarm_Queue.append(self.Interface.Query("SYSTem:ALARm?"))

    def Data_Points_Treshold_Read(self):
        self.Data_Points_Treshold = self.Interface.Query("DATA:POINts:EVENt:THReshold?")

    def Data_Points_Treshold_Write(self):
        self.Interface.Command("DATA:POINts:EVENt:THReshold " + str(self.Data_Points_Treshold))

    def Operation_Complete_set_at_Scan_completion(self):
        self.Interface.Command("*OPC")

# ============================================================ ^ Status System ^ ======================================================
# ============================================================ v Configure v ==========================================================

class  Configure:
    def __init__(self, Interface):
        self.Interface = Interface

    def Configure_Voltage_DC(self, range, resolution, channel):
        self.Interface.Command("CONFigure:VOLTage:DC " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Voltage_AC(self, range, resolution, channel):
        self.Interface.Command("CONFigure:VOLTage:AC " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Resistance_2(self, range, resolution, channel):
        self.Interface.Command("CONFigure:RESistance " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Resistance_4(self, range, resolution, channel):
        self.Interface.Command("CONFigure:FRESistance " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Current_DC(self, range, resolution, channel):
        self.Interface.Command("CONFigure:CURRent:DC " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Current_AC(self, range, resolution, channel):
        self.Interface.Command("CONFigure:CURRent:AC " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Frequency(self, range, resolution, channel):
        self.Interface.Command("CONFigure:FREQuency " + range + "," + resolution + ", (" + channel + ")")

    def Configure_Period(self, range, resolution, channel):
        self.Interface.Command("CONFigure:PERiod " + range + "," + resolution + ", (" + channel + ")")

# ============================================================ ^ Configure ^ ==========================================================
# ============================================================ v Monitoring v ==========================================================

class  Monitor:
    def __init__(self, Interface):
        self.Interface = Interface

    def Monitoring_Start(self, channel):
        self.Interface.Command("ROUTe:MONitor (" + channel + ")")
        time.sleep(0.1)
        self.Interface.Command("ROUTe:MONitor:STATe ON")

    def Monitoring_Stop(self):
        self.Interface.Command("ROUTe:MONitor:STATe OFF")

    def Monitoring_Read(self):
        return(self.Interface.Query("ROUTe:MONitor:DATA?"))

# ============================================================ ^ Monitor ^ ==========================================================
# ============================================================ v Range v ==========================================================
class  Range:
    def __init__(self):
        self.DC_Voltage = ["AUTO", "300", "100", "10", "1", "0.1"]
        self.Resistance = ["AUTO", "10E8", "10E7", "10E6", "10E5", "10E4", "1000", "100"]
        self.DC_Current = ["AUTO", "1", "0.1", "0.01"]
        self.AC_Voltage = ["AUTO", "300", "100", "10", "1", "0.1"]
        self.AC_Current = ["AUTO", "1", "0.1", "0.01"]
        
# ============================================================ ^ Range ^ ==========================================================
# ============================================================ v Scan v ==========================================================


# ============================================================ ^ Scan ^ ==========================================================

class Instrument:
    def __init__(self, Interface, Serial_Number = "", Softvatre_Version = ""):
        self.Interface = Interface

        self.Manufacturer = "HEWLETT-PACKARD"
        self.Name = "34970A"
        self.Serial_Number = Serial_Number
        self.Softvatre_Version = Softvatre_Version
        self.Self_Test_Resoult = ""
        
    
        self.Instrument_Identification_String = Instrument_Identification_String(self.Interface)
        self.Status_System = Status_System(self.Interface)
        self.Configure = Configure(self.Interface)
        self.Monitor = Monitor(self.Interface)
        self.Range = Range()

        # Status Byte Register
        self.Alarm_Condition = False    # One or more bits are set in the Alarm Register (bits must be enabled).
        self.Questionable_Data = False  # One or more bits are set in the Questionable Data Register (bits must be enabled).
        self.Message_Available = False  # Data is available in the instrument’s output buffer.
        self.Standard_Event = False     # One or more bits are set in the Standard Event Register (bits must be enabled).
        self.Master_Summary = False     # One or more bits are set in the Status Byte Register (bits must be enabled).
        self.Standard_Operation = False # One or more bits are set in the Standard Operation Register (bits must be enabled).



    def Perform_Sefl_Test(self):
        self.Self_Test_Resoult = self.Interface.Query("*TST?")

    def Preset(self):
        self.Interface.Command("SYSTem:PRESet")

    def Factory_Reset(self):
        self.Interface.Command("*RST")

    def Display_On(self):
        self.Interface.Command("DISPlay ON")

    def Display_Off(self):
        self.Interface.Command("DISPlay OFF")

    def Display_Text(self, tmp):
        self.Interface.Command("DISPlay:TEXT " + '"' + tmp + '"')

    def Display_Clear(self):
        self.Interface.Command("DISPlay:TEXT:CLEar")

    def Date_Write(self, yyyy, mm, dd):
        self.Interface.Command("SYSTem:DATE " + yyyy + "," + mm + "," + dd)

    def Date_Read(self):
        return(self.Interface.Query("SYSTem:DATE?"))
    
    def Time_Write(self, hh, mm, ssDOTsss):
        self.Interface.Command("SYSTem:TIME " + hh + "," + mm + "," + ssDOTsss)

    def Time_Read(self):
        return(self.Interface.Query("SYSTem:TIME?"))
    
    def Time_Format_Absolute(self):
        self.Interface.Command("FORMat:READing:TIME:TYPE ABSolute")

    def Time_Format_Relative(self):
        self.Interface.Command("FORMat:READing:TIME:TYPE RELative")


# =========================================================== END ====================================================================


"""
port_1 = RS232()
port_1.open()

instrument = Agilent_34970A(port_1)
instrument.Display_Clear()

"""