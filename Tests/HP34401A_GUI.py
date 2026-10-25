import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))

import Agilent_34401A

import asyncio
from nicegui import ui, run
import WebGui_Visuals as WGV
import time
import Time
import Communicator
import RS232
import pandas as pd
import Settings
import WebGui_TraceManager as TM
import threading



Setting_1 = Settings.Settings("HP34401A_Settings", Peter_WebGui_Path, None)

RS232_1 = RS232.RS232(Setting_1.Get_setting("RS232_1_Port", "ttyS1"),
                      Setting_1.Get_setting("RS232_1_Baud", "9600"),
                      Setting_1.Get_setting("RS232_1_Parity", "NONE"),
                      Setting_1.Get_setting("RS232_1_Flow", "NONE"),
                      float(Setting_1.Get_setting("RS232_1_Timeout", 0.01))
                      )
Setting_1.Update_from("RS232_1_Port", RS232_1.Get_Port)
Setting_1.Update_from("RS232_1_Baud", RS232_1.Get_Baud)
Setting_1.Update_from("RS232_1_Parity", RS232_1.Get_Parity)
Setting_1.Update_from("RS232_1_Flow", RS232_1.Get_Flow)
Setting_1.Update_from("RS232_1_Timeout", RS232_1.Get_Timeout)

Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 1, generate_log_function= None)
Instrument_1 = Agilent_34401A.Instrument(Communicator_1,
                                         Setting_1.Get_setting("Instrument_1_Measurement", 'DC V'),
                                         Setting_1.Get_setting("Instrument_1_Range", 'AUTO'),
                                         Setting_1.Get_setting("Instrument_1_Resolution", 'DEF'),
                                         Setting_1.Get_setting("Instrument_1_Trigger_Source", 'IMMediate'), 
                                         Setting_1.Get_setting("Instrument_1_Trigger_Count", 'INFinity'))
Setting_1.Update_from("Instrument_1_Measurement", Instrument_1.Get_Measurement)
Setting_1.Update_from("Instrument_1_Range", Instrument_1.Get_Range)
Setting_1.Update_from("Instrument_1_Resolution", Instrument_1.Get_Resolution)
Setting_1.Update_from("Instrument_1_Trigger_Source", Instrument_1.Get_Trigger_Source),
Setting_1.Update_from("Instrument_1_Trigger_Count", Instrument_1.Get_Trigger_Count)
Communicator_1.Start()
Trace_Data = TM.Trace_Data(
            x_unit='n',
            y_unit='V'
        )

class Instrument_Finder:
    def __init__(self,name: str, RS232: RS232.RS232, Instrument: Agilent_34401A.Instrument, Communicator: Communicator.Communicator = None, Default_No: int = 0, RS232_GUI: RS232.RS232_GUI = None):
        self.RS232 = RS232
        self.Instrument = Instrument
        self.Communicator = Communicator
        self.RS232_GUI = RS232_GUI
        with WGV.Card(name= name, width= 310, height= 300):
            with ui.row():
                self.B_find = WGV.Button(
                    lambda: asyncio.create_task(self.find()),
                    name='Find',
                    width=120,
                    background_color='#B12C2C'
                )
                self.B_find = WGV.Button(
                    lambda: asyncio.create_task(self.find(self.NI_No.Number_input_element.value)),
                    name='Find No.',
                    width=120,
                    background_color='#DF9439'
                )
            with ui.row():
                self.NI_No = WGV.Number_input(name = 'Serial No.: ', text_width = 100, number_width = 100, default_value = Default_No, min = 0, max = 9999)
            with ui.row():
                self.Lport1 = WGV.Create_Label_Right_Bold('Port: ', font_size= 20, width = 120)
                self.Lport2 = WGV.Create_Label_Left_Bold('', font_size= 20, width = 90)
            with ui.row():
                self.Lno1 = WGV.Create_Label_Right_Bold('Serial No.: ', font_size= 20, width = 120)
                self.Lno2 = WGV.Create_Label_Left_Bold('', font_size= 20, width = 90)
                
    async def find(self, No: int= None):
        self.Lport2.set_text('Searching...')
        self.Lno2.set_text('')

        if self.Communicator != None:
            self.Communicator.Stop()
        if self.RS232_GUI != None:
            self.RS232_GUI.B_Disconnect_Function()

        try:
            COM, IDE = await run.io_bound(
                self.RS232.Find_IDE,
                self.Instrument.Vendor,
                self.Instrument.Model,
                No
            )

            if COM:
                self.Lport2.set_text(COM)
                self.Lno2.set_text(IDE[2])
                if self.RS232_GUI != None:
                    self.RS232_GUI.DDC_Port_Function(COM)
                    self.RS232_GUI.B_Connect_Function()
                if self.Communicator != None:
                    self.Communicator.Start()
                return
            else:
                self.Lport2.set_text('Not found')

        except Exception as e:
            self.Lport2.set_text('Error')
            print(f'Instrument search failed: {e}')

    def Get_No(self):
        return self.NI_No.Number_input_element.value


Running = False
i = 0
sweep_thread = None
wait = False

@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with ui.row():
        with ui.column():
            RS232_GUI_1 = RS232.RS232_GUI('HP 34401A COM Port', RS232_1)
            Instrument_Finder_1 = Instrument_Finder('HP 34401A Find', RS232_1, Instrument_1, Communicator_1, int(Setting_1.Get_setting("Instrument_Finder_1_No", "0")), RS232_GUI_1)
            Setting_1.Update_from("Instrument_Finder_1_No", Instrument_Finder_1.Get_No)

        with ui.column():
            with ui.column().classes('gap-0 p-0 m-0'): # column with no spaceing
                with WGV.Card(name= 'HP34401A', width= 1000, height= 200, background_color = "#000000"):
                    Display = WGV.Create_Label_Right_Bold('Hello! :3', font_size= 100, width = 900, height = 180, background_color = "#000000", color = "#DF9439")
                with WGV.Card(name= None, width= 1000, height= 200, background_color = "#808080"):
                    global Running
                    Running = False
                    def set_display(text):
                        if len(f"{float(text):.8f}") > 12:
                            if float(text) > 100_000_000:
                                Display.set_text('Overload!')
                            else:
                                Display.set_text(f"{float(text):.2f}" + ' ' + Instrument_1.Get_Sufix())
                        else:
                            Display.set_text(f"{float(text):.8f}" + ' ' + Instrument_1.Get_Sufix())
                    def Reading_value_single():
                        Display.set_text('Waiting...')
                        Instrument_1.Remote()
                        Instrument_1.Beep()
                        def Reading_value_single_response(data):
                            set_display(data)
                        Instrument_1.Measure_Chanel(Reading_value_single_response)

                    def Reading_value(text):
                        global Running
                        if text == 'Waiting...':
                            Display.set_text(text)
                        else:
                            set_display(text)
                        if Running:
                            Instrument_1.Scan_Read(Reading_value)
                    def B_Start_Function():
                        global Running
                        Instrument_1.Remote()
                        Instrument_1.Beep()
                        Instrument_1.Scan_Configure()
                        Running = True
                        Reading_value('Waiting...')
                    def B_Stop_Function():
                        global Running
                        Running = False
                    with ui.row():
                        B_Meas = WGV.Button(lambda: Reading_value_single(), name='Measure', width= 100, background_color = "#B12C2C")
                        DDC_Measurement = WGV.Create_Dropdown_Card(options=Instrument_1.Get_Possoble_Measurement(), function_to_call=Instrument_1.Set_Measurement, width= 120, background_color = "#2A2727")
                        DDC_Measurement.set_value(Instrument_1.Measurement.upper())
                        DDC_Range = WGV.Create_Dropdown_Card_With_Name(name= 'Range:',options=Instrument_1.Get_Possoble_Range(), function_to_call=Instrument_1.Set_Range, text_width= 70, dropdown_width= 80, background_color = "#2A2727", editable = True)
                        if Instrument_1.Range.upper() not in DDC_Range.options:
                            DDC_Range.options.append(Instrument_1.Range.upper())
                        DDC_Range.set_value(Instrument_1.Range.upper())
                        DDC_Resolution = WGV.Create_Dropdown_Card_With_Name(name= 'Resolution:',options=Instrument_1.Get_Possoble_Resolution(), function_to_call=Instrument_1.Set_Resolution, text_width= 100, dropdown_width= 80, background_color = "#2A2727", editable = True)
                        if Instrument_1.Resolution.upper() not in DDC_Resolution.options:
                            DDC_Resolution.options.append(Instrument_1.Resolution.upper())
                        DDC_Resolution.set_value(Instrument_1.Resolution.upper())
                    with ui.row():
                        B_Start = WGV.Button(lambda: B_Start_Function(), name='START', width= 80, background_color = "#DF9439", border_color = '#2A2727', text_color = "#2A2727")
                        B_Stop = WGV.Button(lambda: B_Stop_Function(), name='STOP', width= 80, background_color = "#F5F5F5", border_color = '#2A2727', text_color = "#2A2727")
                        DDC_Trigger_Source = WGV.Create_Dropdown_Card_With_Name(name= 'Trigger Source:', options=Instrument_1.Get_Possoble_Trigger_Source(), function_to_call=Instrument_1.Set_Trigger_Source, text_width= 120, dropdown_width= 140, background_color = "#2A2727")
                        DDC_Trigger_Source.set_value(Instrument_1.Trigger_Source.upper())
                        DDC_Trigger_Count = WGV.Create_Dropdown_Card_With_Name(name= 'Trigger Count:', options=Instrument_1.Get_Possoble_Trigger_Count(), function_to_call=Instrument_1.Set_Trigger_Count, text_width= 120, dropdown_width= 120, background_color = "#2A2727", editable = True)
                        if Instrument_1.Trigger_Count.upper() not in DDC_Trigger_Count.options:
                            DDC_Trigger_Count.options.append(Instrument_1.Trigger_Count.upper())
                        DDC_Trigger_Count.set_value(Instrument_1.Trigger_Count.upper())
                    with ui.row():
                        WGV.Create_Label_Left_Bold(text = 'For continous readout set Trigger Source: IMMEDIATE, Triger Count: 1.', width = 600, color='#000000')
            
            with WGV.Card(name= 'Sweep', width=1000, height=150):
                with ui.row():

                    def sweep():
                        global Running
                        global i
                    
                        if Running and i < NI_Lenght.Number_input_element.value:
                            Instrument_1.Scan_Read(save_red_data)
                            time.sleep(NI_Delay.Number_input_element.value)
                        else:
                            Running = False
                            print("Sweep finished")

                    def start_sweep():
                        global sweep_thread, Running, i
                        i = 0
                        if sweep_thread is not None and sweep_thread.is_alive():
                            return  # Prevent starting a second sweep
                        Instrument_1.Remote()
                        Instrument_1.Beep()
                        Instrument_1.Scan_Configure()
                        Running = True
                        sweep_thread = threading.Thread(target=sweep, daemon=True)
                        sweep_thread.start()

                    def save_red_data(text):
                        global i
                        Trace_Data.Add_measurement_point(Trace_Name.Text_input_element.value, i, float(text))
                        i = i + 1
                        sweep()
                            
                    B_Start = WGV.Button(lambda: start_sweep(), name='START', width= 80, background_color = "#DF9439", border_color = "#FFFFFF", text_color = "#FFFFFF")
                    B_Stop = WGV.Button(lambda: B_Stop_Function(), name='STOP', width= 80, background_color = "#F5F5F5", border_color = '#2A2727', text_color = "#2A2727")

                    WGV.Create_Label_Left_Bold(text = 'Trace Name:', width = 100)
                    Trace_Name = WGV.Text_input(width = 200)
                with ui.row():
                    NI_Delay = WGV.Number_input(name = 'Measurement delay: ', text_width = 160, number_width = 100, default_value = 0, min = 0, max = 9999)
                    NI_Lenght = WGV.Number_input(name = 'Measurement points: ', text_width = 160, number_width = 100, default_value = 40, min = 1, max = 9999)
            global MB_test
            MB_test = TM.Manager_Basic(name='Trace Manager Basic', trace_data=Trace_Data, width=1000, height=1000, save_path = Setting_1.Get_setting("MB_test_save_path", ''), save_name = Setting_1.Get_setting("MB_test_save_name", ''), load_path = Setting_1.Get_setting("MB_test_load_path", ''), load_name = Setting_1.Get_setting("MB_test_load_name", 'DC V'))
            Setting_1.Update_from("MB_test_save_path", MB_test.Get_save_path)
            Setting_1.Update_from("MB_test_save_name", MB_test.Get_save_name)
            Setting_1.Update_from("MB_test_load_path", MB_test.Get_load_path)
            Setting_1.Update_from("MB_test_load_name", MB_test.Get_load_name)

    with ui.row():
        Com_Log_1 = Communicator.Communicator_Log('HP 34401A COM Port', Communicator_1)
        Communicator_1.Set_generate_log_function(Com_Log_1.Log)
        Settings.Settings_GUI('Settings', Setting_1)

    def update():
        if Trace_Data.changed:
            MB_test.Refresh_Display()
            Trace_Data.Reset_Changed()
        Com_Log_1.Update()

    ui.timer(1, update)

def message_in_loop():
    while True:
        Communicator_1.Message_in_worker()
        time.sleep(0.01)

def message_out_loop():
    while True:
        Communicator_1.Message_out_worker()
        time.sleep(0.01)

threading.Thread(target=message_in_loop, daemon=True).start()
threading.Thread(target=message_out_loop, daemon=True).start()

ui.run()