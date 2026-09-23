import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))

from nicegui import ui
import WebGui_Visuals as WGV
import Time
import Communicator
import RS232
import pandas as pd

def debug(text1, text2, text4, text3):
    print(text2 + ' Text out: "' + text1 + '" ' + text3 + ' Text in: "' + text4 + '"')

RS232_1 = RS232.RS232()


df = pd.DataFrame({
    'Time Out': {},
    'Data Out': {},
    'Time In': {},
    'Data In': {},
})
def G10_Add_New_Line(data_out, time_out, data_in, time_in):
    df.loc[len(df)] = [time_out, data_out, time_in, data_in]
    G10.options['rowData'] = df.to_dict('records')
Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 2, generate_log_function= G10_Add_New_Line)



@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with WGV.Card(name= 'COM Port', width= '301px', height= '400px'):
        with ui.row(): # column with no spaceing:
            L1 = WGV.Create_Label_Right('Port:', font_size= '20px', width= '80px')
            def DDC1_Function(port):
                RS232_1.Set_Port(port)
                DDC1.set_options(RS232_1.Get_Possible_Ports())
            DDC1 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Ports(), function_to_call=DDC1_Function, width= '160px')
            DDC1.set_value(RS232_1.Get_Port())
        with ui.row():
            L2 = WGV.Create_Label_Right('Baud:', font_size= '20px', width= '80px')
            DDC2 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Bauds(), function_to_call=RS232_1.Set_Baud, width= '160px')
            DDC2.set_value(RS232_1.Get_Baud())
        with ui.row():
            L3 = WGV.Create_Label_Right('Parity:', font_size= '20px', width= '80px')
            DDC3 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Paritys(), function_to_call=RS232_1.Set_Parity, width= '160px')
            DDC3.set_value(RS232_1.Get_Parity())
        with ui.row():
            L4 = WGV.Create_Label_Right('Flow:', font_size= '20px', width= '80px')
            DDC4 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Flows(), function_to_call=RS232_1.Set_Flow, width= '160px')
            DDC4.set_value(RS232_1.Get_Flow())
        with ui.row():
            def B5_Function():
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
    ui.timer(2, Communicator_1.Message_out_worker)


ui.run()