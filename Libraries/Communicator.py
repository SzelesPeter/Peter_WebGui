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

class Communicator:
    def __init__(self, message_out_function, message_line_in_function, max_number_of_messages_out = 1, default_message_in_target_function = None, generate_log_function = None):
        self.message_out_function = message_out_function
        self.message_line_in_function = message_line_in_function
        self.max_number_of_messages_out = max_number_of_messages_out
        self.default_message_in_target_function = default_message_in_target_function
        self.generate_log_function = generate_log_function
        self.message_out_list = []
        self.message_out_sent_list = []
        self.message_out_time_list = []
        self.message_in_target_function_list = []
        self.number_of_messages_out = 0

    def Message_out_request(self, message_out, in_message_target_function):
        self.message_out_list.append(message_out)
        self.message_out_sent_list.append(message_out)
        self.message_out_time_list.append(Time.Get_Time_text())
        self.message_in_target_function_list.append(in_message_target_function)

    def Message_out_worker(self):
        if self.number_of_messages_out < self.max_number_of_messages_out:
            if len(self.message_out_list) != 0:
                self.message_out_function(self.message_out_list.pop())
                self.number_of_messages_out = self.number_of_messages_out +1

    def Message_in_worker(self):
        message_in = self.message_line_in_function()
        if message_in != '':
            if self.number_of_messages_out > 0:
                self.number_of_messages_out = self.number_of_messages_out -1
            if self.generate_log_function != None:
                if (len(self.message_out_sent_list) != 0) and (len(self.message_out_time_list) != 0):
                    self.generate_log_function(self.message_out_sent_list.pop(), self.message_out_time_list.pop(), message_in, Time.Get_Time_text())
                else:
                    self.generate_log_function('None', 'None', message_in, Time.Get_Time_text())
            if len(self.message_in_target_function_list) != 0:
                self.message_in_target_function_list.pop()(message_in)
            else:
                if self.default_message_in_target_function != None:
                    self.default_message_in_target_function(message_in)


    



import serial