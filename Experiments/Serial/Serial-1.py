#Imports for Serial communication to work:
import serial
from serial.tools.list_ports import comports
#Imports for the GUI to work:
from nicegui import ui



        
class RS232:
    def __init__(self):

        self.ser = serial.Serial()
        self.Port = ""
        self.Baud = "" #["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        self.Flow = "" #["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        self.Parity = "" #["NONE", "ODD", "EVEN"]
        self.Timeout = 1

    def Get_Port(self):
        return self.Port
    def Set_Port(self, Port):
        self.Port = Port
    def Get_Possible_Ports():
        Possible_Ports = []
        for p in (comports()):
            Possible_Ports.append(p.name)
        return(Possible_Ports)

    def Get_Baud(self):
        return self.Baud
    def Set_Baud(self, Baud):
        self.Baud = Baud
    def Get_Possible_Bauds():
        Possible_Bauds = ["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        return Possible_Bauds

    def Get_Flow(self):
        return self.Flow
    def Set_Flow(self, Flow):
        self.Flow = Flow
    def Get_Possible_Flows():
        Possible_Flows = ["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        return Possible_Flows

    def Get_Parity(self):
        return self.Parity
    def Set_Parity(self, Parity):
        self.Parity = Parity
    def Get_Possible_Paritys():
        Possible_Paritys = ["NONE", "ODD", "EVEN"]
        return Possible_Paritys

    def Get_Timeout(self):
        return self.Timeout
    def Set_Timeout(self, Timeout):
        self.Timeout = Timeout

    def Open(self):
        Error = None
        if(self.ser.is_open):
            Error = "Serial port is already open"
        else:
            self.ser.port = '/dev/' + self.Port
            self.ser.baudrate = self.Baud
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.dsrdtr = False
            self.ser.rtscts = False
            self.ser.xonxoff = False
            if(self.Flow.get() == "Dsr/Dtr"):
                self.ser.dsrdtr = True
            elif(self.Flow.get() == "Rts/Cts"):
                self.ser.rtscts = True
            elif(self.Flow.get() == "Xon/Xoff"):
                self.ser.xonxoff = True
            if(self.Parity.get() == "NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(self.Parity.get() == "ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(self.Parity.get() == "EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            self.ser.stopbits = serial.STOPBITS_TWO
            self.ser.timeout = self.Timeout
            try:
                self.ser.open()
            except:
                Error = "Port: " + '/dev/' + self.Port.get() + " cant be opened!"
        return Error

    def Close(self):
        Error = None
        if(self.ser.is_open):
            self.ser.close()
        else:
            Error = "Port: " + '/dev/' + self.Port.get() + " Cant be closed, was already closed."
        return Error

    def Write(self, text):
        Error = None
        if(self.ser.is_open):
            try:
                self.ser.write(text)
            except:
                Error = "Port: " + '/dev/' + self.Port.get() + " cant transmit!"
        else:
            Error = "Port: " + '/dev/' + self.Port.get() + " cant transmit, because port is not open!"
        return Error

    def Read(self):
        Error = None
        if(self.ser.is_open):
            try: 
                Text = self.ser.read()
            except:
                Error = "Port: " + '/dev/' + self.Port.get() + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port.get() + " cant recive, because port is not open!"
        return Error, Text

    def Read_Line(self):
        Error = None
        if(self.ser.is_open):
            try: 
                Text = self.ser.readline()
            except:
                Error = "Port: " + '/dev/' + self.Port.get() + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port.get() + " cant recive, because port is not open!"
        return Error, Text


RS232_1 = RS232()




# --------------------------------- GUI ---------------------------------------------------


def create_button(name, color, width):
    return ui.button(name) \
        .props('unelevated') \
        .style(f'''
            background-color: {color} !important;
            color: white !important;
            border: 2px solid white !important;
            border-radius: 0 !important;

            width: {width};
            height: 45px;
            font-weight: bold;
            font-size: 20px !important;
        ''')

def create_card(title, width='700px', height='220px', content=None, content_varriables=None):
    with ui.card().style(f'''
        background-color: black;
        border: 3px solid yellow;
        border-radius: 0;
        width: {width};
        height: {height};
        padding: 20px;
        position: relative;
        overflow: visible;
    '''):

        # Card title
        ui.label(title).style('''
            position: absolute;
            top: -16px;
            left: 16px;

            background-color: black;
            color: white;

            font-size: 20px;
            font-weight: bold;

            padding: 0 10px;
            margin: 0;

            z-index: 100;
        ''')

        if content:
            if content_varriables:
                content(content_varriables)
            else:
                content()


@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style('background-color: black;')

    # ---------- NUMERIC INPUT ---------
    ui.add_head_html('''
    <style>
    /* Increase size of the whole number input */
    .q-field__control {
        min-height: 56px !important;
    }
    /* Make spinner (up/down) buttons bigger */
    .q-field__marginal .q-btn {
        width: 42px !important;
        height: 42px !important;
    }
    /* Bigger icons */
    .q-field__marginal .q-icon {
        font-size: 26px !important;
    }
    /* Optional: match your theme */
    .q-field__marginal {
        color: yellow !important;
    }
    /* Keep input text styling */
    .yellow-input input {
        color: yellow !important;
        font-size: 24px !important;
        font-weight: bold !important;
        padding-left: 12px !important;
    }
    </style>
    ''')






    
    # ---------- RS-232 CARD ----------


    def RS232_configurator_card_content(RS232_connection: RS232):

        state = {'value': 'OPTION 1'}
        COM_Port_list = Update_COM_Port_list()

        with ui.row().style('gap: 20px;'):
            with ui.column().style('width: 99px;'):

                ui.label('Port:').style('''
                    color: yellow;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 15px;
                ''')

            with ui.column().style('width: 200px;'):
        
                def Port_updated(e):
                    state['value'] = e.value
                    COM_Port_list = Update_COM_Port_list()
                    select_Port.options = COM_Port_list
                    print('Selected:', '/dev/' + state['value'])

                select_Port = ui.select(
                    options=COM_Port_list,
                    value=COM_Port_list[0],
                    on_change=Port_updated
                ).style('''
                    width: 200px;
                    background-color: #555555;
                    color: yellow;
                    border: 2px solid white;
                    border-radius: 0;
                    font-size: 20px;
                    font-weight: bold;
                ''').props('outlined dense dark')

        with ui.row().style('gap: 20px;'):
            with ui.column().style('width: 99px;'):
        
                ui.label('Baud:').style('''
                    color: yellow;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 15px;
                ''')

            with ui.column().style('width: 200px;'):

                def Baud_updated(e):
                    state['value'] = e.value

                    print('Selected:', state['value'])

                select_Baud = ui.select(
                    options=["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"],
                    value="9600",
                    on_change=Baud_updated
                ).style('''
                    width: 200px;
                    background-color: #555555;
                    color: yellow;
                    border: 2px solid white;
                    border-radius: 0;
                    font-size: 20px;
                    font-weight: bold;
                ''').props('outlined dense dark')

        with ui.row().style('gap: 20px;'):
            with ui.column().style('width: 99px;'):
        
                ui.label('Flow:').style('''
                    color: yellow;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 15px;
                ''')

            with ui.column().style('width: 200px;'):

                def Flow_updated(e):
                    state['value'] = e.value

                    print('Selected:', state['value'])

                select_Flow = ui.select(
                    options=["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"],
                    value="NONE",
                    on_change=Flow_updated
                ).style('''
                    width: 200px;
                    background-color: #555555;
                    color: yellow;
                    border: 2px solid white;
                    border-radius: 0;
                    font-size: 20px;
                    font-weight: bold;
                ''').props('outlined dense dark')

        with ui.row().style('gap: 20px;'):
            with ui.column().style('width: 99px;'):
                
                ui.label('Parity:').style('''
                    color: yellow;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 15px;
                ''')

            with ui.column().style('width: 200px;'):

                def Parity_updated(e):
                    state['value'] = e.value

                    print('Selected:', state['value'])

                select_Parity = ui.select(
                    options=["NONE", "ODD", "EVEN"],
                    value="NONE",
                    on_change=Parity_updated
                ).style('''
                    width: 200px;
                    background-color: #555555;
                    color: yellow;
                    border: 2px solid white;
                    border-radius: 0;
                    font-size: 20px;
                    font-weight: bold;
                ''').props('outlined dense dark')

        with ui.row().style('gap: 20px;'):
            with ui.column().style('width: 99px;'):
                        
                ui.label('Timeout:').style('''
                    color: yellow;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 15px;
                ''')

            with ui.column().style('width: 200px;'):

                def Timeout_updated(e):
                    state['value'] = str(e.value)

                    print('Selected:', state['value'])

                number_Timeout = ui.number(value=0, on_change=Timeout_updated).classes('yellow-input').props('borderless').style('''
                    width: 200px;

                    background-color: #555555;
                    border: 2px solid white;
                    border-radius: 0;

                    color: yellow !important;
                    font-size: 24px !important;
                    font-weight: bold !important;

                    padding-left: 12px;
                    padding-right: 10px;
                ''')

            with ui.row().style('gap: 20px;'):
                with ui.column().style('width: 150px;'):

                    def Connect_pushed():
                        print("Connect")

                    create_button('CONNECT', '#003366', '140px').on(
                        'click',
                        Connect_pushed
                    )

                with ui.column().style('width: 150px;'):
                
                    def Disconnect_pushed():
                        print("DisConnect")

                    create_button('DISCONNECT', '#003366', '140px').on(
                        'click',
                        Disconnect_pushed
                    )

                






        

    create_card(
        'RS-232 Configurator',
        width='400px',
        height='600px',
        content=RS232_configurator_card_content,
        content_varriables=[RS232_1]
    )




    ui.add_css('''
    /* Chrome, Safari, Edge, Opera */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    /* Firefox */
    input[type=number] {
        -moz-appearance: textfield;
        appearance: textfield;
    }
    ''')






ui.run()
