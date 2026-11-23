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

from peter_webgui import timing as Time
import numpy as np

class Message_request:
    def __init__(self, message_out, message_request_time, callback_function, message_timeout, message_delay_after, callback_args = (), callback_kwargs = None):
        self.message_out = message_out
        self.message_request_time = message_request_time
        self.callback_function = callback_function
        self.message_timeout = message_timeout
        self.message_delay_after = message_delay_after
        self.callback_args = tuple(callback_args)
        self.callback_kwargs = dict(callback_kwargs or {})

class Message_sent:
    def __init__(self, message_out, message_request_time, message_out_time , callback_function, message_timeout, timeout_start_time, callback_args = (), callback_kwargs = None):
        self.message_out = message_out
        self.message_request_time = message_request_time
        self.message_out_time = message_out_time
        self.callback_function = callback_function
        self.message_timeout = message_timeout
        self.timeout_start_time = timeout_start_time
        self.callback_args = tuple(callback_args)
        self.callback_kwargs = dict(callback_kwargs or {})


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

    def Message_out_request(self, message_out, callback_function = None, timeout = 0, message_delay_after = 0, callback_args = (), callback_kwargs = None):
        """Queue message_out for sending.

        When the reply line arrives, it is passed to the callback as
        callback_function(message_in, *callback_args, **callback_kwargs), so extra values can travel with the request:

            Communicator_1.Message_out_request('MEAS:VOLT:DC? (@101)', Store_Reading,
                                               timeout=1, callback_args=('101',), callback_kwargs={'unit': 'V'})
            def Store_Reading(message_in, channel, unit='V'): ...
        """
        self.message_out_request_list = np.append(self.message_out_request_list, Message_request(message_out, Time.Get_Time_text(), callback_function, timeout, message_delay_after, callback_args, callback_kwargs))

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
                                                                                                        Message_request_object.callback_function,
                                                                                                        timeout,
                                                                                                        Time.Start_Measureing_Elapsed_Time(),
                                                                                                        Message_request_object.callback_args,
                                                                                                        Message_request_object.callback_kwargs))
                        self.message_delay_after = Message_request_object.message_delay_after
                        self.last_message_send_time = Time.Start_Measureing_Elapsed_Time()

    def Message_in_worker(self):
        if self.working:
            message_in = self.message_line_in_function()
            if message_in != '':
                if (len(self.message_out_sent_list) != 0):
                    Message_sent_object: Message_sent = self.message_out_sent_list[0]
                    self.message_out_sent_list = np.delete(self.message_out_sent_list, 0)
                    if Message_sent_object.callback_function != None:
                        Message_sent_object.callback_function(message_in, *Message_sent_object.callback_args, **Message_sent_object.callback_kwargs)
                    if self.generate_log_function != None:
                        self.generate_log_function(Message_sent_object.message_request_time,
                                                   Message_sent_object.message_out_time,
                                                   Message_sent_object.message_out,
                                                   Time.Get_Time_text(),
                                                   message_in,
                                                   str(len(self.message_out_sent_list)))
                else:
                    if self.generate_log_function != None:
                        self.generate_log_function('', '', '', Time.Get_Time_text(), message_in, 'Unexpected!')
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
                            #if Message_sent_object.callback_function != None:
                                #Message_sent_object.callback_function('')
                            if self.generate_log_function != None:   
                                self.generate_log_function(Message_sent_object.message_request_time,
                                                       Message_sent_object.message_out_time,
                                                       Message_sent_object.message_out,
                                                       '',
                                                       '',
                                                       'Timeout!')



from nicegui import ui, run
import threading
from peter_webgui import visuals as WGV
from peter_webgui import trace_manager as TM
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


class Communicator_Log_v2:
    """Card for sending commands by hand and watching the traffic.

    Left: a multi-line text box with one command per line, and buttons to send all commands, clear the commands,
    and clear the log. Right: a grid with one row per message: out time, out message, response time, response
    message and status.

    Status values:
        OK          a reply arrived for the message
        Sent        a command with no reply expected (it does not end in '?')
        Timeout     a query got no reply within its timeout
        Unexpected  a line arrived when no message was waiting for a reply

    Lines ending in '?' are sent as queries with query_timeout seconds to answer. Other lines are sent as commands
    with no reply expected. Blank lines are skipped.

    The widget sets itself as the communicator's log function and refreshes its grid with its own ui.timer.
    Something else must still run Communicator.Message_out_worker / Message_in_worker.
    """
    Columns = ['Out time', 'Out message', 'Response time', 'Response message', 'Status']

    def __init__(self, name, communicator: Communicator, width = 1400, height = 500, default_commands = '*IDN?', query_timeout = 1, command_delay_after = 0):
        self.communicator = communicator
        self.query_timeout = query_timeout
        self.command_delay_after = command_delay_after
        self.Log_rows = []
        self.Log_lock = threading.Lock()
        self.Log_changed = False

        padding = 20
        border_width = 3
        gap = 16
        inner_width = width - 2 * (padding + border_width)
        inner_height = height - 2 * (padding + border_width)
        commands_width = 400
        button_height = WGV.Default_height

        with WGV.Card(name=name, width=width, height=height, padding=padding, border_width=border_width):
            with ui.column().style(f'gap: {WGV.Number_to_Pixel(gap)};'):
                with ui.row().style(f'gap: {WGV.Number_to_Pixel(gap)}; flex-wrap: nowrap;'):
                    self.Commands = WGV.Text_area(width=commands_width, height=inner_height - button_height - gap, default_text=default_commands)
                    self.G_Log = WGV.Grid(data=pd.DataFrame(columns=self.Columns), width=inner_width - commands_width - gap, height=inner_height - button_height - gap)
                with ui.row().style(f'gap: {WGV.Number_to_Pixel(gap)}; flex-wrap: nowrap;'):
                    button_width = (inner_width - 2 * gap) / 3  # three buttons spanning the whole inner width
                    self.B_Send = WGV.Button(lambda: self.Send_all(), name='Send all', width=button_width, background_color=WGV.Default_color)
                    self.B_Clear_commands = WGV.Button(lambda: self.Commands.Set_text(''), name='Clear cmds', width=button_width)
                    self.B_Clear_log = WGV.Button(lambda: self.Clear_log(), name='Clear log', width=button_width)
                
                # Timeout and Unexpected rows stand out in the accent colour
                for column_def in self.G_Log.Grid_element.options['columnDefs']:
                    if column_def['field'] == 'Status':
                        column_def[':cellStyle'] = (f"params => (params.value === 'Timeout' || params.value === 'Unexpected') "
                                                    f"? {{backgroundColor: '{WGV.Default_color}'}} : null")

        self.communicator.Set_generate_log_function(self.Log)
        ui.timer(0.2, self.Update)

    def Send_all(self):
        for line in self.Commands.Get_lines():
            command = line.strip()
            if command == '':
                continue
            if command.endswith('?'):
                self.communicator.Message_out_request(message_out=command, timeout=self.query_timeout)
            else:
                self.communicator.Message_out_request(message_out=command, message_delay_after=self.command_delay_after)

    def Log(self, time_request, time_out, data_out, time_in, data_in, messages_out):
        """generate_log_function for Communicator. Can be called from worker threads."""
        if messages_out == 'Timeout!':
            status = 'Timeout'
        elif messages_out == 'Unexpected!':
            status = 'Unexpected'
        elif data_in != '':
            status = 'OK'
        else:
            status = 'Sent'
        with self.Log_lock:
            self.Log_rows.append({'Out time': time_out, 'Out message': data_out,
                                  'Response time': time_in, 'Response message': data_in, 'Status': status})
            self.Log_changed = True

    def Clear_log(self):
        with self.Log_lock:
            self.Log_rows = []
            self.Log_changed = True

    def Get_log_df(self):
        with self.Log_lock:
            return pd.DataFrame(self.Log_rows, columns=self.Columns)

    def Update(self):
        with self.Log_lock:
            if not self.Log_changed:
                return
            rows = [dict(row) for row in self.Log_rows]
            self.Log_changed = False
        self.G_Log.Grid_element.options['rowData'] = rows
        self.G_Log.Grid_element.update()
        if rows:
            self.G_Log.Grid_element.run_grid_method('ensureIndexVisible', len(rows) - 1, 'bottom')


if __name__ in {"__main__", "__mp_main__"}:
    # Demo with a simulated instrument, so no serial port is needed:
    #   *IDN? and other queries ending in '?'  -> a reply after 50 ms
    #   a query containing TIMEOUT             -> no reply, so it times out
    #   SPAM                                   -> an unsolicited line 0.5 s later, logged as Unexpected
    #   other commands                         -> no reply (logged as Sent)
    import random
    import time

    class Simulated_Instrument:
        def __init__(self):
            self.lock = threading.Lock()
            self.pending = []  # (time it becomes readable, line)

        def _queue(self, delay, line):
            with self.lock:
                self.pending.append((time.monotonic() + delay, line))

        def Write_Line(self, text):
            command = text.strip().upper()
            if command == '*IDN?':
                self._queue(0.05, 'HEWLETT-PACKARD,34401A,0,11-5-2')
            elif command.endswith('?') and 'TIMEOUT' not in command:
                self._queue(0.05, f'{random.uniform(-10, 10):+.8E}')
            elif command == 'SPAM':
                self._queue(0.5, 'UNSOLICITED MESSAGE')

        def Read_Line(self):
            with self.lock:
                now = time.monotonic()
                for i, (ready_time, line) in enumerate(self.pending):
                    if ready_time <= now:
                        del self.pending[i]
                        return line
            return ''

    Instrument = Simulated_Instrument()
    Demo_communicator = Communicator(message_out_function=Instrument.Write_Line,
                                     message_line_in_function=Instrument.Read_Line,
                                     max_number_of_messages_out=1)
    Demo_communicator.Start()

    def Worker_loop():
        while True:
            Demo_communicator.Message_out_worker()
            Demo_communicator.Message_in_worker()
            time.sleep(0.01)

    @WGV.Page('/', title='Communicator_Log_v2 demo', layout='column')
    def main_page():
        WGV.Create_Label_Left('Simulated instrument: queries ending in ? are answered, a query containing TIMEOUT '
                              'is not, SPAM produces an unexpected message.', width=1400)
        Communicator_Log_v2('Communicator log', Demo_communicator,
                            default_commands='*IDN?\nCONF:VOLT:DC AUTO,DEF\nREAD?\nMEAS:TIMEOUT?\nSPAM\nREAD?')

    threading.Thread(target=Worker_loop, daemon=True).start()
    ui.run(title='Communicator_Log_v2 demo', port=8081, reload=False)
