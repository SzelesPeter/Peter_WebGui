"""Instrument-level widgets shared by the instrument apps.

Error_Log          grid of the errors an instrument driver collected in Instrument.ERROR
Instrument_Finder  card that scans the serial ports for an instrument (*IDN?) and connects to it
Numeric_Display    bench-meter style readout: big reading with SI prefix and unit, title and info line

`python -m peter_webgui.instrument_visuals` shows a Numeric_Display demo on port 8082.
"""
import asyncio
import math
import threading

from nicegui import ui, run

from peter_webgui import visuals as WGV
from peter_webgui import timing as Time
from peter_webgui import trace_manager as TM
from peter_webgui import rs232 as RS232
from peter_webgui import communicator as Communicator


class Error_Log:
    """Grid of instrument errors: Time, Number, Description.

    Instrument.ERROR is a list of [number, description] entries that a driver (or anything else) appends to.
    Update(), run from a ui.timer, moves them into the grid, oldest first.
    """
    def __init__(self, name, Instrument, width = 1840, height = 400):
        self.Instrument = Instrument
        self.Error_Data = TM.General_Data([
                            'Time',
                            'Number',
                            'Description',
        ])
        with WGV.Card(name= name, width= width, height= height):
            grid_width = width - 40
            # Time and Number are short; Description gets the rest of the width.
            self.G_Log = WGV.Grid(data=self.Error_Data.df, width= grid_width, height= height - 46,
                                  column_width={'Time': 190, 'Number': 120, 'Description': grid_width - 190 - 120 - 4})

    def Update(self):
        if len(self.Instrument.ERROR) != 0:
            for i in range(len(self.Instrument.ERROR)):
                ERROR = self.Instrument.ERROR.pop(0)   # oldest first
                # Number as text: it can also be a word like 'Timeout', which a number column would show as invalid
                self.Error_Data.Add_measurement_point([Time.Get_Time_text(), str(ERROR[0]), ERROR[1]])
            self.G_Log.Grid_element.options['rowData'] = self.Error_Data.df.to_dict('records')
            self.G_Log.Grid_element.update()
            self.G_Log.Grid_element.run_grid_method(
            'ensureIndexVisible',
            len(self.G_Log.Grid_element.options['rowData']) - 1,
            'bottom'
            )

async def Find_and_connect(RS232, Instrument, Communicator = None, No = None, RS232_GUI = None):
    """Scan the serial ports for Instrument.Vendor / .Model (and serial number No, if given) and connect to it.

    The Communicator is stopped while scanning and started again in every case. When the instrument is found the
    port is opened (through RS232_GUI if given, so its dropdown follows); otherwise the previous port is set back.
    Returns (port, *IDN? fields) or (None, None). Instrument_Finder's Find buttons run this; an app can also call it
    on its own, e.g. at start-up.
    """
    if Communicator != None:
        Communicator.Stop()
    if RS232_GUI != None:
        RS232_GUI.B_Disconnect_Function()
    previous_port = RS232.Get_Port()
    started = False
    try:
        COM, IDE = await run.io_bound(RS232.Find_IDE, Instrument.Vendor, Instrument.Model, No)
        if COM:
            # Start first: Start() empties the queues, so a message queued when the port opens must come after it.
            if Communicator != None:
                Communicator.Start()
                started = True
            if RS232_GUI != None:
                RS232_GUI.DDC_Port_Function(COM)
                RS232_GUI.B_Connect_Function()
            else:
                RS232.Set_Port(COM)
                RS232.Open()
        else:
            RS232.Set_Port(previous_port)
        return COM, IDE
    except Exception:
        RS232.Set_Port(previous_port)
        raise
    finally:
        # Start again in every case, so a failed search doesn't leave the communicator stopped.
        if Communicator != None and not started:
            Communicator.Start()


class Instrument_Finder:
    """Card that scans every serial port with *IDN? for Instrument.Vendor / Instrument.Model and connects to it.

    "Find" takes the first match, "Find No." also needs the serial number (3rd *IDN? field) to match.
    Instrument is anything with .Vendor and .Model (a driver, or e.g. types.SimpleNamespace(Vendor=..., Model=...)).
    While searching, the Communicator is stopped. When the instrument is found, the port is opened (through
    RS232_GUI if one is given, so its dropdown follows); otherwise the previous port is set back.
    """
    def __init__(self,name: str, RS232: RS232.RS232, Instrument, Communicator: Communicator.Communicator = None, Default_No: int = 0, RS232_GUI: RS232.RS232_GUI = None, width = 310, height = 300):
        self.RS232 = RS232
        self.Instrument = Instrument
        self.Communicator = Communicator
        self.RS232_GUI = RS232_GUI
        with WGV.Card(name= name, width= width, height= height):
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
        try:
            COM, IDE = await Find_and_connect(self.RS232, self.Instrument, self.Communicator, No, self.RS232_GUI)
        except Exception as e:
            self.Lport2.set_text('Error')
            print(f'Instrument search failed: {e}')
            return
        self.Show_result(COM, IDE)

    def Show_result(self, COM, IDE):
        """Show a search result in the card, e.g. one found before the page was opened."""
        self.Lport2.set_text(COM if COM else 'Not found')
        self.Lno2.set_text(IDE[2] if COM else '')

    def Get_No(self):
        return self.NI_No.Number_input_element.value


SI_prefixes = {-12: 'p', -9: 'n', -6: 'µ', -3: 'm', 0: '', 3: 'k', 6: 'M', 9: 'G', 12: 'T'}


def Format_reading(value, digits = 7, si_prefix = True):
    """Number -> (reading text, SI prefix), like a bench meter: fixed number of digits, sign always shown.

        Format_reading(0.0012345678)        -> ('+1.234568', 'm')
        Format_reading(-12345.6, digits=5)  -> ('-12.346', 'k')
        Format_reading(0.0012345678, si_prefix=False) -> ('+1.234568E-03', '')
    """
    if not si_prefix:
        return f'{value:+.{digits - 1}E}', ''
    exponent = 0 if value == 0 else max(-12, min(12, math.floor(math.log10(abs(value)) / 3) * 3))
    for _ in range(2):   # a second pass when rounding gives 1000.0 (e.g. 999.9999 -> 1.000000 k)
        mantissa = value / 10 ** exponent
        integer_digits = len(str(int(abs(mantissa)))) if abs(mantissa) >= 1 else 1
        text = f'{mantissa:+.{max(digits - integer_digits, 0)}f}'
        if abs(float(text)) < 1000 or exponent >= 12:
            break
        exponent += 3
    return text, SI_prefixes[exponent]


class Numeric_Display:
    """Bench-meter readout: a title, a big reading with its unit, and a small info line (range, mode, ...).

        D = IV.Numeric_Display('HP 34401A', unit='V', info='DC  Range 10 V')
        D.Set_value(0.0012345678)        # shows +1.234568 mV
        D.Set_value('+9.90000000E+37')   # driver reply strings work too; this one is the overload value -> OVLD
        D.Set_info('AC  Range 1 V')

    Set_value / Set_unit / Set_info may be called from any thread (e.g. a Communicator callback): they only store the
    value, and the widget's own ui.timer draws it.

    digits:     significant digits shown (the meter's resolution).
    si_prefix:  True scales the reading into p/n/µ/m/k/M/G/T + unit, False shows it in E notation.
    overload:   readings with an absolute value at least this large show 'OVLD' (34401A/34970A send 9.9E+37).
    A value that is None, NaN, or text that is not a number shows dashes.
    """
    def __init__(self, name = None, unit = '', info = '', digits = 7, si_prefix = True, overload = 9.9e37,
                 width = 640, height = 200, color = WGV.Default_border_color, background_color = WGV.Default_page_color,
                 border_color = WGV.Default_border_color, padding = 20, border_width = 3, update_interval = 0.1):
        self.digits = digits
        self.si_prefix = si_prefix
        self.overload = overload
        self.Value = None
        self.Unit = unit
        self.Info = info
        self.Lock = threading.Lock()
        self.Changed = True

        inner_width = width - 2 * (padding + border_width)
        inner_height = height - 2 * (padding + border_width)
        info_height = 24
        reading_height = inner_height - info_height
        reading_font = int(reading_height * 0.7)
        unit_font = int(reading_font * 0.5)

        self.Card = WGV.Card(name=name, width=width, height=height, background_color=background_color,
                             border_color=border_color, padding=padding, border_width=border_width)
        with self.Card:
            with ui.column().style('gap: 0;'):
                with ui.row().classes('no-wrap items-baseline justify-end').style(f'width: {WGV.Number_to_Pixel(inner_width)}; '
                                                                                f'height: {WGV.Number_to_Pixel(reading_height)}; gap: 12px;'):
                    self.Reading_label = ui.label('').style(f"""
                        color: {color}; font-family: 'DejaVu Sans Mono', 'Consolas', monospace; font-weight: bold;
                        font-size: {WGV.Number_to_Pixel(reading_font)}; line-height: {WGV.Number_to_Pixel(reading_height)};
                        white-space: pre;""")
                    self.Unit_label = ui.label('').style(f"""
                        color: {color}; font-weight: bold; font-size: {WGV.Number_to_Pixel(unit_font)};
                        min-width: {WGV.Number_to_Pixel(unit_font * 2)};""")
                self.Info_label = ui.label('').style(f"""
                    color: {color}; font-size: 16px; height: {WGV.Number_to_Pixel(info_height)};
                    width: {WGV.Number_to_Pixel(inner_width)}; text-align: right; opacity: 0.8;""")

        self.Update()
        ui.timer(update_interval, self.Update)

    # ---------- setters (any thread) ----------
    def Set_value(self, value, unit = None):
        with self.Lock:
            self.Value = value
            if unit is not None:
                self.Unit = unit
            self.Changed = True

    def Set_unit(self, unit):
        with self.Lock:
            self.Unit = unit
            self.Changed = True

    def Set_info(self, info):
        with self.Lock:
            self.Info = info
            self.Changed = True

    def Get_value(self):
        """The last value as a float, or None if it is missing or not a number."""
        try:
            value = float(self.Value)
        except (TypeError, ValueError):
            return None
        return None if math.isnan(value) else value

    # ---------- drawing (GUI thread) ----------
    def Text(self):
        """(reading, unit) as the display shows them."""
        value = self.Get_value()
        if value is None:
            return '-' * (self.digits + 1), self.Unit
        if abs(value) >= self.overload:
            return 'OVLD', self.Unit
        reading, prefix = Format_reading(value, self.digits, self.si_prefix)
        return reading, prefix + self.Unit

    def Update(self):
        with self.Lock:
            if not self.Changed:
                return
            self.Changed = False
        reading, unit = self.Text()
        self.Reading_label.set_text(reading)
        self.Unit_label.set_text(unit)
        self.Info_label.set_text(self.Info)


if __name__ in {"__main__", "__mp_main__"}:
    import random

    @WGV.Page('/', title='Numeric_Display demo', layout='column')
    def main_page():
        D1 = Numeric_Display('Voltage', unit='V', info='DC  Range 10 V  (random walk)')
        D2 = Numeric_Display('Resistance', unit='Ω', info='4W  Range 100 kΩ', digits=5, width=480, height=150)
        D3 = Numeric_Display('Overload', unit='V', width=480, height=150)
        D3.Set_value('+9.90000000E+37')
        state = {'v': 0.0012345678}

        def Step():
            state['v'] *= 10 ** random.uniform(-0.3, 0.3) * random.choice((1, 1, 1, -1))
            D1.Set_value(state['v'])
            D2.Set_value(abs(state['v']) * 1e7)
        ui.timer(0.5, Step)

    ui.run(port=8082, reload=False, show=False)
