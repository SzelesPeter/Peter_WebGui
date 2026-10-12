import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))

import Agilent_34401A

from nicegui import ui
import WebGui_Visuals as WGV
import time
import Time
import Communicator
import RS232
import pandas as pd
import Settings
import WebGui_TraceManager as WGTM
import threading

Setting_1 = Settings.Settings("HP34401A_Settings", Peter_WebGui_Path, None)
"""
Setting_1.Get_setting("Name_1", "Data_1")
Setting_1.Set_setting("Name_1", "Data_2")
Setting_1.Save_to_default_file()
Setting_1.Get_setting("Name_1", "Data_1")
"""

def debug(text1, text2, text4, text3):
    print(text2 + ' Text out: "' + text1 + '" ' + text3 + ' Text in: "' + text4 + '"')

RS232_1 = RS232.RS232()


df = pd.DataFrame({
    'Time Request': {},
    'Time Out': {},
    'Data Out': {},
    'Time In': {},
    'Data In': {},
    'Number of messages out': {},
})
def G10_Add_New_Line(time_request, time_out, data_out, time_in, data_in, messages_out):
    df.loc[len(df)] = [time_request, time_out, data_out, time_in, data_in, messages_out]
    G10.options['rowData'] = df.to_dict('records')
    G10.run_grid_method(
    'ensureIndexVisible',
    len(G10.options['rowData']) - 1,
    'bottom'
)


Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 1, generate_log_function= G10_Add_New_Line)
Instrument_1 = Agilent_34401A.Instrument(Communicator_1)

Running = False
Measure = 'DC V'
Resolution = 'DEF'
data = []
i = 1

@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with ui.row():
        with ui.column():
            with WGV.Card(name= 'HP 34401A COM Port', width= 310, height= 400):
                with ui.row(): # column with no spaceing:
                    L1 = WGV.Create_Label_Right('Port:', font_size= 20, width= 80)
                    def DDC1_Function(port):
                        RS232_1.Set_Port(port)
                        Setting_1.Set_setting("RS232_1_Port", port)
                        DDC1.set_options(RS232_1.Get_Possible_Ports())
                    DDC1 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Ports(), function_to_call=DDC1_Function, width= 160)
                    DDC1.set_value(Setting_1.Get_setting("RS232_1_Port", RS232_1.Get_Port()))
                    RS232_1.Set_Port(Setting_1.Get_setting("RS232_1_Port", RS232_1.Get_Port()))
                with ui.row():
                    L2 = WGV.Create_Label_Right('Baud:', font_size= 20, width= 80)
                    def DDC2_Function(baud):
                        Setting_1.Set_setting("RS232_1_Baud", baud)
                        RS232_1.Set_Baud(baud)
                    DDC2 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Bauds(), function_to_call=DDC2_Function, width= 160)
                    DDC2.set_value(Setting_1.Get_setting("RS232_1_Baud", RS232_1.Get_Baud()))
                    RS232_1.Set_Baud(Setting_1.Get_setting("RS232_1_Baud", RS232_1.Get_Baud()))
                with ui.row():
                    L3 = WGV.Create_Label_Right('Parity:', font_size= 20, width= 80)
                    def DDC3_Function(parity):
                        Setting_1.Set_setting("RS232_1_Parity", parity)
                        RS232_1.Set_Parity(parity)
                    DDC3 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Paritys(), function_to_call=DDC3_Function, width= 160)
                    DDC3.set_value(Setting_1.Get_setting("RS232_1_Parity", RS232_1.Get_Parity()))
                    RS232_1.Set_Parity(Setting_1.Get_setting("RS232_1_Parity", RS232_1.Get_Parity()))
                with ui.row():
                    L4 = WGV.Create_Label_Right('Flow:', font_size= 20, width= 80)
                    def DDC3_Function(flow):
                        Setting_1.Set_setting("RS232_1_Flow", flow)
                        RS232_1.Set_Flow(flow)
                    DDC4 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Flows(), function_to_call=DDC3_Function, width= 160)
                    DDC4.set_value(Setting_1.Get_setting("RS232_1_Flow", RS232_1.Get_Flow()))
                    RS232_1.Set_Flow(Setting_1.Get_setting("RS232_1_Flow", RS232_1.Get_Flow()))
                with ui.row():
                    def B5_Function():
                        Setting_1.Save_to_default_file()
                        if RS232_1.Open() == None:
                            L9.set_text('Connected')
                            Communicator_1.Start()
                    B5 = WGV.Button(lambda: B5_Function(), name='Connect', width= 120,background_color = '#B12C2C')
                    def B6_Function():
                        if RS232_1.Close() == None:
                            L9.set_text('Not Connected')
                            Communicator_1.Stop()
                    B6 = WGV.Button(lambda: B6_Function(), name='Disconnect', width= 120)
                with ui.row():
                    L9 = WGV.Create_Label_Left('Not Connected', font_size= 20, width = 200)

            with WGV.Card(name= 'HP 34401A Find', width= 310, height= 200):
                def find():
                    COM, IDE = RS232_1.Find_IDE('HEWLETT-PACKARD', '34401A')
                    print(COM)
                    print(IDE)
                    if COM:
                        DDC1.set_value(COM)
                        Setting_1.Set_setting("RS232_1_Port", COM)
                        L9.set_text('Connected')
                        Communicator_1.Start()
                        Lport2.set_text(COM)
                        Lno2.set_text(IDE[2])
                B_find = WGV.Button(lambda: threading.Thread(target=find, daemon=True).start(), name='Find', width= 120,background_color = '#B12C2C')
                with ui.row():
                    Lport1 = WGV.Create_Label_Right_Bold('Port: ', font_size= 20, width = 90)
                    Lport2 = WGV.Create_Label_Left_Bold('', font_size= 20, width = 90)
                with ui.row():
                    Lno1 = WGV.Create_Label_Right_Bold('No: ', font_size= 20, width = 90)
                    Lno2 = WGV.Create_Label_Left_Bold('', font_size= 20, width = 90)

                
        DDC_Test = WGV.Create_Dropdown_Card_With_Name(name= 'Test:', options= ['1', '2', '3'], text_width= 50, dropdown_width= 50)

        with ui.column().classes('gap-0 p-0 m-0'): # column with no spaceing
            with WGV.Card(name= 'HP34401A', width= 1000, height= 200, background_color = "#000000"):
                Display = WGV.Create_Label_Right_Bold('Hello!', font_size= 100, width = 900, height = 180, background_color = "#000000", color = "#DF9439")
            with WGV.Card(name= None, width= 1000, height= 200, background_color = "#808080"):
                global Running
                Running = False
                def set_display(text):
                    global Measure
                    sufix = ''
                    if Measure == 'DC V':
                        sufix = 'V'
                    if Measure == 'AC V':
                        sufix = 'V'
                    if Measure == 'DC I':
                        sufix = 'A'
                    if Measure == 'AC I':
                        sufix = 'A'
                    if Measure == 'Ω 2W':
                        sufix = 'Ω'
                    if Measure == 'Ω 4W':
                        sufix = 'Ω'
                    if Measure == 'Freq':
                        sufix = 'Hz'
                    if Measure == 'Period':
                        sufix = 's'
                    if Measure == 'Cont':
                        sufix = 'Ω'
                    if Measure == 'Diode':
                        sufix = 'V'
                    Display.set_text(f"{float(text):.8f}" + ' ' + sufix)
                def Reading_value_single():
                    global Measure
                    global Resolution
                    Display.set_text('Waiting')
                    if Measure == 'DC V':
                        measurement_varriable = 'VOLTage_DC'
                    if Measure == 'AC V':
                        measurement_varriable = 'VOLTage_AC'
                    if Measure == 'DC I':
                        measurement_varriable = 'CURRent_DC'
                    if Measure == 'AC I':
                        measurement_varriable = 'CURRent_AC'
                    if Measure == 'Ω 2W':
                        measurement_varriable = 'RESistance'
                    if Measure == 'Ω 4W':
                        measurement_varriable = 'FRESistance'
                    if Measure == 'Freq':
                        measurement_varriable = 'FREQuency'
                    if Measure == 'Period':
                        measurement_varriable = 'PERiod'
                    if Measure == 'Cont':
                        measurement_varriable = 'CONTinuity'
                    if Measure == 'Diode':
                        measurement_varriable = 'DIODe'
                    Instrument_1.Remote()
                    Instrument_1.Beep()
                    def Reading_value_single_response(data):
                        set_display(data)
                    Instrument_1.Measure_Chanel(measurement_varriable, Reading_value_single_response, range = 'AUTO', resolution = Resolution) #resolution = 'MIN'   resolution = 'DEF'
                    

                def Reading_value(text):
                    global Running
                    global Measure
                    global Resolution
                    if text == 'Waiting':
                        Display.set_text(text)
                    else:
                        set_display(text)
                    if Running:
                        if Measure == 'DC V':
                            measurement_varriable = 'VOLTage_DC'
                        if Measure == 'AC V':
                            measurement_varriable = 'VOLTage_AC'
                        if Measure == 'DC I':
                            measurement_varriable = 'CURRent_DC'
                        if Measure == 'AC I':
                            measurement_varriable = 'CURRent_AC'
                        if Measure == 'Ω 2W':
                            measurement_varriable = 'RESistance'
                        if Measure == 'Ω 4W':
                            measurement_varriable = 'FRESistance'
                        if Measure == 'Freq':
                            measurement_varriable = 'FREQuency'
                        if Measure == 'Period':
                            measurement_varriable = 'PERiod'
                        if Measure == 'Cont':
                            measurement_varriable = 'CONTinuity'
                        if Measure == 'Diode':
                            measurement_varriable = 'DIODe'
                        Instrument_1.Measure_Chanel(measurement_varriable, Reading_value, range = 'AUTO', resolution = Resolution) #resolution = 'MIN'   resolution = 'DEF'
                def B_Start_Function():
                    global Running
                    global Measure
                    global Resolution
                    Instrument_1.Remote()
                    Instrument_1.Beep()
                    if Measure == 'DC V':
                        measurement_varriable = 'VOLTage_DC'
                    if Measure == 'AC V':
                        measurement_varriable = 'VOLTage_AC'
                    if Measure == 'DC I':
                        measurement_varriable = 'CURRent_DC'
                    if Measure == 'AC I':
                        measurement_varriable = 'CURRent_AC'
                    if Measure == 'Ω 2W':
                        measurement_varriable = 'RESistance'
                    if Measure == 'Ω 4W':
                        measurement_varriable = 'FRESistance'
                    if Measure == 'Freq':
                        measurement_varriable = 'FREQuency'
                    if Measure == 'Period':
                        measurement_varriable = 'PERiod'
                    if Measure == 'Cont':
                        measurement_varriable = 'CONTinuity'
                    if Measure == 'Diode':
                        measurement_varriable = 'DIODe'
                    Instrument_1.Configure_Chanels(measurement_varriable, range = 'AUTO', resolution = Resolution) #resolution = 'MIN'   resolution = 'DEF'
                    Running = True
                    Reading_value('Waiting')
                def B_Stop_Function():
                    global Running
                    Running = False
                def B_Test_Function():
                    pass
                with ui.row():
                    B_Start = WGV.Button(lambda: B_Start_Function(), name='START', width= 80, background_color = "#F5F5F5", border_color = '#2A2727', text_color = "#2A2727")
                    B_Stop = WGV.Button(lambda: B_Stop_Function(), name='STOP', width= 80, background_color = "#2A2727")
                    B_Meas = WGV.Button(lambda: Reading_value_single(), name='Measure', width= 100, background_color = "#B12C2C")
                    def DDC_Measure_function(chosen_measurement):
                        global Measure
                        Measure = chosen_measurement
                    DDC_Measure = WGV.Create_Dropdown_Card(options=['DC V', 'AC V', 'DC I', 'AC I', 'Ω 2W', 'Ω 4W', 'Freq', 'Period'], function_to_call=DDC_Measure_function, width= 120, background_color = "#2A2727")
                    def DDC_Resolution_function(chosen_resolution):
                        global Resolution
                        Resolution = chosen_resolution
                    DDC_Resolution = WGV.Create_Dropdown_Card_With_Name(name= 'Resolution:',options=['DEF', 'MIN', 'MAX'], function_to_call=DDC_Resolution_function, text_width= 100, dropdown_width= 80, background_color = "#2A2727")
                with ui.row():
                    DDC_Trigger_Source = WGV.Create_Dropdown_Card_With_Name(name= 'Trigger Source:', options= ['Bus', 'Immediate', 'External'], text_width= 120, dropdown_width= 120, background_color = "#2A2727")
                    Number_input1 = WGV.Number_input(name = 'Trigger count:', text_width = 110, number_width = 100, background_color = "#2A2727", default_value = 0)
                


    with ui.row():

        with WGV.Card(name= 'Charts', width=1050, height=440):
            with ui.row().classes('gap-0 p-0 m-0'): # column with no spaceing
                chart1 = WGTM.Chart(name = 'Chart 1', xaxis_name= 'X', yaxis_name= 'Y')

        with WGV.Card(name= 'Test', width= 1000, height= 400):
            L_Test = WGV.Create_Label_Left('Not Tested', font_size= 20, width = 200)
            Running = False
            def Reading_value2(text):
                global Running
                L_Test.set_text(text)
                if text != 'Waiting':
                    global i
                    data.append([i, float(text)])
                    i = i + 1
                    chart1.add_trace('Test', data, digital= False)
                    chart1.set_xaxis_range()
                    chart1.set_yaxis_range()
                if Running:
                    Instrument_1.Measure_Chanel('VOLTage_DC', Reading_value2, range = 'AUTO', resolution = 'DEF') #resolution = 'MIN'   resolution = 'DEF'
            def B_Test_Function2():
                global Running
                Instrument_1.Remote()
                Instrument_1.Beep()
                Running = True
                Reading_value2('Waiting')
            def B_Stop_Function2():
                global Running
                Running = False
            B_Test = WGV.Button(lambda: B_Test_Function2(), name='Test', width= 120)
            B_Stop = WGV.Button(lambda: B_Stop_Function2(), name='Stop', width= 120)

    with ui.row():

 

        with WGV.Card(name= 'HP 34401A COM Port', width= 1820, height= 400):
            global G10
            G10 = WGV.Create_Grid(data=df,width= 1800)
            with ui.row():
                T10 = WGV.Text_input(default_text='*IDN?', width= 1000, font_size= 5)
                def B11_Function():
                    if T10.Text_input_element.value[-1] == '?':
                        Communicator_1.Message_out_request(message_out=T10.Text_input_element.value, timeout = 1)
                    else:
                        Communicator_1.Message_out_request(message_out=T10.Text_input_element.value)
                B11 = WGV.Button(lambda: B11_Function(), name='Write')
                L10 = WGV.Create_Label_Left('None', font_size= 20)
    


    
        
    ui.timer(0.01, Communicator_1.Message_in_worker)
    ui.timer(0.01, Communicator_1.Message_out_worker)


ui.run()