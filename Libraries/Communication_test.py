

from nicegui import ui
import WebGui_Visuals as WGV
import Time
import Communicator
import RS232

def debug(text1, text2, text4, text3):
    print(text2 + ' Text out: "' + text1 + '" ' + text3 + ' Text in: "' + text4 + '"')

RS232_1 = RS232.RS232()
Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 2, generate_log_function= debug)



@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with WGV.Card(name= 'COM Port', width= '500px', height= '800px'):
        with ui.row():
            L1 = WGV.Create_Label('Port:', font_size= '20px')
            DDC1 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Ports(), function_to_call=RS232_1.Set_Port)
            DDC1.set_value(RS232_1.Get_Port())
        with ui.row():
            L2 = WGV.Create_Label('Baud:', font_size= '20px')
            DDC2 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Bauds(), function_to_call=RS232_1.Set_Baud)
            DDC2.set_value(RS232_1.Get_Baud())
        with ui.row():
            L3 = WGV.Create_Label('Parity:', font_size= '20px')
            DDC3 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Paritys(), function_to_call=RS232_1.Set_Parity)
            DDC3.set_value(RS232_1.Get_Parity())
        with ui.row():
            L4 = WGV.Create_Label('Baud:', font_size= '20px')
            DDC4 = WGV.Create_Dropdown_Card(options=RS232_1.Get_Possible_Flows(), function_to_call=RS232_1.Set_Flow)
            DDC4.set_value(RS232_1.Get_Flow())
        with ui.row():
            B5 = WGV.Button(lambda: RS232_1.Open(), name='Connect')
            B6 = WGV.Button(lambda: RS232_1.Close(), name='Disconnect')
        with ui.row():
            global L9
            B7 = WGV.Button(lambda: Communicator_1.Message_out_request(message_out='*IDN?', in_message_target_function=L9.set_text), name='Write')
        with ui.row():
            global L9
            L9 = WGV.Create_Label('None', font_size= '20px')

    global L10
    L10 = WGV.Create_Label('None', font_size= '20px')
        
    ui.timer(0.1, Communicator_1.Message_in_worker)
    ui.timer(2, Communicator_1.Message_out_worker)


ui.run()