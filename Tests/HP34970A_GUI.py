import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))

import Agilent_34970A

from nicegui import ui
import WebGui_Visuals as WGV
import time
import Time
import Communicator
import RS232
import pandas as pd
import Settings

Setting_1 = Settings.Settings("HP34970A_Settings", Peter_WebGui_Path, None)
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


Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 2, generate_log_function= G10_Add_New_Line)
Instrument_1 = Agilent_34970A.Instrument(Communicator_1)

@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')


    with WGV.Card(name= 'Test', width= '1000px', height= '400px'):
        L_Test = WGV.Create_Label_Left('Not Tested', font_size= '20px', width = '200px')
        global Running
        Running = False
        def Reading_value(text):
            global Running
            L_Test.set_text(text)
            if Running:
                Instrument_1.Monitor_Read_Resoult(Reading_value)
        def B_Test_Function():
            global Running
            print(L_Test.set_text)
            Instrument_1.Configure_Chanels(measurement = 'VOLTage_DC',chanels =  ['102'])
            Instrument_1.Monitor_Start(['102'])
            Running = True
            Reading_value('Waiting')
        def B_Stop_Function():
            global Running
            Running = False
        B_Test = WGV.Button(lambda: B_Test_Function(), name='Test', width= '120px')
        B_Stop = WGV.Button(lambda: B_Stop_Function(), name='Stop', width= '120px')



    with WGV.Card(name= 'COM Port', width= '301px', height= '400px'):
        with ui.row(): # column with no spaceing:
            L1 = WGV.Create_Label_Right('Port:', font_size= '20px', width= '80px')
            def DDC1_Function(port):
                RS232_1.Set_Port(port)
                Setting_1.Set_setting("RS232_1_Port", port)
                DDC1.set_options(RS232_1.Get_Possible_Ports())
            DDC1 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Ports(), function_to_call=DDC1_Function, width= '160px')
            DDC1.set_value(Setting_1.Get_setting("RS232_1_Port", RS232_1.Get_Port()))
        with ui.row():
            L2 = WGV.Create_Label_Right('Baud:', font_size= '20px', width= '80px')
            def DDC2_Function(baud):
                Setting_1.Set_setting("RS232_1_Baud", baud)
                RS232_1.Set_Baud(baud)
            DDC2 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Bauds(), function_to_call=DDC2_Function, width= '160px')
            DDC2.set_value(Setting_1.Get_setting("RS232_1_Baud", RS232_1.Get_Baud()))
        with ui.row():
            L3 = WGV.Create_Label_Right('Parity:', font_size= '20px', width= '80px')
            def DDC3_Function(parity):
                Setting_1.Set_setting("RS232_1_Parity", parity)
                RS232_1.Set_Parity(parity)
            DDC3 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Paritys(), function_to_call=DDC3_Function, width= '160px')
            DDC3.set_value(Setting_1.Get_setting("RS232_1_Parity", RS232_1.Get_Parity()))
        with ui.row():
            L4 = WGV.Create_Label_Right('Flow:', font_size= '20px', width= '80px')
            def DDC3_Function(flow):
                Setting_1.Set_setting("RS232_1_Flow", flow)
                RS232_1.Set_Flow(flow)
            DDC4 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Flows(), function_to_call=DDC3_Function, width= '160px')
            DDC4.set_value(Setting_1.Get_setting("RS232_1_Flow", RS232_1.Get_Flow()))
        with ui.row():
            def B5_Function():
                Setting_1.Save_to_default_file()
                if RS232_1.Open() == None:
                    L9.set_text('Connected')
            B5 = WGV.Button(lambda: B5_Function(), name='Connect', width= '120px')
            def B6_Function():
                if RS232_1.Close() == None:
                    L9.set_text('Not Connected')
            B6 = WGV.Button(lambda: B6_Function(), name='Disconnect', width= '120px')
        with ui.row():
            L9 = WGV.Create_Label_Left('Not Connected', font_size= '20px', width = '200px')

    with WGV.Card(name= 'COM Port', width= '2042px', height= '400px'):
        global G10
        G10 = WGV.Create_Grid(data=df,width= 2000)
        with ui.row():
            T10 = WGV.Text_input(default_text='*IDN?', width= '1000px', font_size= '5px')
            def B11_Function():
                if T10.Text_input_element.value[-1] == '?':
                    Communicator_1.Message_out_request(message_out=T10.Text_input_element.value)
                else:
                    Communicator_1.Message_out_request(message_out=T10.Text_input_element.value, in_message_target_function=None)
            B11 = WGV.Button(lambda: B11_Function(), name='Write')
            L10 = WGV.Create_Label_Left('None', font_size= '20px')
    


    
        
    ui.timer(0.1, Communicator_1.Message_in_worker)
    ui.timer(0.1, Communicator_1.Message_out_worker)


ui.run()