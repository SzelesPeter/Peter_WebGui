import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))
import Agilent_34970A


class SCPI_Message:
    def __init__(self, Instrument, Command):
        self.Instrument = Instrument
        self.Command = Command

    def __Send_Command(self, Text):
        self.Instrument.Interface.Message_out_request(message_out=Text, in_message_target_function = None)

    def __Send_Query(self, Text, Target_Function):
        self.Instrument.Interface.Message_out_request(message_out=Text, in_message_target_function = Target_Function)

    def Set(self):
        self.__Send_Command(self.Command + ' ON')

    def Reset(self):
        self.__Send_Command(self.Command + ' OFF')

    def Write(self, *variables):
        Message = self.Command
        for i, variable in enumerate(variables):
            if (0 == i):
                Message = Message + ' ' + variable
            else:
                Message = Message + ',' + variable
        self.__Send_Command(Message)

    def Read(self, Target_Function, *variables):
        Message = self.Command + '?'
        for i, variable in enumerate(variables):
            if (0 == i):
                Message = Message + ' ' + variable
            else:
                Message = Message + ',' + variable 
        self.__Send_Query(Message, Target_Function)
    """
    def Read_Bytes(self, *variables, Target_Function):
        Message = self.Command + '?'
        for i, variable in enumerate(variables):
            if (0 == i):
                Message = Message + ' ' + variable
            else:
                Message = Message + ',' + variable       
        self.__Send_Query(Message, Target_Function)

    def Read_Bits(self, *variables, Target_Function):
        Message = self.Command + '?'
        for i, variable in enumerate(variables):
            if (0 == i):
                Message = Message + ' ' + variable
            else:
                Message = Message + ',' + variable       
        return (format(int(self.__Send_Query(Message)), 'b').zfill(lenght))
    
    def Read_String(self, *variables):
        Message = self.Command + '?'
        for i, variable in enumerate(variables):
            if (0 == i):
                Message = Message + ' ' + variable
            else:
                Message = Message + ',' + variable       
        return (str(self.__Send_Query(Message), 'ascii'))
    
    def Read_Array(self, *variables):  
        return (self.Read_String(*variables).split(','))
    
    #  DONT WORK because of fake \n in text
    def Read_Block(self, *variables):  
        Message = (self.Read_String(*variables))
        digits = 0
        lenght = 0
        if('#' == Message[0]):
            if(('0' == Message[1]) & (b'\n' == Message[-1])):
                Message = Message[2:-2]
            if('0' < Message[1]):
                digits = int(str(Message[1]))
                lenght = int(str(Message[2:2+digits]))
        return (Message[2+digits:2+digits+lenght])
    
    def Read_Array_From_Block(self, *variables):  
        return (self.Read_Block(*variables).split(','))
    """
    

class Instrument:
    def __init__(self, Interface):
        self.Interface = Interface

        # Measurement Commands
        self.MEASure_TEMPerature = SCPI_Message(self, 'MEASure:TEMPerature') # {TCouple|RTD|FRTD|THERmistor|DEF},{<type>|DEF}[,1[,{<resolution >|MIN|MAX|DEF}]] ,(@<scan_list>)
        self.MEASure_VOLTage_DC = SCPI_Message(self, 'MEASure:VOLTage:DC') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_VOLTage_AC = SCPI_Message(self, 'MEASure:VOLTage:AC') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_RESistance = SCPI_Message(self, 'MEASure:RESistance') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_FRESistance = SCPI_Message(self, 'MEASure:FRESistance') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_CURRent_DC = SCPI_Message(self, 'MEASure:CURRent:DC') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_CURRent_AC = SCPI_Message(self, 'MEASure:CURRent:AC') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_FREQuency = SCPI_Message(self, 'MEASure:FREQuency') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_PERiod = SCPI_Message(self, 'MEASure:PERiod') # [{<range>|AUTO |MIN|MAX|DEF}[,<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
        self.MEASure_DIGital_BYTE = SCPI_Message(self, 'MEASure:DIGital:BYTE') # (@<scan_list>)
        self.MEASure_TOTalize = SCPI_Message(self, 'MEASure:TOTalize') # {READ|RRESet} ,(@<scan_list>)

        # Monitor Commands
        self.ROUTe_MONitor = SCPI_Message(self, 'ROUTe:MONitor') # (@<channel>)
        self.ROUTe_MONitor_STATe = SCPI_Message(self, 'ROUTe:MONitor:STATe') # {OFF |ON}
        self.ROUTe_MONitor_DATA = SCPI_Message(self, 'ROUTe:MONitor:DATA')

        # Scan Configuration Commands
        self.ROUTe_SCAN = SCPI_Message(self, 'ROUTe:SCAN') # (@<scan_list>)
        self.ROUTe_SCAN_SIZE = SCPI_Message(self, 'ROUTe:SCAN:SIZE')
        self.TRIGger_SOURce = SCPI_Message(self, 'TRIGger:SOURce') # {BUS|IMMediate|EXTernal|ALARm1|ALARm2|ALARm3|ALARm4|TIMer}
        self.TRIGger_TIMer = SCPI_Message(self, 'TRIGger:TIMer') # {<seconds>|MIN|MAX}
        self.TRIGger_COUNt = SCPI_Message(self, 'TRIGger:COUNt') # {<count>|MIN|MAX|INFinity}
        self.ROUTe_CHANnel_DELay = SCPI_Message(self, 'ROUTe:CHANnel:DELay') # <seconds>[,(@<ch_ list>)]
        self.ROUTe_CHANnel_DELay_AUTO = SCPI_Message(self, 'ROUTe:CHANnel:DELay:AUTO') # {OFF|ON}[,(@<ch_list >)]
        self.ROUTe_CHANnel_ADVance_SOURce = SCPI_Message(self, 'ROUTe:CHANnel:ADVance:SOURce') # {EXTernal|BUS|IMMediate}
        self.ROUTe_CHANnel_FWIRe = SCPI_Message(self, 'ROUTe:CHANnel:FWIRe') # {OFF|ON}[,(@<ch_list>)]
        self.INSTrument_DMM = SCPI_Message(self, 'INSTrument:DMM') # {OFF|ON}
        self.INSTrument_DMM_INSTalled = SCPI_Message(self, 'INSTrument:DMM:INSTalled') # {OFF|ON}
        self.FORMat_READing_ALARm = SCPI_Message(self, 'FORMat:READing:ALARm') # {OFF|ON}
        self.FORMat_READing_CHANnel = SCPI_Message(self, 'FORMat:READing:CHANnel') # {OFF|ON}
        self.FORMat_READing_TIME = SCPI_Message(self, 'FORMat:READing:TIME') # {OFF|ON}
        self.FORMat_READing_UNIT = SCPI_Message(self, 'FORMat:READing:UNIT') # {OFF|ON}
        self.FORMat_READing_TIME_TYPE = SCPI_Message(self, 'FORMat:READing:TIME:TYPE') # {ABSolute|RELative}
        self.ABORt = SCPI_Message(self, 'ABORt')
        self.TRG = SCPI_Message(self, '*TRG')
        self.INITiate = SCPI_Message(self, 'INITiate')
        self.REAd = SCPI_Message(self, 'READ')

        # Scan Statistics Commands
        self.CALCulate_AVERage_MINimum = SCPI_Message(self, 'CALCulate:AVERage:MINimum') # [(@<ch_list >)]
        self.CALCulate_AVERage_MINimum_TIME = SCPI_Message(self, 'CALCulate:AVERage:MINimum:TIME') # [(@<ch_list >)]
        self.CALCulate_AVERage_MAXimum = SCPI_Message(self, 'CALCulate:AVERage:MAXimum') # [(@<ch_list >)]
        self.CALCulate_AVERage_MAXimum_TIME = SCPI_Message(self, 'CALCulate:AVERage:MAXimum:TIME') # [(@<ch_list >)]
        self.CALCulate_AVERage_AVERage = SCPI_Message(self, 'CALCulate:AVERage:AVERage') # [(@<ch_list >)]
        self.CALCulate_AVERage_PTPeak = SCPI_Message(self, 'CALCulate:AVERage:PTPeak') # [(@<ch_list >)]
        self.CALCulate_AVERage_COUNt = SCPI_Message(self, 'CALCulate:AVERage:COUNt') # [(@<ch_list >)]
        self.CALCulate_AVERage_CLEar = SCPI_Message(self, 'CALCulate:AVERage:CLEar') # [(@<ch_list >)]
        self.DATA_LASt = SCPI_Message(self, 'DATA:LAST') # [<num_rdgs>,][(@<channel>)]

        # Scan Memory Commands
        self.DATA_POINts = SCPI_Message(self, 'DATA:POINts')
        self.DATA_LASt = SCPI_Message(self, 'DATA:LAST') # [<num_rdgs>,][(@<channel>)]
        self.DATA_REMove = SCPI_Message(self, 'DATA:REMove') # <num_rdgs >
        self.SYSTem_TIME_SCAN = SCPI_Message(self, 'SYSTem:TIME:SCAN')
        self.FETCh = SCPI_Message(self, 'FETCh')
        self.R = SCPI_Message(self, 'R') # [<max_count>]

        # Temperature Configuration Commands
        self.CONFigure_TEMPerature = SCPI_Message(self, 'CONFigure:TEMPerature') # {TCouple|RTD|FRTD|THERmistor|DEF},{<type>|DEF}[,1[,{<resolution >|MIN|MAX|DEF}]] ,(@<scan_list>)
        self.UNIT_TEMPerature = SCPI_Message(self, 'UNIT:TEMPerature') # {C|F|K}[,(@<ch_list >)]
        self.SENSe_TEMPerature_TRANsducer_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:TYPE') # {TCouple|RTD|FRTD|THERmistor|DEF}[,(@ <ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_TCouple_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:TCouple:TYPE') # {B|E|J|K|N|R|S|T}[,(@<ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_TCouple_CHECk = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:TCouple:TYPE') # {OFF |ON}[,(@<ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_TCouple_RJUNction_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:TCouple:RJUNction:TYPE') # {INTernal |EXTernal|FIXed}[,(@<ch_list >)]
        self.SENSe_TEMPerature_TRANsducer_TCouple_RJUNction = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:TCouple:RJUNction') # {<temperature>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_TEMPerature_RJUNction= SCPI_Message(self, 'SENSe:TEMPerature:RJUNction') # [(@<ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_RTD_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:RTD:TYPE') # {85|91}[,(@<ch_list >)]
        self.SENSe_TEMPerature_TRANsducer_RTD_RESistance = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:RTD:TYPE') # <reference>[,(@<ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_FRTD_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:FRTD:TYPE') # {85|91}[,(@<ch_list >)]
        self.SENSe_TEMPerature_TRANsducer_FRTD_RESistance = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:FRTD:TYPE') # <reference>[,(@<ch_list>)]
        self.SENSe_TEMPerature_TRANsducer_THERmistor_TYPE = SCPI_Message(self, 'SENSe:TEMPerature:TRANsducer:THERmistor:TYPE') # {2252|5000|10000}[,(@<ch_list>)]
        self.SENSe_TEMPerature_NPLC = SCPI_Message(self, 'SENSe:TEMPerature:NPLC') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,(@ <ch_list >)]

        # Voltage Configuration Commands
        self.CONFigure_VOLTage_DC = SCPI_Message(self, 'CONFigure:VOLTage:DC') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_VOLTage_DC_RANGe = SCPI_Message(self, 'SENSe:VOLTage:DC:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_VOLTage_DC_RANGe_AUTO = SCPI_Message(self, 'SENSe:VOLTage:DC:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_VOLTage_DC_RESolution = SCPI_Message(self, 'SENSe:VOLTage:DC:RESolution') # {<resolution>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_VOLTage_DC_APERture = SCPI_Message(self, 'SENSe:VOLTage:DC:APERture') # {<time>|MIN|MAX}[,(@ <ch_list>)]
        self.SENSe_VOLTage_DC_NPLC = SCPI_Message(self, 'SENSe:VOLTage:DC:APERture') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,( @ < ch_list>)]
        self.INPut_IMPedance_AUTO = SCPI_Message(self, 'INPut:IMPedance:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_ZERO_AUTO = SCPI_Message(self, 'INPut:IMPedance:AUTO') # {OFF|ONCE|ON}[,(@<ch_list>)]
        self.CONFigure_VOLTage_AC = SCPI_Message(self, 'CONFigure:VOLTage:AC') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_VOLTage_AC_RANGe = SCPI_Message(self, 'SENSe:VOLTage:AC:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_VOLTage_AC_RANGe_AUTO = SCPI_Message(self, 'SENSe:VOLTage:AC:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_VOLTage_AC_BANDwidth = SCPI_Message(self, 'SENSe:VOLTage:AC:BANDwidth') # {3|20|200|MIN|MAX}[,(@<ch_list>)]
        
        # Resistance Configuration Commands
        self.CONFigure_RESistance = SCPI_Message(self, 'CONFigure:RESistance') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_RESistance_RANGe = SCPI_Message(self, 'SENSe:RESistance:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_RESistance_RANGe_AUTO = SCPI_Message(self, 'SENSe:RESistance:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_RESistance_RESolution = SCPI_Message(self, 'SENSe:RESistance:RESolution') # {<resolution>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_RESistance_ent_DC_NPLC = SCPI_Message(self, 'SENSe:CURRent:DC:APERture') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,( @ < ch_list>)]
        self.CONFigure_CURRent_AC = SCPI_Message(self, 'CONFigure:CURRent:AC') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_CURReAPERture = SCPI_Message(self, 'SENSe:RESistance:APERture') # {<time>|MIN|MAX}[,(@ <ch_list>)]
        self.SENSe_RESistance_NPLC = SCPI_Message(self, 'SENSe:RESistance:APERture') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,( @ < ch_list>)]
        self.SENSe_RESistance_OCOMpensated = SCPI_Message(self, 'SENSe:RESistance:OCOMpensated') # {OFF|ON}[,(@<ch_list>)]
        self.CONFigure_FRESistance = SCPI_Message(self, 'CONFigure:FRESistance') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_FRESistance_RANGe = SCPI_Message(self, 'SENSe:FRESistance:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_FRESistance_RANGe_AUTO = SCPI_Message(self, 'SENSe:FRESistance:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_FRESistance_RESolution = SCPI_Message(self, 'SENSe:FRESistance:RESolution') # {<resolution>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_FRESistance_APERture = SCPI_Message(self, 'SENSe:FRESistance:APERture') # {<time>|MIN|MAX}[,(@ <ch_list>)]
        self.SENSe_FRESistance_NPLC = SCPI_Message(self, 'SENSe:FRESistance:APERture') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,( @ < ch_list>)]
        self.SENSe_FRESistance_OCOMpensated = SCPI_Message(self, 'SENSe:FRESistance:OCOMpensated') # {OFF|ON}[,(@<ch_list>)]

        # Current Configuration Commands
        self.CONFigure_CURRent_DC = SCPI_Message(self, 'CONFigure:CURRent:DC') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_CURRent_DC_RANGe = SCPI_Message(self, 'SENSe:CURRent:DC:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_CURRent_DC_RANGe_AUTO = SCPI_Message(self, 'SENSe:CURRent:DC:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_CURRent_DC_RESolution = SCPI_Message(self, 'SENSe:CURRent:DC:RESolution') # {<resolution>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_CURRent_DC_APERture = SCPI_Message(self, 'SENSe:CURRent:DC:APERture') # {<time>|MIN|MAX}[,(@ <ch_list>)]
        self.SENSe_CURRent_DC_NPLC = SCPI_Message(self, 'SENSe:CURRent:DC:APERture') # {0.02|0.2| 1 |2|10|20|100|200|MIN|MAX}[,( @ < ch_list>)]
        self.CONFigure_CURRent_AC = SCPI_Message(self, 'CONFigure:CURRent:AC') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_CURRent_AC_RANGe = SCPI_Message(self, 'SENSe:CURRent:AC:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_CURRent_AC_RANGe_AUTO = SCPI_Message(self, 'SENSe:CURRent:AC:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_CURRent_AC_BANDwidth = SCPI_Message(self, 'SENSe:CURRent:AC:BANDwidth') # {3|20|200|MIN|MAX}[,(@<ch_list>)]

        # Frequency and Period Configuration Commands
        self.CONFigure_FREQuency = SCPI_Message(self, 'CONFigure:FREQuency') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_FREQuency_RANGe = SCPI_Message(self, 'SENSe:FREQuency:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_FREQuency_RANGe_AUTO = SCPI_Message(self, 'SENSe:FREQuency:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_FREQuency_RESolution = SCPI_Message(self, 'SENSe:FREQuency:RESolution') # {<resolution>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_FREQuency_APERture = SCPI_Message(self, 'SENSe:FREQuency:APERture') # {0.01|0.1|1|MIN|MAX}[,(@ <ch_list>)]
        self.SENSe_FREQuency_RANGe_LOWer = SCPI_Message(self, 'SENSe:FREQuency:RANGe:LOWer') # {3|20|200|MIN|MAX}[,(@<ch_list>)]
        self.CONFigure_PERiod = SCPI_Message(self, 'CONFigure:PERiod') # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        self.SENSe_PERiod_VOLTage_RANGe = SCPI_Message(self, 'SENSe:PERiod:VOLTage:RANGe') # {<range>|MIN|MAX}[,(@<ch_list>)]
        self.SENSe_PERiod_RANGe_VOLTage_AUTO = SCPI_Message(self, 'SENSe:PERiod:VOLTage:RANGe:AUTO') # {OFF|ON}[,(@<ch_list>)]
        self.SENSe_PERiod_RESolution = SCPI_Message(self, 'SENSe:PERiod:RESolution') # {0.01|0.1|1|MIN|MAX}[,(@<ch_list>)]

        # Mx+B Scaling Commands
        self.CALCulate_SCALe_GAIN = SCPI_Message(self, 'CALCulate:SCALe:GAIN') # <gain>[,(@<ch_list>)]
        self.CALCulate_SCALe_OFFSet = SCPI_Message(self, 'CALCulate:SCALe:OFFSet') # <offset>[,(@<ch_list>)]
        self.CALCulate_SCALe_UNIT = SCPI_Message(self, 'CALCulate:SCALe:UNIT') # <quoted_string>[,(@ <ch_ list>)]
        self.CALCulate_SCALe_OFFSet_NULL = SCPI_Message(self, 'CALCulate:SCALe:OFFSet:NULL') # [(@<ch_list>)]
        self.CALCulate_SCALe_STATe = SCPI_Message(self, 'CALCulate:SCALe:STATe') # {OFF|ON}[,(@<ch_list >)]

        # Alarm Limit Commands
        self.OUTPut_ALARm1_SOURce = SCPI_Message(self, 'OUTPut:ALARm1:SOURce') # (@<ch_list>)
        self.OUTPut_ALARm2_SOURce = SCPI_Message(self, 'OUTPut:ALARm2:SOURce') # (@<ch_list>)
        self.OUTPut_ALARm3_SOURce = SCPI_Message(self, 'OUTPut:ALARm3:SOURce') # (@<ch_list>)
        self.OUTPut_ALARm4_SOURce = SCPI_Message(self, 'OUTPut:ALARm4:SOURce') # (@<ch_list>)
        self.CALCulate_LIMit_UPPer = SCPI_Message(self, 'CALCulate:LIMit:UPPer') # <hi_limit>[,(@<ch_ list>)]
        self.CALCulate_LIMit_UPPer_STATe = SCPI_Message(self, 'CALCulate:LIMit:UPPer:STATe') # {OFF|ON}[,(@<ch_list>)]
        self.CALCulate_LIMit_LOWer = SCPI_Message(self, 'CALCulate:LIMit:LOWer') # <hi_limit>[,(@<ch_ list>)]
        self.CALCulate_LIMit_LOWer_STATe = SCPI_Message(self, 'CALCulate:LIMit:LOWer:STATe') # {OFF|ON}[,(@<ch_list>)]
        self.SYSTem_ALARm = SCPI_Message(self, 'SYSTem:ALARm')
        self.OUTPut_ALARm_MODE = SCPI_Message(self, 'OUTPut:ALARm:MODE') # {LATCh|TRACk}
        self.OUTPut_ALARm_SLOPe = SCPI_Message(self, 'OUTPut:ALARm:SLOPe') # {NEGative|POSitive}
        self.OUTPut_ALARm1_CLEar = SCPI_Message(self, 'OUTPut:ALARm1:CLEar')
        self.OUTPut_ALARm2_CLEar = SCPI_Message(self, 'OUTPut:ALARm2:CLEar')
        self.OUTPut_ALARm3_CLEar = SCPI_Message(self, 'OUTPut:ALARm3:CLEar')
        self.OUTPut_ALARm4_CLEar = SCPI_Message(self, 'OUTPut:ALARm4:CLEar')
        self.OUTPut_ALARm_CLEar_ALL = SCPI_Message(self, 'OUTPut:ALARm:CLEar:ALL')
        self.STATus_ALARm_CLEar_ALL = SCPI_Message(self, 'STATus:ALARm:CONDition')
        self.STATus_ALARm_CLEar_ALL = SCPI_Message(self, 'STATus:ALARm:ENABle') # <enable_value >
        self.STATus_ALARm_CLEar_ALL = SCPI_Message(self, 'STATus:ALARm:EVENt')
        """ Ch 01       Ch 02       Ch 03       Ch 04       Ch 05
            DIO (LSB)   DIO (MSB)   Totalizer   DAC         DAC     """
        self.CALCulate_COMPare_TYPE = SCPI_Message(self, 'CALCulate:COMPare:TYPE') # {EQUal|NEQual}[,(@<ch_list>)]
        self.CALCulate_COMPare_DATA = SCPI_Message(self, 'CALCulate:COMPare:DATA') # <data>[,(@<ch_list>)]
        self.CALCulate_COMPare_MASK = SCPI_Message(self, 'CALCulate:COMPare:MASK') # <mask>[,(@<ch_list>)]
        self.CALCulate_COMPare_STATe = SCPI_Message(self, 'CALCulate:COMPare:STATe') # {OFF|ON}[,(@<ch_list>)]

        # Digital Input Commands
        self.CONFigure_DIGital_BYTE = SCPI_Message(self, 'CONFigure:DIGital:BYTE') # (@<scan_list>)
        self.SENSe_DIGital_DATA_BYTE = SCPI_Message(self, 'SENSe:DIGital:DATA_BYTE') # [(@<ch_list>)]
        self.SENSe_DIGital_DATA_WORD = SCPI_Message(self, 'SENSe:DIGital:DATA_WORD') # [(@<ch_list>)]
        self.CONFigure_TOTalize = SCPI_Message(self, 'CONFigure:TOTalize') # {READ|RRESet} ,(@<scan_list>)
        self.SENSe_TOTalize_TYPE = SCPI_Message(self, 'SENSe:TOTalize:TYPE') # {READ |RRESet}[,(@<ch_list>)]
        self.SENSe_TOTalize_SLOPe = SCPI_Message(self, 'SENSe:TOTalize:SLOPe') # {NEGative|POSitive }[,(@<ch_list>)]
        self.SENSe_TOTalize_CLEar_IMMediate = SCPI_Message(self, 'SENSe:TOTalize:CLEar:IMMediate') # [(@<ch_ list>)]
        self.SENSe_TOTalize_DATA = SCPI_Message(self, 'SENSe:TOTalize:DATA') # [(@ <ch_ list>)]

        # Digital Output Commands
        self.SOURce_DIGital_DATA_BYTE = SCPI_Message(self, 'SOURce:DIGital:DATA_BYTE') # <data> ,(@<ch_list>)
        self.SOURce_DIGital_DATA_WORD = SCPI_Message(self, 'SOURce:DIGital:DATA_WORD') # <data> ,(@<ch_list>)
        self.SOURce_DIGital_STATe = SCPI_Message(self, 'SOURce:DIGital:DATA_WORD') # (@<ch_list>)

        # DAC Output Commands
        self.SOURce_VOLTage = SCPI_Message(self, 'SOURce:VOLTage') # <voltage > ,(@<ch_list >)

        # Switch Control Commands
        self.ROUTe_CLOSe = SCPI_Message(self, 'ROUTe:CLOSe') # (@<ch_list>)
        self.ROUTe_CLOSe_EXCLusive = SCPI_Message(self, 'ROUTe:CLOSe:EXCLusive') # (@<ch_list>)
        self.ROUTe_OPEN = SCPI_Message(self, 'ROUTe:OPEN') # (@<ch_list>)
        self.ROUTe_CHANnel_FWIRe = SCPI_Message(self, 'ROUTe:CLOSe:EXCLusive') # {OFF|ON}[,(@<ch_list>)]
        self.ROUTe_DONE = SCPI_Message(self, 'ROUTe:DONE')
        self.SYSTem_CPON = SCPI_Message(self, 'SYSTem:CPON') # {100|200|300|ALL}

        # State Storage Commands
        self.SAV = SCPI_Message(self, '*SAV') # {0|1|2|3|4|5}
        self.RCL = SCPI_Message(self, '*RCL') # {0|1|2|3|4|5}
        self.MEMory_STATe_NAME = SCPI_Message(self, 'MEMory:STATe:NAME') # {1|2|3|4|5} [,<name>]
        self.MEMory_STATe_DELete = SCPI_Message(self, 'MEMory:STATe:DELete') # {1|2|3|4|5}
        self.MEMory_STATe_RECall_AUTO = SCPI_Message(self, 'MEMory:STATe:RECall:AUTO') # {OFF|ON}
        self.MEMory_STATe_VALid = SCPI_Message(self, 'MEMory:STATe:VALid') # {1|2|3|4|5}
        self.MEMory_NSTates = SCPI_Message(self, 'MEMory:NSTates')

        # System-Related Commands
        self.SYSTem_DATE = SCPI_Message(self, 'SYSTem:DATE') # <yyyy>,<mm>,<dd >
        self.SYSTem_TIME = SCPI_Message(self, 'SYSTem:TIME') # <hh>,<mm>,<ss.sss>
        self.IDN = SCPI_Message(self, '*IDN')
        self.SYSTem_CTYPe = SCPI_Message(self, 'SYSTem:CTYPe') # {100|200|300}
        self.DIAGnostic_POKE_SLOT_DATA = SCPI_Message(self, 'DIAGnostic:POKE:SLOT:DATA') # {100|200|300}, <quoted_string>
        self.DIAGnostic_PEEK_SLOT_DATA = SCPI_Message(self, 'DIAGnostic:PEEK:SLOT:DATA') # {100|200|300}
        self.DISPlay = SCPI_Message(self, 'DISPlay') # {OFF|ON}
        self.DISPlay_TEXT = SCPI_Message(self, 'DISPlay:TEXT') # <quoted_string>
        self.DISPlay_TEXT_CLEar = SCPI_Message(self, 'DISPlay:TEXT:CLEar')
        self.RST = SCPI_Message(self, '*RST')
        self.SYSTem_PRESet = SCPI_Message(self, 'SYSTem:PRESet')
        self.SYSTem_ERRor = SCPI_Message(self, 'SYSTem:ERRor')
        self.SYSTem_ALARm = SCPI_Message(self, 'SYSTem:ALARm')
        self.SYSTem_VERSion = SCPI_Message(self, 'SYSTem:VERSion')

        # Interface Configuration Commands
        self.SYSTem_INTerface = SCPI_Message(self, 'SYSTem:INTerface') # {GPIB|RS232}
        self.SYSTem_LOCal = SCPI_Message(self, 'SYSTem:LOCal')
        self.SYSTem_REMote = SCPI_Message(self, 'SYSTem:REMote')
        self.SYSTem_RWLock = SCPI_Message(self, 'SYSTem:RWLock')

        # Status System Commands
        self.STB = SCPI_Message(self, '*STB')
        self.STATus_QUEStionable_CONDition = SCPI_Message(self, 'STATus:QUEStionable:CONDition')
        self.STATus_QUEStionable_EVENt = SCPI_Message(self, 'STATus:QUEStionable:EVENt')
        self.STATus_QUEStionable_ENABle = SCPI_Message(self, 'STATus:QUEStionable:ENABle') # <enable_value >
        self.SRE = SCPI_Message(self, '*SRE') # <enable_value >
        self.ESR = SCPI_Message(self, '*ESR')
        self.ESE = SCPI_Message(self, '*ESE')
        self.STATus_ALARm_CONDition = SCPI_Message(self, 'STATus:ALARm:CONDition')
        self.STATus_ALARm_EVENt = SCPI_Message(self, 'STATus:ALARm:EVENt')
        self.STATus_ALARm_ENABle = SCPI_Message(self, 'STATus:ALARm:ENABle') # <enable_value >
        self.STATus_OPERation_CONDition = SCPI_Message(self, 'STATus:OPERation:CONDition')
        self.STATus_OPERation_EVENt = SCPI_Message(self, 'STATus:OPERation:EVENt')
        self.STATus_OPERation_ENABle = SCPI_Message(self, 'STATus:OPERation:ENABle') # <enable_value >
        self.DATA_POINts_EVENt_THReshold = SCPI_Message(self, 'DATA:POINts:EVENt:THReshold') # <num_rdgs>
        self.CLS = SCPI_Message(self, '*CLS')
        self.PSC = SCPI_Message(self, '*PSC') # {0|1}
        self.OPC = SCPI_Message(self, '*OPC')

        # Service-Related Commands
        self.DIAGnostic_DMM_CYCLes = SCPI_Message(self, 'DIAGnostic:DMM:CYCLes')
        self.DIAGnostic_RELay_CYCLes = SCPI_Message(self, 'DIAGnostic:RELay:CYCLes') # [(@<ch_list>)]
        self.TST = SCPI_Message(self, '*TST')

    def Interface_Set(self, Interface):
        self.Inter__Interfaceface = Interface

    def Scan_list_format_from_array(self, chanels):
        scan_list = '(@'
        for i, chanel in enumerate(chanels):
            if (0 == i):
                scan_list = scan_list + chanel
            else:
                scan_list = scan_list + ',' + chanel
        scan_list = scan_list + ')'
        return (scan_list) 

    def Configure_Chanels(self, measurement, chanels, range = 'AUTO', resolution = 'DEF', TCouple = 'DEF', type = 'DEF'):
        scan_list = self.Scan_list_format_from_array(chanels)
        if ('TEMPerature' == measurement):
            self.CONFigure_TEMPerature.Write(TCouple, type, resolution, scan_list) # {TCouple|RTD|FRTD|THERmistor|DEF},{<type>|DEF}[,1[,{<resolution >|MIN|MAX|DEF}]] ,(@<scan_list>)
        elif ('VOLTage_DC' == measurement):
            self.CONFigure_VOLTage_DC.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('VOLTage_AC' == measurement):
            self.CONFigure_VOLTage_AC.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('RESistance' == measurement):
            self.CONFigure_RESistance.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('FRESistance' == measurement):
            self.CONFigure_FRESistance.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('CURRent_DC ' == measurement):
            self.CONFigure_CURRent_DC.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('CURRent_AC' == measurement):
            self.CONFigure_CURRent_AC.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('FREQuency' == measurement):
            self.CONFigure_FREQuency.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)
        elif ('PERiod' == measurement):
            self.CONFigure_PERiod.Write(range, resolution, scan_list) # [{<range>|AUTO|MIN|MAX|DEF} [,<resolution>|MIN|MAX|DEF}],] (@ <scan_list>)

    def Monitor_Start(self, chanels):
        scan_list = self.Scan_list_format_from_array(chanels)
        self.ROUTe_MONitor.Write(scan_list)
        self.ROUTe_MONitor_STATe.Set()

    def Monitor_Stop(self):
        self.ROUTe_MONitor_STATe.Reset()

    def Monitor_Read_Resoult(self, Target_Function):
        self.ROUTe_MONitor_DATA.Read(Target_Function)
    
    def Scan_Data_Format_Set(self, alarm, chanel, time, unit, time_type):
        self.FORMat_READing_ALARm.Write(alarm) # {OFF|ON}
        self.FORMat_READing_CHANnel.Write(chanel) # {OFF|ON}
        self.FORMat_READing_TIME.Write(time) # {OFF|ON}
        self.FORMat_READing_UNIT.Write(unit) # {OFF|ON}
        self.FORMat_READing_TIME_TYPE.Write(time_type) # {ABSolute|RELative}

    def Scan_Start(self, scan_list, source = 'IMMediate', timer = 'MIN', count = 'INFinity'):
        if('0' == self.Scan_Going()):
            self.Scan_Data_Remove_All()
            self.ROUTe_SCAN.Write(scan_list)
            self.TRIGger_SOURce.Write(source)
            self.TRIGger_TIMer.Write(timer)
            self.TRIGger_COUNt.Write(count)
            self.INITiate.Write()

    def Scan_Stop(self):
        if('1' == self.Scan_Going()):
            self.ABORt.Write()

    def Scan_Trigger(self):
        self.TRG.Write()

    def Scan_Data_Read_Newest(self, scan_list, number = '1'):
        if(self.Scan_Data_Exists()):
            return(self.DATA_LASt.Read_Array(number, scan_list))
    
    def Scan_Data_Remove_oldest(self, number = '1'):
        if(self.Scan_Data_Exists()):
            return(self.DATA_REMove.Read_Array(number))
    
    def Scan_Data_Count(self):
        return(self.DATA_POINts.Read_String())
    
    def Scan_Data_Remove_All(self, max = '50000'):
        if(self.Scan_Data_Exists()):
            return(self.R.Read_Array_From_Block(max))
    
    def Scan_Data_Exists(self):
        if 0 == int(self.Scan_Data_Count()):
           return(False)
        else:
            return(True)

    def Scan_Going(self):
        return(self.STATus_OPERation_CONDition.Read_Bits(8)[-5])
    
    def Scan_And_Format(self, chanels, source = 'IMMediate', timer = 'MIN', count = 'INFinity'):
        self.Scan_Data_Format_Set('OFF', 'OFF', 'ON', 'OFF', 'RELative')
        self.Scan_Start(self.Scan_list_format_from_array(chanels), source, timer, count)

        t = 0
        while('1' == self.Scan_Going()):
            self.DISPlay_TEXT.Write('"Time: ' + str(round(t, 2)) + 's"')
            time.sleep(0.01)
            t = t + 0.01
        self.DISPlay_TEXT_CLEar.Write()

        trace_data = []
        for chanel in chanels:
            trace_data.append([[],[]])
        while(self.Scan_Data_Exists()):
            for i, chanel in enumerate(chanels):
                tmp = self.Scan_Data_Remove_oldest()
                trace_data[i][0].append(float(tmp[1]))
                trace_data[i][1].append(float(tmp[0]))
        print(trace_data)
        return(trace_data)
    


# ==================================== v TEST v ===========================================================================

"""
import serial
import time
import sys
sys.path.append('/home/peter/Documents/Python/Projects/TestBeam/Graph/')
import Graph

class RS232:
    def __init__(self):
        self.ser = serial.Serial()
        
    def open3(self):
        self.ser.baudrate = "115200"
        self.ser.port = '/dev/ttyS0'
        self.ser.timeout = 10
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.dsrdtr = False
        self.ser.rtscts = False
        self.ser.xonxoff = False
        self.ser.open()     

    def open2(self):
        self.ser.baudrate = "9600"
        self.ser.port = '/dev/ttyS2'
        self.ser.timeout = 10
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.dsrdtr = True
        self.ser.rtscts = False
        self.ser.xonxoff = False
        self.ser.open()  

    def open1(self):
        self.ser.baudrate = "9600"
        self.ser.port = '/dev/ttyS3'
        self.ser.timeout = 10
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.dsrdtr = True
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
            self.ser.write((command + '\n').encode("utf-8"))

    def Query(self, command):
        self.Command(command)
        #read data
        return self.Read()
    
    def Read(self):
        #read data
        text = self.ser.readline()
        if(10 == text[-1]):
            text = text[0:-1]
            if(13 == text[-1]):
                text = text[0:-1]
        return text





interface3 = RS232()
interface3.open2()
Instrument_3 = Instrument(interface3)
print(Instrument_3.IDN.Read_Array())
#Instrument_3.Configure_Chanels('VOLTage_DC', ['101'])
Instrument_3.TRIGger_SOURce.Write('IMMediate')
Instrument_3.TRIGger_COUNt.Write('2')

Instrument_3.INITiate.Write()
time.sleep(1)

time.sleep(1)

time.sleep(1)
Instrument_3.FETCh.Read_String()
Instrument_3.RST.Write()
time.sleep(1)
Instrument_3.INITiate.Write()
time.sleep(1)
Instrument_3.FETCh.Read_String()



#Instrument_1.Configure_Chanels('RESistance', ['101'])
#time.sleep(0.1)
#Graph.fast_plot("Voltage [V]",Instrument_1.Scan_And_Format(['101'], count = '10'),"X", "Y")





#print(Instrument_1.DIAGnostic_RELay_CYCLes.Read_String('(@101,102)'))
 """
# ====================================================== START ======================================================================
"""
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
"""
port_1 = RS232()
port_1.open()

instrument = Agilent_34970A(port_1)
instrument.Display_Clear()

"""