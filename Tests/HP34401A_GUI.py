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

import SVG
import math




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
Trace_Data = TM.Trace_Data(
            x_unit='n',
            y_unit='V'
        )

Communicator_1.Start()


Status_on = False










# ==========================================================
# Diagram drawing helpers
# ==========================================================

def draw_register(
    svg,
    x, y,
    title,
    subtitle,
    labels,
    colors,
    indices,
    gate_x,
    row_height=25,
    box_width=134,
    enable_width=67,
    crossed_rows=None,
):
    """Draw a register, enable register, and its OR convergence gate."""

    crossed_rows = crossed_rows or []

    count = len(labels)
    height = count * row_height

    enable_x = x + box_width + 15
    gate_y = y + height / 2

    # Titles
    svg.text(
        x + box_width / 2, y - 35,
        title, 21, anchor="middle", weight="bold"
    )

    svg.text(
        x + box_width / 2, y - 12,
        subtitle, 17, anchor="middle"
    )

    svg.text(
        enable_x + enable_width / 2, y - 12,
        "Enable Register", 17, anchor="middle"
    )

    # Register outlines
    svg.rect(x, y, box_width, height)
    svg.rect(enable_x, y, enable_width, height)

    # Draw rows
    for i, label in enumerate(labels):
    
        yy = y + i * row_height
        cy = yy + row_height / 2

        # Horizontal row separator
        if i > 0:
            svg.line(x, yy, x + box_width, yy)
            svg.line(
                enable_x, yy,
                enable_x + enable_width, yy
            )

        # Register label
        svg.text(
            x + 5, cy + 5,
            label, 15, color = colors[i]
        )

        # Bit number
        if indices[i] is not None:
            svg.text(
                x - 8, cy + 5,
                str(indices[i]),
                16,
                anchor="end"
            )

        # Crossed enable row
        if i in crossed_rows:
            svg.line(
                enable_x, yy,
                enable_x + enable_width, yy + row_height,
                width=1
            )
            svg.line(
                enable_x, yy + row_height,
                enable_x + enable_width, yy,
                width=1
            )

    # Draw convergence lines
    for i in range(count):
    
        cy = y + i * row_height + row_height / 2

        # Lines start at enable register
        start_x = enable_x + enable_width

        # Spread the lines around the gate
        target_y = (
            gate_y + (i - (count - 1) / 2) * 11
        )

        dx = gate_x - start_x
        dy = target_y - gate_y

        length = math.hypot(dx, dy) or 1

        end_x = gate_x - 38 * dx / length
        end_y = gate_y + 38 * dy / length

        svg.line(
            start_x, cy,
            end_x, end_y,
            width=1
        )

    # OR gate
    svg.logic_gate(gate_x, gate_y)

    svg.text(
        gate_x + 18, gate_y - 16,
        '"OR"', 16
    )

    return {
        "x": x,
        "y": y,
        "width": box_width,
        "height": height,
        "enable_x": enable_x,
        "gate_x": gate_x,
        "gate_y": gate_y,
        "right": x + box_width,
        "bottom": y + height,
        "row_height": row_height,
    }


# ==========================================================
# Binary weights
# ==========================================================

def draw_binary_weights(svg):

    x, y = 718, 49
    w, h = 209, 179

    svg.text(
        x + w / 2, y - 10,
        "Binary Weights",
        21,
        anchor="middle",
        weight="bold"
    )

    svg.rect(x, y, w, h)

    left_x = x + 10
    right_x = x + 108

    for i in range(8):
    
        yy = y + 24 + i * 21

        left = f"2{['⁰','¹','²','³','⁴','⁵','⁶','⁷'][i]}  =  {2**i}"
        right = f"2{['⁸','⁹','¹⁰','¹¹','¹²','¹³','¹⁴','¹⁵'][i]}  =  {2**(i+8)}"

        svg.text(left_x, yy, left, 15)
        svg.text(right_x, yy, right, 15)


# ==========================================================
# Output buffer
# ==========================================================

def draw_output_buffer(svg):

    x, y = 574, 676
    w, h = 150, 129

    svg.text(
        x + w / 2, y - 14,
        "Output Buffer",
        22,
        anchor="middle",
        weight="bold"
    )

    svg.rect(x, y, w, h)

    row_height = h / 5

    for i in range(1, 5):
        svg.line(
            x, y + i * row_height,
            x + w, y + i * row_height
        )


# ==========================================================
# Main diagram
# ==========================================================

def create_diagram():

    svg = SVG.SVG(
        name="Status_Register_Diagram",
        width=950,
        height=850
    )

    svg.start()

    # ------------------------------------------------------
    # QUESTIONABLE DATA - 16 bits
    # ------------------------------------------------------
    questionable_labels = []
    questionable_colors = []
    for bit in Instrument_1.Questionable_Data_Register.Bits:
        questionable_labels.append(bit.Name)
        if bit.Event_Register == True:
            questionable_colors.append("#B12C2C")
        else:
            questionable_colors.append("#000000")

    questionable_indices = [
        0, 1, None, None, None, None, None, None,
        None, 9, None, 11, 12, None, None, 15
    ]

    questionable = draw_register(
        svg,
        x=88,
        y=77,
        title="Questionable Data",
        subtitle="Event Register",
        labels=questionable_labels,
        colors=questionable_colors,
        indices=questionable_indices,
        gate_x=432,
        row_height=25,
    )

    svg.text(
        88, 505,
        "STAT:QUES:EVEN?",
        15
    )

    svg.text(
        238, 505,
        "STAT:QUES:ENAB <value>",
        15
    )

    svg.text(
        238, 523,
        "STAT:QUES:ENAB?",
        15
    )

    # ------------------------------------------------------
    # STANDARD EVENT - 8 bits
    # ------------------------------------------------------

    standard_labels = []
    standard_colors = []
    for bit in Instrument_1.Standard_Event_Register.Bits:
        standard_labels.append(bit.Name)
        if bit.Event_Register == True:
            standard_colors.append("#B12C2C")
        else:
            standard_colors.append("#000000")

    standard_indices = [
        0, None, 2, 3, 4, 5, None, 7
    ]

    standard = draw_register(
        svg,
        x=88,
        y=604,
        title="Standard Event",
        subtitle="Event Register",
        labels=standard_labels,
        colors=standard_colors,
        indices=standard_indices,
        gate_x=392,
        row_height=25,
    )

    svg.text(
        88, 825,
        "*ESR?",
        15
    )

    svg.text(
        238, 825,
        "*ESE <value>",
        15
    )

    svg.text(
        238, 843,
        "*ESE?",
        15
    )

    # ------------------------------------------------------
    # STATUS BYTE - 8 bits
    # ------------------------------------------------------

    status_labels = []
    status_colors = []
    for bit in Instrument_1.Status_Byte.Bits:
        status_labels.append(bit.Name)
        if bit.Event_Register == True:
            status_colors.append("#B12C2C")
        else:
            status_colors.append("#000000")

    status_indices = [
        0, None, None, 3, 4, 5, 6, 7
    ]

    status = draw_register(
        svg,
        x=574,
        y=339,
        title="Status Byte",
        subtitle="Summary Register",
        labels=status_labels,
        colors=status_colors,
        indices=status_indices,
        gate_x=877,
        row_height=25,
        crossed_rows=[6],
    )

    svg.text(
        574, 583,
        "Serial Poll (SPOLL)",
        15
    )

    svg.text(
        574, 600,
        '"STB?',
        15
    )

    svg.text(
        723, 583,
        "*SRE <value>",
        15
    )

    svg.text(
        723, 600,
        "*SRE?",
        15
    )

    # ------------------------------------------------------
    # BINARY WEIGHTS
    # ------------------------------------------------------

    draw_binary_weights(svg)

    # ------------------------------------------------------
    # OUTPUT BUFFER
    # ------------------------------------------------------

    draw_output_buffer(svg)

    # ------------------------------------------------------
    # INTERCONNECTIONS
    # ------------------------------------------------------

    # Questionable Data OR -> Status Byte bit 3
    svg.line(470, 281, 486, 281)
    svg.line(486, 281, 486, 427)
    svg.line(486, 427, 574, 427)

    # Standard Event OR -> Status Byte bit 5
    svg.line(430, 704, 442, 704)
    svg.line(442, 704, 442, 477)
    svg.line(442, 477, 574, 477)

    # Status Byte Message Available -> Output Buffer
    svg.line(574, 452, 486, 452)
    svg.line(486, 452, 486, 740)
    svg.line(486, 740, 558, 740)

    # Status Byte OR output
    svg.line(915, 439, 928, 439)
    svg.line(928, 439, 928, 606)
    svg.line(928, 606, 530, 606)
    svg.line(530, 606, 530, 504)
    svg.line(530, 504, 574, 504)

    # ------------------------------------------------------
    # FINISH SVG
    # ------------------------------------------------------

    svg.end()

    return svg.svg
























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
    ui.page_title("HP34401A")
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

    with WGV.Card(name= 'Status', width=1000, height=1870):
        def Status_set(value):
            global Status_on
            Status_on = value
        WGV.Checkbox(name= 'Status on', default_value = False, function_when_changed = Status_set )
        SVG_1 = SVG.SVG()
        SVG_1.svg = create_diagram()
        SVG_Box_1 = WGV.SVG_Box(SVG_1)
        with ui.row():
            for byte in Instrument_1.Status_Bytes:
                with WGV.Card(name= byte.Name, width=300, height=950):
                    for i in range(len(byte.Bits)):
                        if (byte.Bits[i].Name != 'Not Used') and (byte.Bits[i].Name != 'Request Service'):
                            WGV.Checkbox(name= byte.Bits[i].Name, default_value = True, function_when_changed = byte.Bits[len(byte.Bits)-1-i].Set_Enable_Register)
                            byte.Bits[len(byte.Bits)-1-i].Set_Enable_Register(1)

    def update():
        global Status_on
        if Trace_Data.changed:
            MB_test.Refresh_Display()
            Trace_Data.Reset_Changed()
        Com_Log_1.Update()
        #if Instrument_1.Status_Byte.Event_Register_Changed() or Instrument_1.Standard_Event_Register.Event_Register_Changed() or Instrument_1.Questionable_Data_Register.Event_Register_Changed():
        #Instrument_1.Status_Byte.Reset_Event_Register_Changed()
        #Instrument_1.Standard_Event_Register.Reset_Event_Register_Changed()
        #Instrument_1.Questionable_Data_Register.Reset_Event_Register_Changed()
        if Status_on == True:
            SVG_1.svg = create_diagram()
            SVG_Box_1.Update()
            print('1')
            if Communicator_1.working == True:
                print('3')
                Instrument_1.Poll()

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