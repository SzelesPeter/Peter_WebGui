"""Delta v1: multi-page app with a Page_Selector on the left.

Pages:
    Main     (/)        empty for now
    RS-232   (/rs232)   RS232_GUI and Communicator_Log_v2
    Status   (/status)  empty for now

Every input's value is stored in Delta_v1_Settings.csv in the folder the app is started from (settings.py). Values
are read when the app starts, and an app-wide timer writes the file whenever one of them changes.
"""
import threading
import time

from nicegui import app, ui

from peter_webgui import visuals as WGV
from peter_webgui import settings as Settings
from peter_webgui import rs232 as RS232
from peter_webgui import communicator as Communicator


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

# Values of inputs that live on a page. Each browser tab builds its own widgets, so they write here on change,
# and the settings read from here.
State = {
    'Com_Log_1_Commands': Setting_text("Com_Log_1_Commands", "*IDN?"),
}
Setting_1.Update_from("Com_Log_1_Commands", lambda: State['Com_Log_1_Commands'])

Communicator_1 = Communicator.Communicator(message_out_function=RS232_1.Write_Line,
                                           message_line_in_function=RS232_1.Read_Line,
                                           max_number_of_messages_out=1)
Communicator_1.Start()


# ----------------------------------------------------------------------------------------------------------
# Page contents
# ----------------------------------------------------------------------------------------------------------

def main_page():
    pass


def rs232_page():
    with ui.row():
        RS232_GUI_1 = RS232.RS232_GUI('RS-232 Port', RS232_1)
        Com_Log_1 = Communicator.Communicator_Log_v2('RS-232 Log', Communicator_1, width=1200, height=450,
                                                     default_commands=State['Com_Log_1_Commands'])

        def Commands_changed(text):
            State['Com_Log_1_Commands'] = text
        Com_Log_1.Commands.function_when_changed = Commands_changed


def status_page():
    pass


# (path, button text, builder)
PAGES = [
    ('/',       'Main',   main_page),
    ('/rs232',  'RS-232', rs232_page),
    ('/status', 'Status', status_page),
]


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

def message_in_loop():
    while True:
        Communicator_1.Message_in_worker()
        time.sleep(0.01)


def message_out_loop():
    while True:
        Communicator_1.Message_out_worker()
        time.sleep(0.01)


def main():
    threading.Thread(target=message_in_loop, daemon=True).start()
    threading.Thread(target=message_out_loop, daemon=True).start()
    app.timer(1, Setting_1.Save_if_changed)   # save settings within a second of any change
    app.on_shutdown(Setting_1.Save_if_changed)
    ui.run(title='Delta v1', reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
