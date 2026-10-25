"""
==========================================================================================================================================================================

Button
   |
   v
Function_out___________________________________________________________________________________________________
    |                                     |                             |                                      |
    v                                     v                             v                                      v
out_message_list.append    out_message_sent_list.append    out_message_time_list.append     in_message_target_function_list.append    

==========================================================================================================================================================================

thred_handeling_the_port_out (gets called periodicaly)
   |
   v
if Messages_outr < X
    if port not buisy:
        Serial_Write(out_message_list.pop)
        Message_out = Message_out +1

==========================================================================================================================================================================

thred_handeling_the_port_In (gets called periodicaly)
   |
   v
message_in = Serial_read_line()
if message_in != ''
   |
    _________________________________________________________________
   |                                                                |
   v                                                                v
call in_message_target_function_list.pop(message_in)        Generate_report(out_message_sent_list.pop, out_message_time_list.pop, message_in, message_in_time)

==========================================================================================================================================================================
"""

import Time
import numpy as np

class Message_request:
    def __init__(self, message_out, message_request_time, message_in_target_function, message_timeout, message_delay_after):
        self.message_out = message_out
        self.message_request_time = message_request_time
        self.message_in_target_function = message_in_target_function
        self.message_timeout = message_timeout
        self.message_delay_after = message_delay_after

class Message_sent:
    def __init__(self, message_out, message_request_time, message_out_time , message_in_target_function, message_timeout, timeout_start_time):
        self.message_out = message_out
        self.message_request_time = message_request_time
        self.message_out_time = message_out_time
        self.message_in_target_function = message_in_target_function
        self.message_timeout = message_timeout
        self.timeout_start_time = timeout_start_time


class Communicator:
    def __init__(self, message_out_function, message_line_in_function, max_number_of_messages_out = 1, generate_log_function = None):
        self.working = False
        self.message_out_function = message_out_function
        self.message_line_in_function = message_line_in_function
        self.max_number_of_messages_out = max_number_of_messages_out
        self.generate_log_function = generate_log_function
        self.message_out_request_list = np.empty(0, dtype=Message_request)
        self.message_out_sent_list = np.empty(0, dtype=Message_sent)
        self.last_message_send_time = Time.Start_Measureing_Elapsed_Time()
        self.message_delay_after = 0

    def Set_generate_log_function(self, generate_log_function):
        self.generate_log_function = generate_log_function

    def Message_out_request(self, message_out, message_in_target_function = None, timeout = 0, message_delay_after = 0):
        self.message_out_request_list = np.append(self.message_out_request_list, Message_request(message_out, Time.Get_Time_text(), message_in_target_function, timeout, message_delay_after))

    def Start(self):
        self.message_out_request_list = np.empty(0, dtype=Message_request)
        self.message_out_sent_list = np.empty(0, dtype=Message_sent)
        message_in = self.message_line_in_function()
        self.working = True

    def Stop(self):
        self.message_out_request_list = np.empty(0, dtype=Message_request)
        self.message_out_sent_list = np.empty(0, dtype=Message_sent)
        self.working = False

    def Get_Working(self):
        return self.working

    def Message_out_worker(self):
        if self.working:
            if self.message_delay_after < Time.Time_Elapsed_Since_Start(self.last_message_send_time):
                if len(self.message_out_sent_list) < self.max_number_of_messages_out:
                    if len(self.message_out_request_list) != 0:
                        Message_request_object: Message_request = self.message_out_request_list[0]
                        self.message_out_request_list = np.delete(self.message_out_request_list, 0)
                        timeout = Message_request_object.message_timeout
                        if timeout != 0:
                            for message in self.message_out_sent_list:
                                timeout = timeout + message.message_timeout
                        self.message_out_function(Message_request_object.message_out)
                        self.message_out_sent_list = np.append(self.message_out_sent_list, Message_sent(Message_request_object.message_out,
                                                                                                        Message_request_object.message_request_time,
                                                                                                        Time.Get_Time_text(),
                                                                                                        Message_request_object.message_in_target_function,
                                                                                                        timeout,
                                                                                                        Time.Start_Measureing_Elapsed_Time()))
                        self.message_delay_after = Message_request_object.message_delay_after
                        self.last_message_send_time = Time.Start_Measureing_Elapsed_Time()

    def Message_in_worker(self):
        if self.working:
            message_in = self.message_line_in_function()
            if message_in != '':
                if (len(self.message_out_sent_list) != 0):
                    Message_sent_object: Message_sent = self.message_out_sent_list[0]
                    self.message_out_sent_list = np.delete(self.message_out_sent_list, 0)
                    if Message_sent_object.message_in_target_function != None:
                        Message_sent_object.message_in_target_function(message_in)
                    if self.generate_log_function != None:
                        self.generate_log_function(Message_sent_object.message_request_time,
                                                   Message_sent_object.message_out_time,
                                                   Message_sent_object.message_out,
                                                   Time.Get_Time_text(),
                                                   message_in,
                                                   str(len(self.message_out_sent_list)))
                else:
                    if self.generate_log_function != None:
                        self.generate_log_function('', '', '', message_in, Time.Get_Time_text(), 'Unexpected!')
            else:
                if len(self.message_out_sent_list != 0):
                    if self.message_out_sent_list[0].message_timeout == 0:
                        if self.generate_log_function != None:
                            Message_sent_object: Message_sent = self.message_out_sent_list[0]
                            self.message_out_sent_list = np.delete(self.message_out_sent_list, 0)
                            self.generate_log_function(Message_sent_object.message_request_time,
                                                       Message_sent_object.message_out_time,
                                                       Message_sent_object.message_out,
                                                       '',
                                                       '',
                                                       str(len(self.message_out_sent_list)))
                    else:
                        if self.message_out_sent_list[-1].message_timeout <= Time.Time_Elapsed_Since_Start(self.message_out_sent_list[-1].timeout_start_time):
                            Message_sent_object: Message_sent = self.message_out_sent_list[0]
                            self.message_out_sent_list = np.delete(self.message_out_sent_list, 0)
                            if Message_sent_object.message_in_target_function != None:
                                Message_sent_object.message_in_target_function('')
                            if self.generate_log_function != None:   
                                self.generate_log_function(Message_sent_object.message_request_time,
                                                       Message_sent_object.message_out_time,
                                                       Message_sent_object.message_out,
                                                       '',
                                                       '',
                                                       'Timeout!')



from nicegui import ui, run
import WebGui_Visuals as WGV
import WebGui_TraceManager as TM
import pandas as pd

class Communicator_Log:
    def __init__(self, name, communicator):
        self.communicator = communicator
        self.Com_Data = TM.General_Data([
                            'Time Request',
                            'Time Out',
                            'Data Out',
                            'Time In',
                            'Data In',
                            'Number of messages out',
        ])
        with WGV.Card(name= 'HP 34401A COM Port', width= 1840, height= 400):

            self.G_Log = WGV.Grid(data=self.Com_Data.df,width= 1800)
            with ui.row():
                self.T10 = WGV.Text_input(default_text='*IDN?', width= 1000, font_size= 5)
                self.B11 = WGV.Button(lambda: self.B11_Function(), name='Write')
                self.L10 = WGV.Create_Label_Left('None', font_size= 20)
    def B11_Function(self):
        if self.T10.Text_input_element.value[-1] == '?':
            self.communicator.Message_out_request(message_out=self.T10.Text_input_element.value, timeout = 1)
        else:
            self.communicator.Message_out_request(message_out=self.T10.Text_input_element.value)
    def Log(self, time_request, time_out, data_out, time_in, data_in, messages_out):
        self.Com_Data.Add_measurement_point([time_request, time_out, data_out, time_in, data_in, messages_out])
    def Update(self):
        if self.Com_Data.changed:
            self.G_Log.Grid_element.options['rowData'] = self.Com_Data.df.to_dict('records')
            self.G_Log.Grid_element.run_grid_method(
            'ensureIndexVisible',
            len(self.G_Log.Grid_element.options['rowData']) - 1,
            'bottom'
            )
            self.Com_Data.Reset_Changed()