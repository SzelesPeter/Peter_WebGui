import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from threading import *

import sys
sys.path.append('/home/peter/Documents/Python/Projects/TestBeam/Graph/')
sys.path.append('/home/peter/Documents/Python/Projects/TestBeam/GUI/')
import Graph
import GUI
import CSV
import serial
from serial.tools.list_ports import comports
import time
import datetime

import Agilent_34970A
from queue import Queue
#==============================================START========================================================
#========================================================= ROOT =========================================================

root = tk.Tk()
height = 600
width = 960
root.geometry(f"{width}x{height}")
root.title("34970A v1 ")


#==================================================================EXIT==============================================
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        RS232_1.update_settings()

        if(RS232_1.ser.is_open):
            RS232_1.ser.close()
        root.destroy()

# Handle the window close event (X button)
root.protocol("WM_DELETE_WINDOW", on_closing)

#============================================================= SETTINGS =====================================================
Default_start_values = [
["tty", "baud", "hardvare_flow_control", "parity", "data_out"],
["ttyS0", "9600", "NONE", "NONE", "*IDN?"]
]
#"/home/peter/Documents/Python/Projects/TestBeam/GUI/"
setings_1 = GUI.Settings("GUI_34970A_v1_settings.txt", "/home/peter/Documents/Python/Projects/TestBeam/Agilent drivers/", Default_start_values)

#============================================================NOTEBOOK=======================================
def tab_selected(event):
    notebook = event.widget
    tab_id = notebook.select()
    tab_text = notebook.tab(tab_id, 'text')
    print(f"Selected Tab Text: {tab_text}")


notebook = ttk.Notebook(root, width=810, height=420)
notebook.place(x=150, y=0)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)
tab6 = ttk.Frame(notebook)

notebook.add(tab1, text='DMM')
notebook.add(tab2, text='Com')
notebook.add(tab3, text='Scan')
notebook.add(tab4, text='Satus')
notebook.add(tab5, text='ERROR')
notebook.add(tab6, text='Com Settings')

notebook.bind("<<NotebookTabChanged>>", tab_selected)
#======================================================== Menu ===============================================




menu = tk.Menu(root)
root.config(menu=menu)


filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_command(label="Open...")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_closing)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")

#==================================================== Main Loop ========================================

def main_thred_function():
    
    root.after(1, main_thred_function)  # Schedule again in 1ms (1 second)


# ====================================================== v Tx v ==========================================================
def DestinationThread() :
  while True :
    time.sleep(0.1)
    if instrument_queue.empty != True:
        items = instrument_queue.get()
        func = items[0]
        args = items[1]
        querry = items[2]
        response_func = items[3]
        if(querry == 1):
            response = str(func(*args))
            if response != "":
                response_queue.put([response_func, [response]])
        else:
            func(*args)

instrument_queue = Queue()
# ====================================================== ^ Tx ^ ==========================================================
# ===================================================== v Rx v ==========================================================
def ResponseThread() :
  while True :
    time.sleep(0.1)
    if response_queue.empty != True:
        items = response_queue.get()
        func = items[0]
        args = items[1]
        func(*args)

response_queue = Queue()
# ===================================================== ^ Rx ^ ==========================================================



#==================================================Time===========================================================
def Time_thred_function():
    while True:
        time_1.Time_update_thred_function()
        Debug_log.Time_label_update()
        time.sleep(0.001)

# ================================================= v Multimeter v =================================================
class Multimeter_gui:
    def __init__(self, origin, x_location, y_location, settings, com, debug):
        self.measure_setting = "DC_V"
        self.resolution = "5"
        self.Range = "AUTO"
        self.dimension = " V"
        self.sufix = ""

        self.instrument_frame = tk.Frame(origin, bg="white", width=810, height=420, bd=3, relief=tk.RAISED)
        self.instrument_frame.place(x=x_location, y=y_location)
        self.entry_var = tk.StringVar()
        self.readout = tk.Entry(self.instrument_frame,
               font=("Arial", 65, "bold"),
               bg="black",
               fg="cyan",
               width=16,
               textvariable=self.entry_var,
               justify="right",
               relief="raised")
        self.readout.place(x=0, y=0,)
        self.entry_var.set("-000.0000 mV DC")


        self.chanel_frame = tk.Frame(origin, bg="white", width=90, height=140, bd=3, relief=tk.RAISED)
        self.chanel_frame.place(x=10, y=270)
        self.chanel_label = tk.Label(self.chanel_frame, width=10, text="CHANNEL", bg= "light grey")
        self.chanel_label.place(x=0, y=0)
        # Create a Combobox widget
        self.channel_combo_box = ttk.Combobox(
            self.chanel_frame, width=7,
            state="readonly",
            values=["@101", "@102", "@103", "@104", "@105", "@106", "@107", "@108", "@109", "@110", "@111", "@112", "@113", "@114", "@115", "@116", "@117", "@118", "@119", "@120", "@121", "@122"]
        )
        self.channel_combo_box.place(x=5, y=40)
        self.channel_combo_box.bind("<<ComboboxSelected>>", self.channel_sellect)
        self.channel_combo_box.set("@101")

        self.ON_Check = IntVar() 
        self.ON_button = Checkbutton(self.chanel_frame, text = "ON", 
                    variable = self.ON_Check, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 5,
                    command = self.measure_start) 
        self.ON_button.place(x=7, y=80)

        self.function_frame = tk.Frame(origin, bg="white", width=505, height=140, bd=3, relief=tk.RAISED)
        self.function_frame.place(x=10, y=120)
        self.function_label = tk.Label(self.function_frame, width=62, text="FUNCTION", bg= "light grey")
        self.function_label.place(x=0, y=0)

        self.DC_I_button = tk.Button(self.function_frame, text="DC I", width=4, command=self.DC_I_button_function)
        self.DC_I_button.place(x=20, y=38)
        self.DC_V_button = tk.Button(self.function_frame, text="DC V", width=4, command=self.DC_V_button_function)
        self.DC_V_button.place(x=20, y=86)
        self.AC_I_button = tk.Button(self.function_frame, text="AC I", width=4, command=self.AC_I_button_function)
        self.AC_I_button.place(x=100, y=38)
        self.AC_V_button = tk.Button(self.function_frame, text="AC V", width=4, command=self.AC_V_button_function)
        self.AC_V_button.place(x=100, y=86)
        self.ohm_4W_button = tk.Button(self.function_frame, text="Ω 4W", width=4, state='disabled', command=self.ohm_4W_button_function)
        self.ohm_4W_button.place(x=180, y=38)
        self.ohm_2W_button = tk.Button(self.function_frame, text="Ω 2W", width=4, command=self.ohm_2W_button_function)
        self.ohm_2W_button.place(x=180, y=86)
        self.Period_button = tk.Button(self.function_frame, text="Period", width=4, command=self.Period_button_function)
        self.Period_button.place(x=260, y=38)
        self.Freq_button = tk.Button(self.function_frame, text="Freq", width=4, command=self.Freq_button_function)
        self.Freq_button.place(x=260, y=86)
        self.Diode_button = tk.Button(self.function_frame, text="Diode", width=4, state='disabled', command=self.Diode_button_function)
        self.Diode_button.place(x=340, y=38)
        self.Cont_button = tk.Button(self.function_frame, text="Cont", width=4, state='disabled', command=self.Cont_button_function)
        self.Cont_button.place(x=340, y=86)
        self.Temp_button = tk.Button(self.function_frame, text="Temp", width=4, state='disabled', command=self.Temp_button_function)
        self.Temp_button.place(x=420, y=38)

        self.math_frame = tk.Frame(origin, bg="white", width=270, height=140, bd=3, relief=tk.RAISED)
        self.math_frame.place(x=530, y=120)
        self.math_label = tk.Label(self.math_frame, width=33, text="MATH", bg= "light grey")
        self.math_label.place(x=0, y=0)

        self.null_button = tk.Button(self.math_frame, text="Null", width=4, state='disabled', command=self.DC_I_button)
        self.null_button.place(x=20, y=38)
        self.dB_button = tk.Button(self.math_frame, text="dB", width=4, state='disabled', command=self.DC_I_button)
        self.dB_button.place(x=100, y=38)
        self.dBm_button = tk.Button(self.math_frame, text="dBm", width=4, state='disabled', command=self.DC_V_button)
        self.dBm_button.place(x=100, y=86)
        self.min_button = tk.Button(self.math_frame, text="Min", width=4, state='disabled', command=self.DC_I_button)
        self.min_button.place(x=180, y=38)
        self.max_button = tk.Button(self.math_frame, text="Max", width=4, state='disabled', command=self.DC_V_button)
        self.max_button.place(x=180, y=86)

        self.range_frame = tk.Frame(origin, bg="white", width=90, height=65, bd=3, relief=tk.RAISED)
        self.range_frame.place(x=115, y=270)
        self.range_label = tk.Label(self.range_frame, width=10, text="RANGE", bg= "light grey")
        self.range_label.place(x=0, y=0)
        # Create a Combobox widget
        self.range_combo_box = ttk.Combobox(
            self.range_frame, width=7,
            state='disabled',
            values=["@101", "@102", "@103", "@104"]
        )
        self.range_combo_box.place(x=5, y=30)
        self.range_combo_box.bind("<<ComboboxSelected>>", self.channel_sellect)
        self.range_combo_box.set("@101")

        self.digits_frame = tk.Frame(origin, bg="white", width=90, height=65, bd=3, relief=tk.RAISED)
        self.digits_frame.place(x=115, y=345)
        self.digits_label = tk.Label(self.digits_frame, width=10, text="DIGITS", bg= "light grey")
        self.digits_label.place(x=0, y=0)
        # Create a Combobox widget
        self.digits_combo_box = ttk.Combobox(
            self.digits_frame, width=7,
            state="disabled",
            values=["4", "5", "6"]
        )
        self.digits_combo_box.place(x=5, y=30)
        self.digits_combo_box.bind("<<ComboboxSelected>>", self.channel_sellect)
        self.digits_combo_box.set("5")

        self.display_frame = tk.Frame(origin, bg="white", width=90, height=65, bd=3, relief=tk.RAISED)
        self.display_frame.place(x=500, y=345)
        self.display_label = tk.Label(self.display_frame, width=10, text="DISPLAY", bg= "light grey")
        self.display_label.place(x=0, y=0)
        self.Display_ON = IntVar() 
        self.Display_ON_button = Checkbutton(self.display_frame, text = "ON", 
                    variable = self.Display_ON, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 1, 
                    width = 5,
                    command = self.set_display) 
        self.Display_ON_button.place(x=7, y=29)
        self.Display_ON.set(1)

    def DC_I_button_function(self):
        self.measure_setting = "DC_I"
        self.dimension = " A"
        self.measure_settings_update()
    def DC_V_button_function(self):
        self.measure_setting = "DC_V"
        self.dimension = " V"
        self.measure_settings_update()
    def AC_I_button_function(self):
        self.measure_setting = "AC_I"
        self.dimension = " A"
        self.measure_settings_update()
    def AC_V_button_function(self):
        self.measure_setting = "AC_V"
        self.dimension = " V"
        self.measure_settings_update()
    def ohm_4W_button_function(self):
        self.measure_setting = "ohm_4W"
        self.dimension = " Ohm"
        self.measure_settings_update()
    def ohm_2W_button_function(self):
        self.measure_setting = "ohm_2W"
        self.dimension = " Ohm"
        self.measure_settings_update()
    def Period_button_function(self):
        self.measure_setting = "Period"
        self.dimension = " S"
        self.measure_settings_update()
    def Freq_button_function(self):
        self.measure_setting = "Freq"
        self.dimension = " Hz"
        self.measure_settings_update()
    def Diode_button_function(self):
        self.measure_setting = "Diode"
        self.dimension = " "
        self.measure_settings_update()
    def Cont_button_function(self):
        self.measure_setting = "Cont"
        self.dimension = " "
        self.measure_settings_update()
    def Temp_button_function(self):
        self.measure_setting = "Temp"
        self.dimension = " "
        self.measure_settings_update()

    def measure_settings_update(self): 
        if self.measure_setting == "DC_I":
            instrument_queue.put([Instrument.Configure.Configure_Current_DC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "DC_V":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_DC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "AC_I":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_AC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "AC_V":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_AC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "ohm_4W":
            instrument_queue.put([Instrument.Configure.Configure_Resistance_4, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "ohm_2W":
            instrument_queue.put([Instrument.Configure.Configure_Resistance_2, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "Period":
            instrument_queue.put([Instrument.Configure.Configure_Period, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "Freq":
            instrument_queue.put([Instrument.Configure.Configure_Frequency, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_setting == "Diode":
            time.sleep(0.1)
        elif self.measure_setting == "Cont":
            time.sleep(0.1)
        elif self.measure_setting == "Temp":
            time.sleep(0.1)

    def set_display(self):
        if self.Display_ON.get() == 1:
            instrument_queue.put([Instrument.Display_On, [], 0, 0])
        else:
            instrument_queue.put([Instrument.Display_Off, [], 0, 0])

    def measure_start(self):
        
        if self.ON_Check.get() == 1:
            self.measure_settings_update()
            instrument_queue.put([Instrument.Monitor.Monitoring_Start, [self.channel_combo_box.get()], 0, 0])
            instrument_queue.put([Instrument.Monitor.Monitoring_Read, [], 1, self.data_in])
        else:
             instrument_queue.put([Instrument.Monitor.Monitoring_Stop, [], 0, 0])

    def channel_sellect(self, sellected):
        self.measure_settings_update()

    def data_in(self, response):
        self.entry_var.set("{:.6f}".format(round((float( response )), 6)) + self.dimension + "  ")
        if self.ON_Check.get() == 1:
            instrument_queue.put([Instrument.Monitor.Monitoring_Read, [], 1, self.data_in])

# ================================================= ^ Multimeter ^ =================================================
# ================================================= v Scan v =================================================
class Scan_gui:
    def __init__(self, origin, x_location, y_location, settings, com, debug):

        self.scan_frame = tk.Frame(origin, bg="white", width=810, height=420, bd=3, relief=tk.RAISED)
        self.scan_frame.place(x=x_location, y=y_location)

        self.settings_frame = tk.Frame(self.scan_frame, bg="white", width=200, height=300, bd=3, relief=tk.RAISED)
        self.settings_frame.place(x=10, y=10)
        self.settings_label = tk.Label(self.settings_frame, width=24, text="SCANN SETTINGS", bg= "light grey")
        self.settings_label.place(x=0, y=0)

        self.chanel_label = tk.Label(self.settings_frame, text="Channel:", bg= "white")
        self.chanel_label.place(x=5, y=30)
        # Create a Combobox widget
        self.channel_combo_box = ttk.Combobox(
            self.settings_frame, width=7,
            state="readonly",
            values=["@101", "@102", "@103", "@104", "@105", "@106", "@107", "@108", "@109", "@110", "@111", "@112", "@113", "@114", "@115", "@116", "@117", "@118", "@119", "@120", "@121", "@122"]
        )
        self.channel_combo_box.place(x=100, y=30)
        self.channel_combo_box.set("@101")

        self.measure_label = tk.Label(self.settings_frame, text="Measure:", bg= "white")
        self.measure_label.place(x=5, y=50)
        # Create a Combobox widget
        self.measure_combo_box = ttk.Combobox(
            self.settings_frame, width=7,
            state="readonly",
            values=["@101", "DC_I", "DC_V", "AC_I", "AC_V", "ohm_4W", "ohm_2W", "Period", "Freq", "Diode", "Cont", "Temp"]
        )
        self.measure_combo_box.place(x=100, y=50)
        self.measure_combo_box.set("DC_V")

        self.start_button = tk.Button(self.settings_frame, text="Start", width=4, command=self.measure_start)
        self.start_button.place(x=10, y=200)

    def measure_settings_update(self): 
        if self.measure_combo_box.get() == "DC_I":
            instrument_queue.put([Instrument.Configure.Configure_Current_DC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "DC_V":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_DC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "AC_I":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_AC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "AC_V":
            instrument_queue.put([Instrument.Configure.Configure_Voltage_AC, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "ohm_4W":
            instrument_queue.put([Instrument.Configure.Configure_Resistance_4, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "ohm_2W":
            instrument_queue.put([Instrument.Configure.Configure_Resistance_2, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "Period":
            instrument_queue.put([Instrument.Configure.Configure_Period, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "Freq":
            instrument_queue.put([Instrument.Configure.Configure_Frequency, ["AUTO", "DEF", self.channel_combo_box.get()], 0, 0])
        elif self.measure_combo_box.get() == "Diode":
            time.sleep(0.1)
        elif self.measure_combo_box.get() == "Cont":
            time.sleep(0.1)
        elif self.measure_combo_box.get() == "Temp":
            time.sleep(0.1)

    def measure_start(self):
        
        if self.ON_Check.get() == 1:
            self.measure_settings_update()
            instrument_queue.put([Instrument.Monitor.Monitoring_Start, [self.channel_combo_box.get()], 0, 0])
            instrument_queue.put([Instrument.Monitor.Monitoring_Read, [], 1, self.data_in])
        else:
             instrument_queue.put([Instrument.Monitor.Monitoring_Stop, [], 0, 0])

    def channel_sellect(self, sellected):
        self.measure_settings_update()

    def data_in(self, response):
        self.entry_var.set("{:.6f}".format(round((float( response )), 6)) + self.dimension + "  ")
        if self.ON_Check.get() == 1:
            instrument_queue.put([Instrument.Monitor.Monitoring_Read, [], 1, self.data_in])
# ================================================= ^ Scan ^ =================================================
#==================================================== start========================================



time_1 = GUI.Time()
Debug_log = GUI.Debug_Logbox(root, 150, 450, time_1)
RS232_1 = GUI.RS232(tab6, 0, 0, setings_1, Debug_log)
RS232_1.update_COM_Port_list()
Instrument = Agilent_34970A.Instrument(RS232_1)
Multimeter = Multimeter_gui(tab1, 0, 0, setings_1, RS232_1, Debug_log)
Scan = Scan_gui(tab3, 0, 0, setings_1, RS232_1, Debug_log)
Logbox_1 = GUI.COM_Logbox(tab2, 5, 5, setings_1, RS232_1, time_1)
Finder_1 = GUI.Device_Finder("34970A Finder", root, 0, 0, Instrument, RS232_1, Debug_log)
#--------Threding--------
thred_time=Thread(target=Time_thred_function)
thred_time.daemon = True
thred_time.start()
thred_1=Thread(target=DestinationThread)
thred_1.start()
thred_2=Thread(target=ResponseThread)
thred_2.start()
#--------Main thred--------

#-------------- START TK --------------
root.mainloop()
