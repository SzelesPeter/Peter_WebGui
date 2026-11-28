"""Bus pages of the Delta app (delta_v1.py): I2C, SPI, RS-485, GPIO and CAN.

Each bus is described by a Bus (see the definitions at the end) and gets the same page:
    Config_GUI   card with the port settings: Apply sends them (plus :SYST:ERR?), Read asks the board for them
    Help card    how to type lines into the log
    Bus_Log      Communicator_Log_v2 subclass: one line per transfer in the text box -> SCPI -> one row per transfer
All of them talk to the board with the SCPI commands of docs_legacy/SCPI_Commands.txt over the RS-232 port.

Nothing here runs at import time; delta_v1.py builds the pages and keeps the settings.
"""
import html
import re
import threading
from collections import Counter
from types import SimpleNamespace

from nicegui import ui

from peter_webgui import visuals as WGV
from peter_webgui import timing as Time
from peter_webgui import communicator as Communicator


ERROR_CHECK = ';:SYST:ERR?'   # appended to commands, so the reply line tells whether they worked


# ----------------------------------------------------------------------------------------------------------
# Parsing helpers
# ----------------------------------------------------------------------------------------------------------

def Clean_hex(text, max_bytes = 127, min_bytes = 1):
    """'0A 1B FF', '0x0A,0x1B,0xFF', '0a1bff' -> '0A1BFF'. Raises ValueError for bad digits or a wrong length."""
    parts = re.split(r'[\s,:_]+', text.strip().strip('"\''))
    digits = ''.join(p[2:] if p.lower().startswith('0x') else p for p in parts)
    if not re.fullmatch(r'[0-9A-Fa-f]*', digits):
        raise ValueError(f'not hex data: {text!r}')
    if len(digits) % 2:
        raise ValueError(f'odd number of hex digits: {text!r}')
    if not min_bytes <= len(digits) // 2 <= max_bytes:
        raise ValueError(f'hex data must be {min_bytes}..{max_bytes} bytes: {text!r}')
    return digits.upper()


def Parse_int(text, low, high, what):
    try:
        value = int(text, 0)   # decimal or 0x.. hex
    except (TypeError, ValueError):
        raise ValueError(f'{what} must be a number, not {text!r}')
    if not low <= value <= high:
        raise ValueError(f'{what} must be {low}..{high} ({low:#x}..{high:#x}), not {text}')
    return value


def Parse_choice(text, choices, what):
    """Look text up (any case) in choices, a dict {accepted word: SCPI word}."""
    word = str(text).strip().upper()
    if word not in choices:
        raise ValueError(f'{what} must be one of {", ".join(choices)}, not {text!r}')
    return choices[word]


def Unquote(text):
    text = text.strip()
    return text[1:-1] if len(text) >= 2 and text[0] == text[-1] == '"' else text


def Quote_text(text, max_chars = 255):
    """A <text> parameter: kept as it is if already quoted, otherwise put in double quotes (inner " escaped).
    Escapes like \\r \\n \\xHH are passed through for the board to decode."""
    text = text.strip()
    if not (len(text) >= 2 and text[0] == text[-1] and text[0] in '"\''):
        text = '"' + re.sub(r'(?<!\\)"', r'\\"', text) + '"'
    if len(text) - 2 > max_chars:
        raise ValueError(f'text must be at most {max_chars} characters')
    return text


# ----------------------------------------------------------------------------------------------------------
# Config card
# ----------------------------------------------------------------------------------------------------------

def Field(key, label, kind, options = (), default = ''):
    """One input of a Config_GUI. kind: 'choice' (dropdown), 'edit' (dropdown you can type into) or 'text'."""
    return SimpleNamespace(key=key, label=label, kind=kind, options=list(options), default=default)


def Error_report(ok_text, fail_text):
    """Reply handler for a line that ends in :SYST:ERR?."""
    def handler(reply):
        ok = reply.startswith('0,')
        return None, ok_text if ok else f'{fail_text}: {reply}', not ok
    return handler


def Config_reply(keys, label):
    """Reply handler for a comma separated config reply (e.g. :SPI:CONF?): fills the fields named in keys (None skips)."""
    def handler(reply):
        parts = [p.strip() for p in reply.split(',')]
        if len(parts) != len(keys):
            return None, f'Unexpected {label} reply: {reply}', True
        return {k: v for k, v in zip(keys, parts) if k}, f'{label}: {reply}', False
    return handler


def Field_reply(key):
    """Reply handler that puts the (unquoted) reply into one field."""
    return lambda reply: ({key: Unquote(reply)}, None, False)


def Status_reply(format_text):
    """Reply handler that only shows the reply in the status line, e.g. Status_reply('Buttons: {}')."""
    return lambda reply: (None, format_text.format(reply), False)


class Config_GUI:
    """Port settings card (320 x 450, like RS232_GUI), built from bus.fields.

    Apply     bus.apply(values) -> one SCPI line; sent with :SYST:ERR? so the status line says whether it worked,
              then the settings are read back
    Read      bus.read(values) -> [(SCPI query, reply handler), ...]
    bus.buttons: extra buttons [(name, function(values) -> [(SCPI, reply handler), ...]), ...]
    A reply handler gets the reply text and returns (fields to set or None, status text or None, is error), and may
    add a 4th item: follow-up requests [(SCPI, reply handler), ...] that depend on this reply.

    The inputs' values are kept in state[<prefix>_<field key>].
    """
    def __init__(self, name, communicator, state, prefix, bus, width = 320, height = 450, query_timeout = 1):
        self.communicator = communicator
        self.state = state
        self.prefix = prefix
        self.bus = bus
        self.query_timeout = query_timeout
        self.Widgets = {}
        self.Replies = []                 # (handler, text) from the communicator's worker thread, shown by Update()
        self.Replies_lock = threading.Lock()

        input_width = width - 150         # same layout as RS232_GUI
        button_width = 120

        with WGV.Card(name=name, width=width, height=height):
            for field in bus.fields:
                value = state[f'{prefix}_{field.key}']
                with ui.row():
                    WGV.Create_Label_Right(f'{field.label}:', font_size=20, width=80)
                    if field.kind == 'text':
                        widget = WGV.Text_input(width=input_width, default_text=value)
                        widget.Text_input_element.on_value_change(lambda e, k=field.key: self.Store(k, e.value))
                    else:
                        options = list(field.options)
                        if value not in options:
                            if field.kind == 'edit' and value:
                                options.append(value)
                            else:
                                value = field.default
                        widget = WGV.Create_Dropdown_Card(options=options, function_to_call=lambda v, k=field.key: self.Store(k, v),
                                                          width=input_width, editable=field.kind == 'edit')
                        widget.set_value(value)
                self.Widgets[field.key] = widget

            buttons = [('Apply', self.Apply, WGV.Default_color), ('Read', self.Read, WGV.Default_background_color)]
            buttons += [(text, self.Button_action(function), WGV.Default_background_color) for text, function in bus.buttons]
            for i in range(0, len(buttons), 2):
                with ui.row():
                    for text, action, color in buttons[i:i + 2]:
                        WGV.Button(action, name=text, width=button_width, background_color=color)
            self.L_Status = ui.label('').style(f'color: {WGV.Default_border_color}; font-size: 16px; width: {width - 46}px; word-break: break-all;')

        ui.timer(0.2, self.Update)

    def Button_action(self, function):
        # A plain closure: NiceGUI would pass the click event into a handler that has parameters.
        return lambda: self.Send_requests(function)

    # ---------- values ----------
    def Store(self, key, value):
        self.state[f'{self.prefix}_{key}'] = '' if value is None else str(value)

    def Values(self):
        values = {}
        for key, widget in self.Widgets.items():
            value = widget.Text_input_element.value if isinstance(widget, WGV.Text_input) else widget.value
            values[key] = '' if value is None else str(value).strip()
        return values

    def Set_field(self, key, value):
        widget = self.Widgets.get(key)
        if widget is None:
            return
        if isinstance(widget, WGV.Text_input):
            widget.Text_input_element.value = value
        else:
            if value not in widget.options:
                widget.set_options(widget.options + [value])
            widget.set_value(value)

    def Set_status(self, text, error = False):
        self.L_Status.set_text(text)
        self.L_Status.style(f'color: {WGV.Default_color if error else WGV.Default_border_color};')

    # ---------- requests ----------
    def Query(self, command, handler):
        # Reply callbacks run in the worker thread, so they only queue the text; Update() shows it.
        self.communicator.Message_out_request(message_out=command, callback_function=self.Queue_reply,
                                              callback_args=(handler,), timeout=self.query_timeout)

    def Queue_reply(self, message_in, handler):
        with self.Replies_lock:
            self.Replies.append((handler, message_in.strip()))

    def Apply(self):
        try:
            command = self.bus.apply(self.Values())
        except ValueError as e:
            self.Set_status(str(e), error=True)
            return
        self.Query(command + ERROR_CHECK, Error_report('Applied', 'Apply failed'))
        self.Set_status('Applying...')
        self.Read()

    def Read(self):
        self.Send_requests(self.bus.read)

    def Send_requests(self, function):
        try:
            requests = function(self.Values())
        except ValueError as e:
            self.Set_status(str(e), error=True)
            return
        for command, handler in requests:
            self.Query(command, handler)

    # ---------- replies (GUI thread) ----------
    def Update(self):
        with self.Replies_lock:
            replies, self.Replies = self.Replies, []
        for handler, text in replies:
            fields, status, error, *follow_up = handler(text)
            for key, value in (fields or {}).items():
                self.Set_field(key, value)
            if status is not None:
                self.Set_status(status, error)
            for command, next_handler in (follow_up[0] if follow_up else []):
                self.Query(command, next_handler)


# ----------------------------------------------------------------------------------------------------------
# Log
# ----------------------------------------------------------------------------------------------------------

class Bus_Log(Communicator.Communicator_Log_v2):
    """Communicator_Log_v2 for one bus: one transfer per line in the text box, one row per transfer in the grid.

    A subclass sets
        Columns    grid columns ('Out time', 'Operation', ..., 'Status', 'SCPI')
        Prefixes   SCPI groups shown in the grid besides this widget's own lines, e.g. ('I2C:',)
        Patterns   [(regex on the SCPI command, function(match) -> {column: value}), ...] for Describe
    and Parse(op, args, rest) -> (scpi, is_query) for its line formats (raise ValueError for a bad line).

    Lines starting with ':' or '*' are sent unchanged, lines starting with '#' are comments, and lines starting with
    '$' are instructions for the widget (e.g. $Delay_ms 500, see Communicator.Parse_directive). Commands (not queries) get ;:SYST:ERR? appended, so their
    reply is the board's error report: Status OK for 0,"No error", Error otherwise (the message goes to Data in).
    A failed query sends no reply and ends as Timeout. Lines that cannot be parsed get a Syntax row and are not sent.
    """
    Columns = ['Out time', 'Operation', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Highlight_statuses = ('Timeout', 'Error', 'Syntax')
    Prefixes = ()
    Patterns = []
    Operations = ''   # for the 'unknown operation' message

    def __init__(self, name, communicator, **kwargs):
        self.Own_messages = Counter()   # SCPI lines this widget sent and has not seen in the log yet
        super().__init__(name, communicator, **kwargs)

    # ---------- line -> SCPI ----------
    @classmethod
    def To_SCPI(cls, line):
        """One text-box line -> (scpi, is_query). Raises ValueError with a readable message."""
        if line[0] in ':*':
            return line, line.endswith('?')
        op, _, rest = line.partition(' ')
        return cls.Parse(op.upper(), rest.split(), rest.strip())

    @classmethod
    def Parse(cls, op, args, rest):
        raise ValueError(f'unknown operation {op!r} ({cls.Operations}, or a SCPI line starting with : or *)')

    @staticmethod
    def Need(args, n, usage, exact = False):
        if len(args) < n or (exact and len(args) != n):
            raise ValueError(f'usage: {usage}')

    @classmethod
    def Describe(cls, scpi):
        """SCPI line -> {column: value} for the grid."""
        command = scpi[:-len(ERROR_CHECK)] if scpi.endswith(ERROR_CHECK) else scpi
        for pattern, fields in cls.Patterns:
            m = re.fullmatch(pattern, command, re.IGNORECASE)
            if m:
                return fields(m)
        return {'Operation': command}

    def Describe_reply(self, row):
        """Hook for buses whose replies carry more than data (e.g. CAN frames). Changes row in place."""

    # ---------- sending ----------
    def Send_all(self):
        for line in self.Commands.Get_lines():
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            if line.startswith('$'):
                self.Run_directive(line)   # e.g. $Delay_ms 500, see Communicator.Parse_directive
                continue
            try:
                scpi, is_query = self.To_SCPI(line)
            except ValueError as e:
                self.Add_row({'Out time': Time.Get_Time_text(), 'Operation': line, 'Data in': str(e), 'Status': 'Syntax'})
                continue
            if not is_query:
                scpi += ERROR_CHECK   # turns the command into a query whose reply is the error report
            with self.Log_lock:
                self.Own_messages[scpi] += 1
            self.communicator.Message_out_request(message_out=scpi, timeout=self.query_timeout, message_delay_after=self.message_delay)

    def Add_syntax_row(self, line, message):
        self.Add_row({'Out time': Time.Get_Time_text(), 'Operation': line, 'Data in': message, 'Status': 'Syntax'})

    def Add_row(self, row):
        with self.Log_lock:
            self.Log_rows.append({column: row.get(column, '') for column in self.Columns})
            self.Log_changed = True

    # ---------- log listener (worker thread) ----------
    def Log(self, time_request, time_out, data_out, time_in, data_in, messages_out):
        if data_out == '':
            return   # 'Unexpected' lines can't be matched to a transfer; the RS-232 log shows them
        with self.Log_lock:
            own = self.Own_messages[data_out] > 0
            if own:
                self.Own_messages[data_out] -= 1
        if not own and not data_out.upper().lstrip(':').startswith(self.Prefixes):
            return
        row = self.Describe(data_out)
        if messages_out == 'Timeout!':
            status, data_in = 'Timeout', ''
        elif data_out.endswith(ERROR_CHECK) or data_out.upper().lstrip(':') == 'SYST:ERR?':
            ok = data_in.strip().startswith('0,')
            status = 'OK' if ok else 'Error'
            data_in = '' if ok and data_out.endswith(ERROR_CHECK) else data_in.strip()
        elif data_in != '':
            status, data_in = 'OK', Unquote(data_in)
        else:
            status = 'Sent'
        row.update({'Out time': time_out, 'Response time': time_in, 'Data in': data_in, 'Status': status, 'SCPI': data_out})
        if status == 'OK':
            self.Describe_reply(row)
        self.Add_row(row)


class I2C_Log(Bus_Log):
    Columns = ['Out time', 'Operation', 'Address', 'Register', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Prefixes = ('I2C:',)
    Operations = 'W, R, RW, RR, SCAN, SR'
    Patterns = [
        (r':I2C:WRIT (\S+?),"([^"]*)"',            lambda m: {'Operation': 'Write', 'Address': m[1], 'Data out': m[2]}),
        (r':I2C:READ\? (\S+?),(\d+)',              lambda m: {'Operation': 'Read', 'Address': m[1], 'Data out': f'{m[2]} bytes'}),
        (r':I2C:REG:WRIT (\S+?),(\S+?),"([^"]*)"', lambda m: {'Operation': 'Reg write', 'Address': m[1], 'Register': m[2], 'Data out': m[3]}),
        (r':I2C:REG:READ\? (\S+?),(\S+?),(\d+)',   lambda m: {'Operation': 'Reg read', 'Address': m[1], 'Register': m[2], 'Data out': f'{m[3]} bytes'}),
        (r':I2C:SCAN\?',                           lambda m: {'Operation': 'Scan'}),
        (r':I2C:SLAV:READ\?',                      lambda m: {'Operation': 'Slave read'}),
    ]

    @classmethod
    def Parse(cls, op, args, rest):
        if op in ('W', 'WRITE'):
            cls.Need(args, 2, 'W <addr> <hex>')
            addr = Parse_int(args[0], 0, 0x7F, 'I2C address')
            return f':I2C:WRIT 0x{addr:02X},"{Clean_hex(" ".join(args[1:]))}"', False
        if op in ('R', 'READ'):
            cls.Need(args, 2, 'R <addr> <count>', exact=True)
            addr = Parse_int(args[0], 0, 0x7F, 'I2C address')
            return f':I2C:READ? 0x{addr:02X},{Parse_int(args[1], 1, 128, "Count")}', True
        if op in ('RW', 'REGWRITE'):
            cls.Need(args, 3, 'RW <addr> <reg> <hex>')
            addr = Parse_int(args[0], 0, 0x7F, 'I2C address')
            reg = Parse_int(args[1], 0, 0xFF, 'register')
            return f':I2C:REG:WRIT 0x{addr:02X},0x{reg:02X},"{Clean_hex(" ".join(args[2:]))}"', False
        if op in ('RR', 'REGREAD'):
            cls.Need(args, 3, 'RR <addr> <reg> <count>', exact=True)
            addr = Parse_int(args[0], 0, 0x7F, 'I2C address')
            reg = Parse_int(args[1], 0, 0xFF, 'register')
            return f':I2C:REG:READ? 0x{addr:02X},0x{reg:02X},{Parse_int(args[2], 1, 128, "Count")}', True
        if op == 'SCAN' and not args:
            return ':I2C:SCAN?', True
        if op in ('SR', 'SLAVEREAD') and not args:
            return ':I2C:SLAV:READ?', True
        return super().Parse(op, args, rest)


class SPI_Log(Bus_Log):
    Columns = ['Out time', 'Operation', 'CS', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Prefixes = ('SPI:',)
    Operations = 'T, POL, SR'
    Patterns = [
        (r':SPI:TRAN\? (\d+),"([^"]*)"',   lambda m: {'Operation': 'Transfer', 'CS': m[1], 'Data out': m[2]}),
        (r':SPI:CS:POL (\d+),(\w+)',       lambda m: {'Operation': 'CS polarity', 'CS': m[1], 'Data out': m[2]}),
        (r':SPI:SLAV:READ\?',              lambda m: {'Operation': 'Slave read'}),
    ]

    @classmethod
    def Parse(cls, op, args, rest):
        if op in ('T', 'TRANSFER'):
            cls.Need(args, 2, 'T <cs> <hex>')
            cs = Parse_int(args[0], 0, 6, 'Chip select')
            return f':SPI:TRAN? {cs},"{Clean_hex(" ".join(args[1:]))}"', True
        if op in ('POL', 'POLARITY'):
            cls.Need(args, 2, 'POL <cs> LOW|HIGH', exact=True)
            cs = Parse_int(args[0], 1, 6, 'Chip select')
            return f':SPI:CS:POL {cs},{Parse_choice(args[1], {"LOW": "LOW", "HIGH": "HIGH"}, "Polarity")}', False
        if op in ('SR', 'SLAVEREAD') and not args:
            return ':SPI:SLAV:READ?', True
        return super().Parse(op, args, rest)


class RS485_Log(Bus_Log):
    Columns = ['Out time', 'Operation', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Prefixes = ('RS485:',)
    Operations = 'W, WH, R, C, CLR'
    Patterns = [
        (r':RS485:WRIT "(.*)"',  lambda m: {'Operation': 'Write', 'Data out': m[1]}),
        (r':RS485:READ\?',       lambda m: {'Operation': 'Read'}),
        (r':RS485:COUN\?',       lambda m: {'Operation': 'Count'}),
        (r':RS485:CLE',          lambda m: {'Operation': 'Clear RX'}),
    ]

    @classmethod
    def Parse(cls, op, args, rest):
        if op in ('W', 'WRITE'):
            if not rest:
                raise ValueError('usage: W <text>')
            return f':RS485:WRIT {Quote_text(rest)}', False
        if op in ('WH', 'WRITEHEX'):
            cls.Need(args, 1, 'WH <hex>')
            data = Clean_hex(' '.join(args), max_bytes=63)   # each byte becomes \xHH (4 characters, at most 255)
            return ':RS485:WRIT "' + ''.join(f'\\x{data[i:i + 2]}' for i in range(0, len(data), 2)) + '"', False
        if op in ('R', 'READ') and not args:
            return ':RS485:READ?', True
        if op in ('C', 'COUNT') and not args:
            return ':RS485:COUN?', True
        if op in ('CLR', 'CLEAR') and not args:
            return ':RS485:CLE', False
        return super().Parse(op, args, rest)


IO_MODES = {'IN': 'INP', 'INPUT': 'INP', 'OUT': 'OUTP', 'OUTPUT': 'OUTP', 'AN': 'ANAL', 'ANALOG': 'ANAL'}
IO_PULLS = {'NONE': 'NONE', 'UP': 'UP', 'DOWN': 'DOWN'}
IO_LEVELS = {'0': '0', '1': '1', 'LOW': '0', 'HIGH': '1', 'OFF': '0', 'ON': '1'}


class GPIO_Log(Bus_Log):
    Columns = ['Out time', 'Operation', 'Pin', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Prefixes = ('IO:', 'BUTT:')
    Operations = 'MODE, PULL, W, R, A, V, MQ, B, BALL'
    Patterns = [
        (r':IO:MODE (\d+),(\w+)',   lambda m: {'Operation': 'Mode', 'Pin': f'IO_{m[1]}', 'Data out': m[2]}),
        (r':IO:PULL (\d+),(\w+)',   lambda m: {'Operation': 'Pull', 'Pin': f'IO_{m[1]}', 'Data out': m[2]}),
        (r':IO:WRIT (\d+),(\w+)',   lambda m: {'Operation': 'Write', 'Pin': f'IO_{m[1]}', 'Data out': m[2]}),
        (r':IO:READ\? (\d+)',       lambda m: {'Operation': 'Read', 'Pin': f'IO_{m[1]}'}),
        (r':IO:ANAL\? (\d+)',       lambda m: {'Operation': 'Analog (raw)', 'Pin': f'IO_{m[1]}'}),
        (r':IO:VOLT\? (\d+)',       lambda m: {'Operation': 'Voltage', 'Pin': f'IO_{m[1]}'}),
        (r':IO:MODE\? (\d+)',       lambda m: {'Operation': 'Mode?', 'Pin': f'IO_{m[1]}'}),
        (r':BUTT:READ\? (\d+)',     lambda m: {'Operation': 'Button', 'Pin': f'BUTTON{m[1]}'}),
        (r':BUTT:ALL\?',            lambda m: {'Operation': 'All buttons', 'Pin': 'BUTTON1..5'}),
    ]

    @classmethod
    def Parse(cls, op, args, rest):
        if op == 'MODE':
            cls.Need(args, 2, 'MODE <n> IN|OUT|ANALOG', exact=True)
            return f':IO:MODE {Parse_int(args[0], 1, 8, "Pin")},{Parse_choice(args[1], IO_MODES, "Mode")}', False
        if op == 'PULL':
            cls.Need(args, 2, 'PULL <n> NONE|UP|DOWN', exact=True)
            return f':IO:PULL {Parse_int(args[0], 1, 8, "Pin")},{Parse_choice(args[1], IO_PULLS, "Pull")}', False
        if op in ('W', 'WRITE'):
            cls.Need(args, 2, 'W <n> 0|1', exact=True)
            return f':IO:WRIT {Parse_int(args[0], 1, 8, "Pin")},{Parse_choice(args[1], IO_LEVELS, "Level")}', False
        if op in ('R', 'READ'):
            cls.Need(args, 1, 'R <n>', exact=True)
            return f':IO:READ? {Parse_int(args[0], 1, 8, "Pin")}', True
        if op in ('A', 'ANALOG'):
            cls.Need(args, 1, 'A <n>', exact=True)
            return f':IO:ANAL? {Parse_int(args[0], 1, 4, "Analog pin")}', True
        if op in ('V', 'VOLT', 'VOLTAGE'):
            cls.Need(args, 1, 'V <n>', exact=True)
            return f':IO:VOLT? {Parse_int(args[0], 1, 4, "Analog pin")}', True
        if op == 'MQ':
            cls.Need(args, 1, 'MQ <n>', exact=True)
            return f':IO:MODE? {Parse_int(args[0], 1, 8, "Pin")}', True
        if op in ('B', 'BUTTON'):
            cls.Need(args, 1, 'B <n>', exact=True)
            return f':BUTT:READ? {Parse_int(args[0], 1, 5, "Button")}', True
        if op == 'BALL' and not args:
            return ':BUTT:ALL?', True
        return super().Parse(op, args, rest)


class CAN_Log(Bus_Log):
    Columns = ['Out time', 'Operation', 'ID', 'Data out', 'Response time', 'Data in', 'Status', 'SCPI']
    Prefixes = ('CAN:',)
    Operations = 'W, R, C'
    Patterns = [
        (r':CAN:WRIT (\S+?),"([^"]*)"',  lambda m: {'Operation': 'Write', 'ID': m[1], 'Data out': m[2]}),
        (r':CAN:READ\?',                 lambda m: {'Operation': 'Read'}),
        (r':CAN:COUN\?',                 lambda m: {'Operation': 'Count'}),
    ]

    @classmethod
    def Parse(cls, op, args, rest):
        if op in ('W', 'WRITE'):
            cls.Need(args, 1, 'W <id> [hex]')
            frame_id = Parse_int(args[0], 0, 0x1FFFFFFF, 'CAN id')
            data = Clean_hex(' '.join(args[1:]), max_bytes=8, min_bytes=0)
            return f':CAN:WRIT 0x{frame_id:X},"{data}"', False
        if op in ('R', 'READ') and not args:
            return ':CAN:READ?', True
        if op in ('C', 'COUNT') and not args:
            return ':CAN:COUN?', True
        return super().Parse(op, args, rest)

    def Describe_reply(self, row):
        # :CAN:READ? -> STD,0x123,"DEADBEEF" | EXT,0x1ABCDE,"" | STD,0x7,RTR | NONE
        m = re.fullmatch(r'(STD|EXT),(\S+?),(.*)', row['Data in'])
        if m and row.get('Operation') == 'Read':
            row.update({'Operation': f'Read {m[1]}', 'ID': m[2], 'Data in': Unquote(m[3])})


# ----------------------------------------------------------------------------------------------------------
# Help card
# ----------------------------------------------------------------------------------------------------------

def Help_html(bus):
    rows = []
    for line_format, description, example in bus.help_rows:
        cells = f'<td>{html.escape(line_format)}</td>'
        if example:
            cells += f'<td>{html.escape(description)}</td><td>{html.escape(example)}</td>'
        else:
            cells += f'<td colspan="2">{html.escape(description)}</td>'
        rows.append(f'<tr>{cells}</tr>')
    return f'''
<p>Type one {bus.item} per line in the box on the left of the {bus.title} Log, then press <b>Send all</b>.
<code>#</code> starts a comment, <code>:</code> or <code>*</code> lines are sent unchanged, and <code>$</code> lines
are not sent: <code>$Delay_ms 500</code> waits 500 ms before the next line.</p>
<table>{''.join(rows)}</table>
<p>{bus.help_notes}</p>
<p><b>Status</b><br>
OK: done.<br>
Error: the board reported a problem, see Data in.<br>
Timeout: a query got no reply, send <code>:SYST:ERR?</code> to see why.<br>
Syntax: the line could not be read, so it was not sent.</p>
<p><b>Delay [ms]</b> pauses after every line, <code>$Delay_ms</code> only where you put it. Load or save the lines
with <b>{bus.title} Data Files</b>.</p>
'''


RS232_LOG_HELP = '''
<p>Type one SCPI line per line in the box on the left of the RS-232 Log, then press <b>Send all</b>.
Each line goes to the board exactly as typed. The commands are listed in <code>docs_legacy/SCPI_Commands.txt</code>.</p>
<table>
<tr><td>... ?</td><td>a query: waits for one reply</td><td>*IDN?</td></tr>
<tr><td>...</td><td>a command: no reply expected</td><td>:IO:WRIT 5,1</td></tr>
<tr><td>...;...</td><td>up to 8 commands in one line</td><td>:RS485:BAUD 9600;PAR EVEN</td></tr>
<tr><td># ...</td><td colspan="2">a comment, not sent</td></tr>
<tr><td>$Delay_ms &lt;ms&gt;</td><td>wait before the next line</td><td>$Delay_ms 500</td></tr>
</table>
<p>A failed command sends nothing back: end the line with <code>;:SYST:ERR?</code> to get the result as the reply.
The log shows all traffic on the port, including what the other pages send.</p>
<p><b>Status</b><br>
OK: the reply arrived. Sent: a command, no reply expected.<br>
Timeout: a query got no reply, send <code>:SYST:ERR?</code> to see why.<br>
Unexpected: the board sent a line nobody asked for.<br>
Syntax: a <code>$</code> line could not be read, nothing was sent.</p>
<p><b>Delay [ms]</b> pauses after every line, <code>$Delay_ms</code> only where you put it. Load or save the lines
with <b>Command Files</b>.</p>
'''


def Help_card(title, help_html, width = 640, height = 450, padding = 20, border_width = 3):
    """Card with help text (HTML; first table column and <code> in monospace). 450 high, like the port cards."""
    inner_width = width - 2 * (padding + border_width)
    with WGV.Card(name=title, width=width, height=height, padding=padding, border_width=border_width):
        ui.html(help_html).classes('wgv-help').style(f'''
            color: {WGV.Default_border_color}; font-size: 14px; line-height: 1.5;
            width: {WGV.Number_to_Pixel(inner_width)}; max-width: {WGV.Number_to_Pixel(inner_width)}; overflow-wrap: anywhere;
            --code: 'DejaVu Sans Mono', 'Consolas', monospace;''')
    ui.add_css('''
        .wgv-help table { width: 100%; border-collapse: collapse; margin: 6px 0; }
        .wgv-help td { padding: 1px 12px 1px 0; vertical-align: top; }
        .wgv-help td:first-child { white-space: nowrap; }
        .wgv-help td:first-child, .wgv-help td:last-child, .wgv-help code { font-family: var(--code); }
        .wgv-help td[colspan] { font-family: inherit; }   /* descriptions spanning two columns are plain text */
        .wgv-help p { margin: 4px 0; }
    ''')


def Default_commands(bus):
    """Starting text of the log's command box: the line formats as comments, then bus.example."""
    width = max(len(f) for f, _, _ in bus.help_rows)
    lines = [f'# One {bus.item} per line (# starts a comment):']
    lines += [f'# {f.ljust(width)}  {d}' for f, d, _ in bus.help_rows]
    lines += [f'# {"$Delay_ms <ms>".ljust(width)}  wait before the next line']
    return '\n'.join(lines) + '\n' + bus.example + '\n'


# ----------------------------------------------------------------------------------------------------------
# Bus definitions
# ----------------------------------------------------------------------------------------------------------

ROLES = {'MASTER': 'MAST', 'SLAVE': 'SLAV'}


def _i2c_apply(v):
    frequency = Parse_int(v['Frequency'], 10000, 400000, 'Frequency')
    address = Parse_int(v['Address'], 0x08, 0x77, 'Own address')
    reply = Clean_hex(v['Reply'])
    return (f':I2C:FREQ {frequency};:I2C:ROLE {Parse_choice(v["Role"], ROLES, "Role")};'
            f':I2C:ADDR 0x{address:02X};:I2C:SLAV:REPL "{reply}"')


def _i2c_scan(reply):
    return None, 'No devices found' if reply == 'NONE' else f'Devices: {reply}', False


def _spi_apply(v):
    frequency = Parse_int(v['Frequency'], 218750, 28000000, 'Frequency')
    reply = Clean_hex(v['Reply'])
    return (f':SPI:FREQ {frequency};:SPI:MODE {Parse_choice(v["Mode"], {m: m for m in "0123"}, "Mode")};'
            f':SPI:ORD {Parse_choice(v["Order"], {"MSB": "MSB", "LSB": "LSB"}, "Order")};'
            f':SPI:ROLE {Parse_choice(v["Role"], ROLES, "Role")};:SPI:SLAV:REPL "{reply}"')


PARITIES = {'NONE': 'NONE', 'EVEN': 'EVEN', 'ODD': 'ODD'}


def _rs485_apply(v):
    baud = Parse_int(v['Baud'], 300, 1750000, 'Baud')
    return (f':RS485:BAUD {baud};:RS485:PAR {Parse_choice(v["Parity"], PARITIES, "Parity")};'
            f':RS485:STOP {Parse_choice(v["Stop"], {"1": "1", "2": "2"}, "Stop bits")}')


GPIO_MODES = {'INPUT': 'INP', 'OUTPUT': 'OUTP', 'ANALOG': 'ANAL'}


def _gpio_apply(v):
    pin = Parse_int(v['Pin'], 1, 8, 'Pin')
    # Pull first, so a pin that becomes an input gets its pull resistor straight away
    return f':IO:PULL {pin},{Parse_choice(v["Pull"], IO_PULLS, "Pull")};:IO:MODE {pin},{Parse_choice(v["Mode"], GPIO_MODES, "Mode")}'


def _gpio_level(v):
    """Level button: ask the board for the pin's mode first, then read volts (ANALOG) or the logic level (0/1)."""
    pin = Parse_int(v['Pin'], 1, 8, 'Pin')

    def mode_reply(mode):
        if mode == 'ANALOG':
            return ({'Mode': mode}, f'IO_{pin}: reading voltage...', False,
                    [(f':IO:VOLT? {pin}', Status_reply(f'IO_{pin} (ANALOG): {{}} V'))])
        return ({'Mode': mode}, f'IO_{pin}: reading level...', False,
                [(f':IO:READ? {pin}', Status_reply(f'IO_{pin} ({mode}) level: {{}}'))])
    return [(f':IO:MODE? {pin}', mode_reply)]


def _gpio_read(v):
    pin = Parse_int(v['Pin'], 1, 8, 'Pin')
    return [(f':IO:MODE? {pin}', lambda reply: ({'Mode': reply}, f'IO_{pin} mode: {reply} (pull can not be read back)', False))]


CAN_MODES = {'NORMAL': 'NORM', 'LOOPBACK': 'LOOP', 'SILENT': 'SIL'}


def _can_apply(v):
    bitrate = Parse_int(v['Bitrate'], 10000, 1000000, 'Bitrate')
    # Switch off while changing the bit rate and mode, then on or off as chosen
    return (f':CAN:ENAB OFF;:CAN:BITR {bitrate};:CAN:MODE {Parse_choice(v["Mode"], CAN_MODES, "Mode")};'
            f':CAN:ENAB {Parse_choice(v["Enable"], {"ON": "ON", "OFF": "OFF"}, "Enable")}')


BUSES = {
    'I2C': SimpleNamespace(
        key='I2C', title='I2C', path='/i2c', port_title='I2C Port', item='transfer', log_class=I2C_Log,
        fields=[Field('Frequency', 'Freq', 'edit', ['10000', '50000', '100000', '400000'], '100000'),
                Field('Role', 'Role', 'choice', ['MASTER', 'SLAVE'], 'MASTER'),
                Field('Address', 'Address', 'text', default='0x42'),
                Field('Reply', 'Reply', 'text', default='FF')],
        apply=_i2c_apply,
        read=lambda v: [(':I2C:CONF?', Config_reply(['Frequency', 'Role', 'Address'], 'Config')),
                        (':I2C:SLAV:REPL?', Field_reply('Reply'))],
        buttons=[('Scan', lambda v: [(':I2C:SCAN?', _i2c_scan)])],
        help_rows=[('W  <addr> <hex>', 'write bytes', 'W 0x50 00 10 FF'),
                   ('R  <addr> <count>', 'read bytes', 'R 0x50 2'),
                   ('RW <addr> <reg> <hex>', 'register write', 'RW 0x3C 0x00 AF'),
                   ('RR <addr> <reg> <count>', 'register read', 'RR 0x68 0x75 1'),
                   ('SCAN  /  SR', 'list the devices on the bus / read the slave buffer', None)],
        help_notes='Numbers are decimal or 0x hex. Data is hex bytes, spaces allowed, at most 127 bytes per line. '
                   'Address and Reply on the port card are used in the SLAVE role.',
        example='SCAN', data_file='i2c_data.txt', log_file='i2c_log.csv'),

    'SPI': SimpleNamespace(
        key='SPI', title='SPI', path='/spi', port_title='SPI Port', item='transfer', log_class=SPI_Log,
        fields=[Field('Frequency', 'Freq', 'edit', ['28000000', '14000000', '7000000', '3500000', '1750000',
                                                    '875000', '437500', '218750'], '14000000'),
                Field('Mode', 'Mode', 'choice', ['0', '1', '2', '3'], '0'),
                Field('Order', 'Order', 'choice', ['MSB', 'LSB'], 'MSB'),
                Field('Role', 'Role', 'choice', ['MASTER', 'SLAVE'], 'MASTER'),
                Field('Reply', 'Reply', 'text', default='FF')],
        apply=_spi_apply,
        read=lambda v: [(':SPI:CONF?', Config_reply(['Frequency', 'Mode', 'Order', 'Role'], 'Config')),
                        (':SPI:SLAV:REPL?', Field_reply('Reply'))],
        buttons=[],
        help_rows=[('T   <cs> <hex>', 'transfer (send + receive)', 'T 2 9F 00 00 00'),
                   ('POL <cs> LOW|HIGH', 'chip select active level', 'POL 1 HIGH'),
                   ('SR', 'read the bytes received in the SLAVE role', None)],
        help_notes='&lt;cs&gt; is the chip select 1..6, or 0 for none. Data is hex bytes, spaces allowed, at most '
                   '127 bytes per line; the reply has as many bytes as were sent. The board uses the fastest clock '
                   'that is not above Freq: Read shows the real one.',
        example='T 0 9F 00 00 00', data_file='spi_data.txt', log_file='spi_log.csv'),

    'RS485': SimpleNamespace(
        key='RS485', title='RS-485', path='/rs485', port_title='RS-485 Port', item='message', log_class=RS485_Log,
        fields=[Field('Baud', 'Baud', 'edit', ['9600', '19200', '38400', '57600', '115200', '230400', '460800',
                                               '921600'], '115200'),
                Field('Parity', 'Parity', 'choice', ['NONE', 'EVEN', 'ODD'], 'NONE'),
                Field('Stop', 'Stop', 'choice', ['1', '2'], '1')],
        apply=_rs485_apply,
        read=lambda v: [(':RS485:CONF?', Config_reply(['Baud', 'Parity', 'Stop'], 'Config'))],
        buttons=[('Clear RX', lambda v: [(':RS485:CLE' + ERROR_CHECK, Error_report('Receive buffer cleared', 'Clear failed'))]),
                 ('RX count', lambda v: [(':RS485:COUN?', Status_reply('{} bytes waiting'))])],
        help_rows=[('W  <text>', 'send text', r'W AT\r\n'),
                   ('WH <hex>', 'send bytes', 'WH 01 03 00 00 00 01 84 0A'),
                   ('R', 'read what was received', None),
                   ('C  /  CLR', 'bytes waiting / empty the receive buffer', None)],
        help_notes=r'Text can use \r \n \t \\ \" and \xHH escapes, at most 255 characters. WH sends at most 63 '
                   r'bytes. Received bytes that are not printable come back as \xHH.',
        example=r'W Hello\r\n', data_file='rs485_data.txt', log_file='rs485_log.csv'),

    'GPIO': SimpleNamespace(
        key='GPIO', title='GPIO', path='/gpio', port_title='GPIO Pins', item='command', log_class=GPIO_Log,
        fields=[Field('Pin', 'Pin', 'choice', [str(n) for n in range(1, 9)], '1'),
                Field('Mode', 'Mode', 'choice', ['INPUT', 'OUTPUT', 'ANALOG'], 'INPUT'),
                Field('Pull', 'Pull', 'choice', ['NONE', 'UP', 'DOWN'], 'NONE')],
        apply=_gpio_apply,
        read=_gpio_read,
        buttons=[('Level', _gpio_level),
                 ('Buttons', lambda v: [(':BUTT:ALL?', Status_reply('BUTTON1..5: {}'))])],
        help_rows=[('MODE <n> IN|OUT|ANALOG', 'pin mode', 'MODE 5 OUT'),
                   ('PULL <n> NONE|UP|DOWN', 'pull resistor', 'PULL 6 UP'),
                   ('W <n> 0|1   R <n>', 'set an output / read a pin', 'W 5 1'),
                   ('A <n>   V <n>', 'analog: raw 0..4095 / volts', 'V 1'),
                   ('MQ <n>', 'read the pin mode', 'MQ 5'),
                   ('B <n>   BALL', 'read one button / all five', 'BALL')],
        help_notes='Pins are IO_1..IO_8 (&lt;n&gt; 1..8); only IO_1..IO_4 can be ANALOG. Buttons are 1..5 and read '
                   '1 when released. Pin voltages must stay within 0..3.3 V.',
        example='BALL', data_file='gpio_data.txt', log_file='gpio_log.csv'),

    'CAN': SimpleNamespace(
        key='CAN', title='CAN', path='/can', port_title='CAN Port', item='frame', log_class=CAN_Log,
        fields=[Field('Bitrate', 'Bitrate', 'edit', ['10000', '20000', '50000', '100000', '125000', '250000',
                                                     '500000', '1000000'], '500000'),
                Field('Mode', 'Mode', 'choice', ['NORMAL', 'LOOPBACK', 'SILENT'], 'NORMAL'),
                Field('Enable', 'Enable', 'choice', ['ON', 'OFF'], 'OFF')],
        apply=_can_apply,
        read=lambda v: [(':CAN:CONF?', Config_reply(['Bitrate', 'Mode', 'Enable'], 'Config'))],
        buttons=[('RX count', lambda v: [(':CAN:COUN?', Status_reply('{} frames waiting'))])],
        help_rows=[('W <id> [hex]', 'send a data frame', 'W 0x123 DE AD BE EF'),
                   ('R', 'read the oldest received frame', None),
                   ('C', 'frames waiting', None)],
        help_notes='IDs up to 0x7FF are sent as standard (11-bit) frames, bigger ones as extended (29-bit). Data is '
                   '0..8 hex bytes. CAN must be enabled (Enable ON, Apply) to send; LOOPBACK receives your own '
                   'frames without a bus. A frame nobody acknowledges gives error 502.',
        example='C', data_file='can_data.txt', log_file='can_log.csv'),
}
