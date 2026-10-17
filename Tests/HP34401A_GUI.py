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
import WebGui_TraceManager as WGTM
import threading

Setting_1 = Settings.Settings("HP34401A_Settings", Peter_WebGui_Path, None)


RS232_1 = RS232.RS232(Setting_1.Get_setting("RS232_1_Port", "ttyS1"),
                      Setting_1.Get_setting("RS232_1_Baud", "9600"),
                      Setting_1.Get_setting("RS232_1_Parity", "NONE"),
                      Setting_1.Get_setting("RS232_1_Flow", "NONE"),
                      float(Setting_1.Get_setting("RS232_1_Timeout", 0.01))
                      )

def G10_Add_New_Line(time_request, time_out, data_out, time_in, data_in, messages_out):
    df.loc[len(df)] = [time_request, time_out, data_out, time_in, data_in, messages_out]
    G10.options['rowData'] = df.to_dict('records')
    G10.run_grid_method(
    'ensureIndexVisible',
    len(G10.options['rowData']) - 1,
    'bottom'
)

df = pd.DataFrame({
    'Time Request': {},
    'Time Out': {},
    'Data Out': {},
    'Time In': {},
    'Data In': {},
    'Number of messages out': {},
})

Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line, message_line_in_function=RS232_1.Read_Line, max_number_of_messages_out= 1, generate_log_function= G10_Add_New_Line)
Instrument_1 = Agilent_34401A.Instrument(Communicator_1,
                                         Setting_1.Get_setting("Instrument_1_Measurement", 'DC V'),
                                         Setting_1.Get_setting("Instrument_1_Range", 'AUTO'),
                                         Setting_1.Get_setting("Instrument_1_Resolution", 'DEF'),
                                         Setting_1.Get_setting("Instrument_1_Trigger_Source", 'IMMediate'), 
                                         Setting_1.Get_setting("Instrument_1_Trigger_Count", 'INFinity'))
Communicator_1.Start()


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

data = []
i = 1

@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with ui.row():
        with ui.column():
            RS232_GUI_1 = RS232.RS232_GUI('HP 34401A COM Port', RS232_1)
            Instrument_Finder_1 = Instrument_Finder('HP 34401A Find', RS232_1, Instrument_1, Communicator_1, int(Setting_1.Get_setting("Instrument_Finder_1_No", "0")), RS232_GUI_1)

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
                        DDC_Measurement.set_value(Instrument_1.Measurement)
                        DDC_Range = WGV.Create_Dropdown_Card_With_Name(name= 'Range:',options=Instrument_1.Get_Possoble_Range(), function_to_call=Instrument_1.Set_Range, text_width= 100, dropdown_width= 80, background_color = "#2A2727", editable = True)
                        if Instrument_1.Range not in DDC_Range.options:
                            DDC_Range.options.append(Instrument_1.Range)
                        DDC_Range.set_value(Instrument_1.Range)
                        DDC_Resolution = WGV.Create_Dropdown_Card_With_Name(name= 'Resolution:',options=Instrument_1.Get_Possoble_Resolution(), function_to_call=Instrument_1.Set_Resolution, text_width= 100, dropdown_width= 80, background_color = "#2A2727", editable = True)
                        if Instrument_1.Resolution not in DDC_Resolution.options:
                            DDC_Resolution.options.append(Instrument_1.Resolution)
                        DDC_Resolution.set_value(Instrument_1.Resolution)
                    with ui.row():
                        B_Start = WGV.Button(lambda: B_Start_Function(), name='START', width= 80, background_color = "#DF9439", border_color = '#2A2727', text_color = "#2A2727")
                        B_Stop = WGV.Button(lambda: B_Stop_Function(), name='STOP', width= 80, background_color = "#F5F5F5", border_color = '#2A2727', text_color = "#2A2727")
                        DDC_Trigger_Source = WGV.Create_Dropdown_Card_With_Name(name= 'Trigger Source:', options=Instrument_1.Get_Possoble_Trigger_Source(), function_to_call=Instrument_1.Set_Trigger_Source, text_width= 120, dropdown_width= 140, background_color = "#2A2727")
                        DDC_Trigger_Source.set_value(Instrument_1.Trigger_Source)
                        DDC_Trigger_Count = WGV.Create_Dropdown_Card_With_Name(name= 'Trigger Count:', options=Instrument_1.Get_Possoble_Trigger_Count(), function_to_call=Instrument_1.Set_Trigger_Count, text_width= 120, dropdown_width= 120, background_color = "#2A2727", editable = True)
                        if Instrument_1.Trigger_Count not in DDC_Trigger_Count.options:
                            DDC_Trigger_Count.options.append(Instrument_1.Trigger_Count)
                        DDC_Trigger_Count.set_value(Instrument_1.Trigger_Count)

            with WGV.Card(name= 'Charts', width=1000, height=440):
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

 

        with WGV.Card(name= 'HP 34401A COM Port', width= 1840, height= 400):
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

            
        with WGV.Card(name= 'Settings', width= 1000, height= 400):
            
            G_save = WGV.Create_Grid(data=Setting_1.df,width= 960, editable = True)
            def Load_Settings():
                nonlocal G_save
                Setting_1.Read_from_default_file()
                G_save.options['rowData'] = Setting_1.df.to_dict('records')
            def Save_Settings():
                Setting_1.Set_setting("RS232_1_Port", RS232_1.Get_Port())
                Setting_1.Set_setting("RS232_1_Baud", RS232_1.Get_Baud())
                Setting_1.Set_setting("RS232_1_Parity", RS232_1.Get_Parity())
                Setting_1.Set_setting("RS232_1_Flow", RS232_1.Get_Flow())
                Setting_1.Set_setting("RS232_1_Timeout", str(RS232_1.Get_Timeout()))
                Setting_1.Set_setting("Instrument_Finder_1_No", str(Instrument_Finder_1.Get_No()))
                Setting_1.Set_setting("Instrument_1_Measurement", Instrument_1.Measurement)
                Setting_1.Set_setting("Instrument_1_Range", Instrument_1.Range)
                Setting_1.Set_setting("Instrument_1_Resolution", Instrument_1.Resolution)
                Setting_1.Set_setting("Instrument_1_Trigger_Source", Instrument_1.Trigger_Source),
                Setting_1.Set_setting("Instrument_1_Trigger_Count", Instrument_1.Trigger_Count)
                Setting_1.Save_to_default_file()
            with ui.row():
                #B_update = WGV.Button(lambda: Save_Settings(), name='Update Optios', width= 180)
                #B_edit = WGV.Button(lambda: Edit_Settings(), name='Save Edits', width= 180)
                B_save = WGV.Button(lambda: Save_Settings(), name='Save to file', width= 180)
                B_load = WGV.Button(lambda: Load_Settings(), name='Load from file', width= 180)
    




    
    ui.timer(0.01, Communicator_1.Message_in_worker)
    ui.timer(0.01, Communicator_1.Message_out_worker)


ui.run()