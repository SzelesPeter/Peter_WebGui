import krpc
import time
import math

import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))

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

altitude_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='m'
        )
g_force_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='G'
        )
speed_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='m/s'
        )
acceleration_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='m/s2'
        )
pitch_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='deg'
        )
dynamic_pressure_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='pascal'
        )

angle_of_attack_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='deg'
        )

downrange_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='km'
        )

thrust_Trace_Data = TM.Trace_Data(
            x_unit='s',
            y_unit='N'
        )

launched = False
vessel = None
sc = None
launch_time = None

def connect():
    global vessel, sc, body
    global ut
    global altitude
    global g_force
    global speed
    global acceleration
    global pitch
    global dynamic_pressure
    global angle_of_attack
    global apoapsis
    global thrust

    conn = krpc.connect(name='Hello World',address='192.168.0.143', rpc_port=50000, stream_port=50001)
    vessel = conn.space_center.active_vessel
    print(vessel.name)

    sc = conn.space_center
    body = vessel.orbit.body

    # Set up streams for telemetry
    ut = conn.add_stream(getattr, conn.space_center, "ut")
    altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
    g_force = conn.add_stream(getattr, vessel.flight(), "g_force")
    speed = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), "speed")
    acceleration = conn.add_stream(getattr, vessel.flight(vessel.reference_frame), "acceleration")
    pitch = conn.add_stream(getattr, vessel.flight(), "pitch")
    dynamic_pressure = conn.add_stream(getattr, vessel.flight(), "dynamic_pressure")
    angle_of_attack =conn.add_stream(getattr, vessel.flight(), "angle_of_attack")
    apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
    thrust = conn.add_stream(getattr, vessel, "thrust")

def launch1():
    global launch_time, launched, launch_lat, launch_lon
    # Pre-launch setup
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    vessel.control.sas = True
    vessel.control.rcs = False
    vessel.auto_pilot.engaged = True
    vessel.control.throttle = 1.0
 
    # Countdown...
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Launch!")
    # Record the time at launch
    launch_lat = vessel.flight(body.reference_frame).latitude
    launch_lon = vessel.flight(body.reference_frame).longitude
    launch_time = sc.ut
    launched = True
    threading.Thread(target=launch2, daemon=True).start()

def launch2():

    vessel.control.activate_next_stage()
    time.sleep(2)
    vessel.control.activate_next_stage()
    while(altitude() < 10000):
        pass
    vessel.auto_pilot.target_pitch_and_heading(85, 90)

    while(thrust() > 1000):
        pass
    vessel.control.activate_next_stage()
    time.sleep(1)
    vessel.control.activate_next_stage()
    time.sleep(1)
    vessel.control.activate_next_stage()

    while(altitude() < 30000):
        pass
    vessel.auto_pilot.target_pitch_and_heading(75, 90)
    while(altitude() < 70000):
        pass
    vessel.auto_pilot.target_pitch_and_heading(65, 90)
    while(altitude() < 100000):
        pass
    vessel.auto_pilot.target_pitch_and_heading(55, 90)
    
    while(thrust() > 1000):
        pass
    vessel.control.activate_next_stage()
    time.sleep(1)
    vessel.control.activate_next_stage()  
    time.sleep(1)
    while(thrust() > 1000):
            pass
    vessel.control.activate_next_stage()
    time.sleep(1)
    vessel.control.activate_next_stage()  

def downrange():
    flight = vessel.flight(body.reference_frame)
    lat1 = math.radians(launch_lat)
    lon1 = math.radians(launch_lon)
    lat2 = math.radians(flight.latitude)
    lon2 = math.radians(flight.longitude)

    dlon = lon2 - lon1
    a = (math.sin((lat2-lat1)/2)**2
         + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2)

    angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return body.equatorial_radius * angle/1000

@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')
    with ui.row():
        B_Connect = WGV.Button(lambda: connect(), name='Connect', width= 80, background_color = "#DF9439", border_color = "#FFFFFF", text_color = "#FFFFFF")
        B_Launch = WGV.Button(lambda: launch1(), name='Launch', width= 80, background_color = "#DF9439", border_color = "#FFFFFF", text_color = "#FFFFFF")
    with ui.row():
        altitude_Trace_Manager= TM.Manager_Basic_No_Buttons(name='altitude', trace_data=altitude_Trace_Data, width=800, height=300)
        speed_Trace_Manager= TM.Manager_Basic_No_Buttons(name='speed', trace_data=speed_Trace_Data, width=800, height=300)
    with ui.row():
        acceleration_Trace_Manager= TM.Manager_Basic_No_Buttons(name='acceleration', trace_data=acceleration_Trace_Data, width=800, height=300)
        dynamic_pressure_Trace_Manager= TM.Manager_Basic_No_Buttons(name='dynamic_pressure', trace_data=dynamic_pressure_Trace_Data, width=800, height=300)
    with ui.row():
        angle_of_attack_Trace_Manager= TM.Manager_Basic_No_Buttons(name='angle_of_attack', trace_data=angle_of_attack_Trace_Data, width=800, height=300)
        pitch_Trace_Manager= TM.Manager_Basic_No_Buttons(name='pitch', trace_data=pitch_Trace_Data, width=800, height=300)
    with ui.row():
        g_force_Trace_Manager= TM.Manager_Basic_No_Buttons(name='g_force', trace_data=g_force_Trace_Data, width=800, height=300)
        downrange_Trace_Manager= TM.Manager_Basic_No_Buttons(name='downrange', trace_data=downrange_Trace_Data, width=800, height=300)
    with ui.row():
        thrust_Trace_Manager= TM.Manager_Basic_No_Buttons(name='thrust', trace_data=thrust_Trace_Data, width=800, height=300)

    def update_disp():
        if altitude_Trace_Data.changed:
            altitude_Trace_Manager.Refresh_Display()
            g_force_Trace_Manager.Refresh_Display()
            speed_Trace_Manager.Refresh_Display()
            acceleration_Trace_Manager.Refresh_Display()
            pitch_Trace_Manager.Refresh_Display()
            dynamic_pressure_Trace_Manager.Refresh_Display()
            angle_of_attack_Trace_Manager.Refresh_Display()
            downrange_Trace_Manager.Refresh_Display()
            thrust_Trace_Manager.Refresh_Display()
            
            altitude_Trace_Data.Reset_Changed()
            g_force_Trace_Data.Reset_Changed()
            speed_Trace_Data.Reset_Changed()
            acceleration_Trace_Data.Reset_Changed()
            pitch_Trace_Data.Reset_Changed()
            dynamic_pressure_Trace_Data.Reset_Changed()
            angle_of_attack_Trace_Data.Reset_Changed()
            downrange_Trace_Data.Reset_Changed()
            thrust_Trace_Data.Reset_Changed()
    ui.timer(10, update_disp)

    def log_data():
        if launched:
            flight_time = round(ut() - launch_time, 3)
            altitude_Trace_Data.Add_measurement_point('altitude', flight_time, round(altitude(), 3))
            g_force_Trace_Data.Add_measurement_point('g_force', flight_time, round(g_force(), 3))
            speed_Trace_Data.Add_measurement_point('speed', flight_time, round(speed(), 3))
            acceleration_Trace_Data.Add_measurement_point('acceleration', flight_time, round(acceleration()[1], 3))
            pitch_Trace_Data.Add_measurement_point('pitch', flight_time, round(pitch(), 3))
            dynamic_pressure_Trace_Data.Add_measurement_point('dynamic_pressure', flight_time, round(dynamic_pressure(), 3))
            angle_of_attack_Trace_Data.Add_measurement_point('angle_of_attack', flight_time, round(angle_of_attack(), 3))
            downrange_Trace_Data.Add_measurement_point('downrange', flight_time, round(downrange(), 3))
            thrust_Trace_Data.Add_measurement_point('thrust', flight_time, round(thrust(), 3))
    ui.timer(0.001, log_data)


ui.run()

