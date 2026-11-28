"""Delta v1: multi-page app with a Page_Selector on the left.

Pages:
    Main     (/)        Instrument_Finder: finds the Delta board (*IDN? PeterFox,Delta,001,...) on the serial ports.
                        The same search runs once when the app starts (Auto_find).
    RS-232   (/rs232)   RS232_GUI, a help card and Communicator_Log_v2, with a File_Manager below for loading / saving the
                        log's command box as a text file, and a second one for saving / loading the log grid as CSV
    I2C      (/i2c)     one page per bus (delta_buses.py): a port settings card (Config_GUI), a help card, the
    SPI      (/spi)     bus log (Bus_Log) that sends what you type, and File_Managers for the data to send (.txt)
    RS-485   (/rs485)   and the log (.csv)
    GPIO     (/gpio)
    CAN      (/can)
    Status   (/status)  RTC_GUI (reads and sets the board's clock), Board_Errors (reads or clears the board's error
                        queue) and an Error_Log of everything that went wrong (board error reports, timeouts,
                        unexpected lines)

The bus pages send the Delta board's SCPI commands (docs_legacy/SCPI_Commands.txt) over the RS-232 port, so that
traffic also shows up in the RS-232 log.

Every input's value is stored in Delta_v1_Settings.csv in the folder the app is started from (settings.py). Values
are read when the app starts, and an app-wide timer writes the file whenever one of them changes.
"""
import threading
import time
from datetime import datetime
from types import SimpleNamespace

import pandas as pd

from nicegui import app, ui

from peter_webgui import visuals as WGV
from peter_webgui import settings as Settings
from peter_webgui import rs232 as RS232
from peter_webgui import communicator as Communicator
from peter_webgui import timing as Time
from peter_webgui import instrument_visuals as IV
from peter_webgui.apps import delta_buses as Buses
from peter_webgui.apps.delta_buses import ERROR_CHECK


# ----------------------------------------------------------------------------------------------------------
# Settings, serial port and communicator (shared by all browser tabs)
# ----------------------------------------------------------------------------------------------------------

Setting_1 = Settings.Settings("Delta_v1_Settings", Settings.default_dir(), None)


def Setting_text(name, default):
    """Get a text setting. An empty cell loads from the CSV as NaN, so turn that back into ''."""
    value = Setting_1.Get_setting(name, default)
    return value if isinstance(value, str) else ('' if value != value else str(value))


RS232_1 = RS232.RS232(Setting_text("RS232_1_Port", "ttyS1"),
                      Setting_text("RS232_1_Baud", "9600"),
                      Setting_text("RS232_1_Parity", "NONE"),
                      Setting_text("RS232_1_Flow", "NONE"),
                      float(Setting_1.Get_setting("RS232_1_Timeout", 0.01)))
Setting_1.Update_from("RS232_1_Port", RS232_1.Get_Port)
Setting_1.Update_from("RS232_1_Baud", RS232_1.Get_Baud)
Setting_1.Update_from("RS232_1_Parity", RS232_1.Get_Parity)
Setting_1.Update_from("RS232_1_Flow", RS232_1.Get_Flow)
Setting_1.Update_from("RS232_1_Timeout", RS232_1.Get_Timeout)

# The Delta board's *IDN? fields (firmware PET_IDN_MANUFACTURER / PET_IDN_MODEL / PET_IDN_SERIAL_NUMBER)
DELTA_IDN_MANUFACTURER = "PeterFox"
DELTA_IDN_MODEL = "Delta"
DELTA_IDN_SERIAL_NUMBER = "001"
# What Instrument_Finder looks for. ERROR collects [number, description] entries for the Error_Log on the Status page.
Delta_1 = SimpleNamespace(Vendor=DELTA_IDN_MANUFACTURER, Model=DELTA_IDN_MODEL, ERROR=[])

# Values of inputs that live on a page. Each browser tab builds its own widgets, so they write here on change,
# and the settings read from here.
State = {
    'Instrument_Finder_1_No':   int(float(Setting_1.Get_setting("Instrument_Finder_1_No", DELTA_IDN_SERIAL_NUMBER))),
    'Com_Log_1_Commands':       Setting_text("Com_Log_1_Commands", "*IDN?"),
    'Com_Log_1_Delay':          float(Setting_1.Get_setting("Com_Log_1_Delay", 0)),
    'Com_File_1_Folder':        Setting_text("Com_File_1_Folder", Settings.default_dir()),
    'Com_File_1_Extensions':    Setting_text("Com_File_1_Extensions", ".txt"),
    'Com_File_1_Filename':      Setting_text("Com_File_1_Filename", "commands.txt"),
    'Log_File_1_Folder':        Setting_text("Log_File_1_Folder", Settings.default_dir()),
    'Log_File_1_Extensions':    Setting_text("Log_File_1_Extensions", ".csv"),
    'Log_File_1_Filename':      Setting_text("Log_File_1_Filename", "rs232_log.csv"),
}
for _key in State:
    Setting_1.Update_from(_key, lambda k=_key: State[k])


def Add_state(key, value):
    State[key] = value
    Setting_1.Update_from(key, lambda: State[key])


def Add_bus_state(bus):
    """Settings of one bus page (delta_buses.BUSES), e.g. for I2C: I2C_1_<field>, I2C_Log_1_Commands / _Delay,
    I2C_File_1_* (data files) and I2C_Log_File_1_* (log files)."""
    k = bus.key
    for field in bus.fields:
        Add_state(f'{k}_1_{field.key}', Setting_text(f'{k}_1_{field.key}', field.default))
    Add_state(f'{k}_Log_1_Commands', Setting_text(f'{k}_Log_1_Commands', Buses.Default_commands(bus)))
    Add_state(f'{k}_Log_1_Delay', float(Setting_1.Get_setting(f'{k}_Log_1_Delay', 0)))
    for prefix, extension, filename in ((f'{k}_File_1', '.txt', bus.data_file), (f'{k}_Log_File_1', '.csv', bus.log_file)):
        Add_state(f'{prefix}_Folder', Setting_text(f'{prefix}_Folder', Settings.default_dir()))
        Add_state(f'{prefix}_Extensions', Setting_text(f'{prefix}_Extensions', extension))
        Add_state(f'{prefix}_Filename', Setting_text(f'{prefix}_Filename', filename))


for _bus in Buses.BUSES.values():
    Add_bus_state(_bus)

Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line,
                                           message_line_in_function=RS232_1.Read_Line,
                                           max_number_of_messages_out=1)
Communicator_1.Start()


def RTC_set_command(moment):
    """SCPI line that sets the board clock to moment (a datetime) and reports the result (:SYST:ERR?)."""
    return (f':RTC:DATE {moment.year},{moment.month},{moment.day};'
            f':RTC:TIME {moment.hour},{moment.minute},{moment.second}{ERROR_CHECK}')


def Sync_board_clock():
    """Set the board clock to this PC's time. Runs every time the RS-232 port is opened (Connect, or Find on the
    Main page). A failure shows up in the Error_Log on the Status page."""
    Communicator_1.Message_out_request(message_out=RTC_set_command(datetime.now()), timeout=1)


RS232_1.Add_open_function(Sync_board_clock)


def Parse_board_error(reply):
    """'-113,"Undefined header;2026-11-25 14:05:09"' -> (-113, 'Undefined header (board time 2026-11-25 14:05:09)').
    Returns None for 0,"No error"."""
    number, _, text = reply.strip().partition(',')
    try:
        number = int(number)
    except ValueError:
        return 'Reply', reply.strip()        # not an error report, keep it as it is
    if number == 0:
        return None
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] == '"':
        text = text[1:-1]
    description, _, board_time = text.partition(';')
    return number, f'{description} (board time {board_time})' if board_time else description


def Collect_errors(time_request, time_out, data_out, time_in, data_in, messages_out):
    """Communicator log listener (worker thread): puts every problem it sees into Delta_1.ERROR.

    - the reply to any message that asks :SYST:ERR? (the bus pages add it to their commands), unless it is 0,"No error"
    - a query that timed out
    - a line from the board that no message was waiting for
    """
    if messages_out == 'Timeout!':
        Delta_1.ERROR.append(['Timeout', f'No reply to {data_out}'])
    elif messages_out == 'Unexpected!':
        Delta_1.ERROR.append(['Unexpected', f'Line nobody asked for: {data_in}'])
    elif data_in and data_out.upper().replace(':', '').endswith('SYSTERR?'):
        error = Parse_board_error(data_in)
        if error:
            Delta_1.ERROR.append(list(error))


Communicator_1.Add_log_function(Collect_errors)


# ----------------------------------------------------------------------------------------------------------
# Page contents
# ----------------------------------------------------------------------------------------------------------

def Duration_text(seconds):
    """75 -> '1 min 15 s', 97662774 -> '1130 d 8 h 32 min 54 s'."""
    parts = []
    for unit, size in (('d', 86400), ('h', 3600), ('min', 60)):
        if seconds >= size:
            parts.append(f'{seconds // size} {unit}')
            seconds %= size
    if seconds or not parts:
        parts.append(f'{seconds} s')
    return ' '.join(parts)


class RTC_GUI:
    """Card that reads and sets the Delta board's real-time clock (SCPI_Commands.txt section 14).

    Read         :RTC:NOW? -> shows the board's date and time, and how far it is from this PC's clock
    Set from PC  sends this PC's date and time (:RTC:DATE y,m,d;:RTC:TIME h,m,s in one line). This also happens
                 by itself every time the RS-232 port is opened (Sync_board_clock).
    Set          sends the date and time typed into the Date / Time boxes (YYYY-MM-DD, HH:MM:SS)
    Both "Set" buttons add :SYST:ERR? to the line, so the status line shows whether the board accepted it, and then
    read the clock back. The board counts in whole seconds and supports the years 2000..2099.
    """
    def __init__(self, name, communicator, width = 320, height = 450, query_timeout = 1):
        self.communicator = communicator
        self.query_timeout = query_timeout
        self.Replies = []                 # (kind, text, PC time) from the worker thread, shown by Update()
        self.Replies_lock = threading.Lock()

        inner_width = width - 46
        label_width = 80
        input_width = inner_width - label_width - 16
        now = datetime.now()

        with WGV.Card(name=name, width=width, height=height):
            self.L_Board = WGV.Create_Label_Center_Bold('----------  --:--:--', font_size=24, width=inner_width)
            self.L_Difference = ui.label('Board clock not read yet').style(
                f'color: {WGV.Default_border_color}; font-size: 14px; width: {inner_width}px; text-align: center;')
            WGV.Button(lambda: self.Read(), name='Read', width=inner_width)
            WGV.Button(lambda: self.Set_from_PC(), name='Set from PC', width=inner_width, background_color=WGV.Default_color)
            with ui.row():
                WGV.Create_Label_Right('Date:', font_size=20, width=label_width)
                self.T_Date = WGV.Text_input(width=input_width, default_text=now.strftime('%Y-%m-%d'))
            with ui.row():
                WGV.Create_Label_Right('Time:', font_size=20, width=label_width)
                self.T_Time = WGV.Text_input(width=input_width, default_text=now.strftime('%H:%M:%S'))
            WGV.Button(lambda: self.Set_typed(), name='Set', width=inner_width)
            self.L_Status = ui.label('').style(f'color: {WGV.Default_border_color}; font-size: 14px; width: {inner_width}px;')

        ui.timer(0.2, self.Update)

    def Set_status(self, text, error = False):
        self.L_Status.set_text(text)
        self.L_Status.style(f'color: {WGV.Default_color if error else WGV.Default_border_color};')

    # ---------- requests ----------
    def Query(self, command, kind):
        self.communicator.Message_out_request(message_out=command, callback_function=self.Queue_reply,
                                              callback_args=(kind,), timeout=self.query_timeout)

    def Queue_reply(self, message_in, kind):
        # Worker thread: note the PC time the reply arrived, for the board - PC difference.
        with self.Replies_lock:
            self.Replies.append((kind, message_in.strip(), datetime.now()))

    def Read(self):
        self.Query(':RTC:NOW?', 'now')

    def Send(self, moment):
        if not 2000 <= moment.year <= 2099:
            self.Set_status('The board supports the years 2000..2099', error=True)
            return
        self.Query(RTC_set_command(moment), 'set')
        self.Set_status('Setting...')
        self.Read()

    def Set_from_PC(self):
        self.Send(datetime.now())

    def Set_typed(self):
        text = f'{(self.T_Date.Text_input_element.value or "").strip()} {(self.T_Time.Text_input_element.value or "").strip()}'
        try:
            moment = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.Set_status('Date must be YYYY-MM-DD and time HH:MM:SS', error=True)
            return
        self.Send(moment)

    # ---------- replies (GUI thread) ----------
    def Update(self):
        with self.Replies_lock:
            replies, self.Replies = self.Replies, []
        for kind, text, pc_time in replies:
            if kind == 'set':
                ok = text.startswith('0,')
                self.Set_status('Clock set' if ok else f'Set failed: {text}', error=not ok)
            elif kind == 'now':                                      # 2026-11-25 14:05:09
                try:
                    board_time = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    self.Set_status(f'Unexpected reply to :RTC:NOW?: {text}', error=True)
                    continue
                self.L_Board.set_text(board_time.strftime('%Y-%m-%d  %H:%M:%S'))
                seconds = round((board_time - pc_time.replace(microsecond=0)).total_seconds())
                if seconds == 0:
                    self.L_Difference.set_text('Same as this PC (to the second)')
                else:
                    self.L_Difference.set_text(f'Board is {Duration_text(abs(seconds))} {"ahead of" if seconds > 0 else "behind"} this PC')


# Result of the search that runs when the app starts (Auto_find), shown by the Delta Find card on the Main page.
Auto_find_result = {'running': False, 'done': False, 'port': None, 'idn': None, 'error': None}


async def Auto_find():
    """At start-up: do what Delta Find's "Find" button does (any Delta board, any serial number) and connect.
    Connecting also sets the board's clock (Sync_board_clock)."""
    Auto_find_result.update(running=True, done=False)
    try:
        port, idn = await IV.Find_and_connect(RS232_1, Delta_1, Communicator_1)
        Auto_find_result.update(port=port, idn=idn, error=None)
        print(f'Delta board found on {port}: {",".join(idn)}' if port else 'Delta board not found')
    except Exception as e:
        Auto_find_result.update(port=None, idn=None, error=str(e))
        print(f'Delta board search failed: {e}')
    finally:
        Auto_find_result.update(running=False, done=True)


def main_page():
    with ui.row():
        # "Find" takes any Delta board, "Find No." also needs the serial number in the box (001 = 1).
        Instrument_Finder_1 = IV.Instrument_Finder('Delta Find', RS232_1, Delta_1, Communicator_1,
                                                   Default_No=State['Instrument_Finder_1_No'], width=320, height=450)
        Instrument_Finder_1.NI_No.Number_input_element.on_value_change(
            lambda e: State.__setitem__('Instrument_Finder_1_No', int(e.value)) if e.value is not None else None)

    # Show the start-up search: at once if it has finished, otherwise as soon as it does.
    def Show_auto_find():
        if Auto_find_result['running']:
            Instrument_Finder_1.Lport2.set_text('Searching...')
            return
        if Auto_find_result['error']:
            Instrument_Finder_1.Lport2.set_text('Error')
        elif Auto_find_result['done']:
            Instrument_Finder_1.Show_result(Auto_find_result['port'], Auto_find_result['idn'])
        Auto_find_timer.cancel()
    Auto_find_timer = ui.timer(0.5, Show_auto_find)
    Show_auto_find()


def rs232_page():
    with ui.row():
        # First row, next to Pages: port settings and the help card, all three 450 high (like the bus pages).
        RS232_GUI_1 = RS232.RS232_GUI('RS-232 Port', RS232_1)
        Buses.Help_card('How to use the RS-232 Log', Buses.RS232_LOG_HELP)
    with ui.row():
        Com_Log_1 = Communicator.Communicator_Log_v2('RS-232 Log', Communicator_1, height=450,
                                                     message_delay=State['Com_Log_1_Delay'],
                                                     function_when_delay_changed=lambda v: State.__setitem__('Com_Log_1_Delay', v),
                                                     default_commands=State['Com_Log_1_Commands'])

        def Commands_changed(text):
            State['Com_Log_1_Commands'] = text
        Com_Log_1.Commands.function_when_changed = Commands_changed

    # Load a text file into the RS-232 Log command box, or save the command box into a file.
    def Load_commands(path):
        Com_Log_1.Commands.Set_text(path.read_text(encoding='utf-8'))   # Set_text also updates State via the change callback

    def Save_commands(path):
        path.write_text(Com_Log_1.Commands.Get_text(), encoding='utf-8')

    # Save the RS-232 Log grid into a CSV, or load a saved CSV back into the grid.
    def Load_log(path):
        Com_Log_1.Set_log_df(pd.read_csv(path, keep_default_na=False))

    def Save_log(path):
        Com_Log_1.Get_log_df().to_csv(path, index=False)

    with ui.row():
        File_Manager_1 = File_Manager_with_state('Com_File_1', Load_commands, Save_commands, name='Command Files')
        File_Manager_2 = File_Manager_with_state('Log_File_1', Load_log, Save_log, name='Log Files')


def File_Manager_with_state(prefix, load_function, save_function, name):
    """File_Manager whose Folder / Extensions / Filename boxes start from, and write back to, State[<prefix>_*]."""
    fm = WGV.File_Manager(load_function, save_function, name=name,
                          folder=State[f'{prefix}_Folder'],
                          extensions=State[f'{prefix}_Extensions'],
                          filename=State[f'{prefix}_Filename'])
    for suffix, text_input in (('Folder', fm.Folder_input), ('Extensions', fm.Extensions_input), ('Filename', fm.Filename_input)):
        text_input.Text_input_element.on_value_change(lambda e, k=f'{prefix}_{suffix}': State.__setitem__(k, e.value or ''))
    return fm


class Board_Errors:
    """Card with buttons for the Delta board's error queue.

    "Read errors" asks how many errors are queued (:SYST:ERR:COUN?) and then reads each one (:SYST:ERR?); the
    replies reach the Error_Log through Collect_errors. "Clear queue" sends *CLS, which deletes them unread.
    """
    def __init__(self, name, communicator, width = 320, height = 450, query_timeout = 1):
        self.communicator = communicator
        self.query_timeout = query_timeout
        button_width = width - 46
        with WGV.Card(name=name, width=width, height=height):
            WGV.Button(lambda: self.Read_errors(), name='Read errors', width=button_width, background_color=WGV.Default_color)
            WGV.Button(lambda: self.communicator.Message_out_request(message_out='*CLS'), name='Clear queue', width=button_width)
            ui.label('Errors also show up here on their own when a reply to :SYST:ERR? reports one (the bus '
                     'pages ask after every command), when a query times out, and when the board sends a line '
                     'nobody asked for.').style(f'color: {WGV.Default_border_color}; font-size: 14px; width: {button_width}px;')

    def Read_errors(self):
        self.communicator.Message_out_request(message_out=':SYST:ERR:COUN?', callback_function=self.Read_count,
                                              timeout=self.query_timeout)

    def Read_count(self, reply):
        # Worker thread: queue one :SYST:ERR? per waiting error (the queue holds at most 16).
        try:
            count = min(int(reply.strip()), 16)
        except ValueError:
            Delta_1.ERROR.append(['Reply', f'Unexpected reply to :SYST:ERR:COUN?: {reply.strip()}'])
            return
        for _ in range(count):
            self.communicator.Message_out_request(message_out=':SYST:ERR?', timeout=self.query_timeout)


def status_page():
    with ui.row():
        RTC_GUI_1 = RTC_GUI('Board Clock', Communicator_1)
    with ui.row():
        Board_Errors('Board Errors', Communicator_1)
        Error_Log_1 = IV.Error_Log('Delta Errors', Delta_1, width=1280 - 320 - 16, height=450)   # with Board_Errors: 1280 wide, like the other pages
    Error_Log_1.Update()   # errors collected while the page was closed show at once
    ui.timer(0.5, Error_Log_1.Update)


def Bus_page(bus):
    """Page builder for one bus of delta_buses.BUSES: port card + help card, the log, and two file managers."""
    def page():
        k = bus.key
        with ui.row():
            # First row, next to Pages: port settings and the help card, all three 450 high.
            Buses.Config_GUI(bus.port_title, Communicator_1, State, f'{k}_1', bus)
            Buses.Help_card(f'How to use the {bus.title} Log', Buses.Help_html(bus))
        with ui.row():
            Log = bus.log_class(f'{bus.title} Log', Communicator_1, height=450, default_commands=State[f'{k}_Log_1_Commands'],
                                message_delay=State[f'{k}_Log_1_Delay'],
                                function_when_delay_changed=lambda v: State.__setitem__(f'{k}_Log_1_Delay', v))
            Log.Commands.function_when_changed = lambda text: State.__setitem__(f'{k}_Log_1_Commands', text)

        def Load_data(path):
            Log.Commands.Set_text(path.read_text(encoding='utf-8'))

        def Save_data(path):
            path.write_text(Log.Commands.Get_text(), encoding='utf-8')

        def Load_log(path):
            Log.Set_log_df(pd.read_csv(path, keep_default_na=False, dtype=str))

        def Save_log(path):
            Log.Get_log_df().to_csv(path, index=False)

        with ui.row():
            File_Manager_with_state(f'{k}_File_1', Load_data, Save_data, name=f'{bus.title} Data Files')
            File_Manager_with_state(f'{k}_Log_File_1', Load_log, Save_log, name=f'{bus.title} Log Files')
    return page


# (path, button text, builder)
PAGES = ([('/', 'Main', main_page), ('/rs232', 'RS-232', rs232_page)]
         + [(bus.path, bus.title, Bus_page(bus)) for bus in Buses.BUSES.values()]
         + [('/status', 'Status', status_page)])


def register_page(path, name, builder):
    # A separate function per page so each page function closes over its own path/builder.
    @WGV.Page(path, title=f'Delta v1 - {name}', layout='row')
    def page():
        WGV.Page_Selector([(p, n) for p, n, _ in PAGES], current_path=path)
        with ui.column():
            builder()


for _path, _name, _builder in PAGES:
    register_page(_path, _name, _builder)


# ----------------------------------------------------------------------------------------------------------
# Background work
# ----------------------------------------------------------------------------------------------------------

def Worker_loop(worker):
    """Run worker every 10 ms for ever. An exception is printed (once per kind) and the loop goes on, so one bad
    read or write can't stop the communication for the rest of the session."""
    last_error = None
    while True:
        try:
            worker()
            last_error = None
        except Exception as e:
            if repr(e) != last_error:
                print(f'{worker.__name__} failed: {e!r}')
                last_error = repr(e)
            time.sleep(0.5)
        time.sleep(0.01)


def message_in_loop():
    Worker_loop(Communicator_1.Message_in_worker)


def message_out_loop():
    Worker_loop(Communicator_1.Message_out_worker)


def main():
    threading.Thread(target=message_in_loop, daemon=True).start()
    threading.Thread(target=message_out_loop, daemon=True).start()
    app.timer(1, Setting_1.Save_if_changed)   # save settings within a second of any change
    app.on_shutdown(Setting_1.Save_if_changed)
    app.on_startup(Auto_find)   # find and connect the Delta board, as if "Find" was pressed on the Main page
    ui.run(title='Delta v1', reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
