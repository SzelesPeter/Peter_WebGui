#Imports for Serial communication to work:
import serial
from serial.tools.list_ports import comports
#Imports for the GUI to work:
from nicegui import ui



        
class RS232:
    def __init__(self):

        self.ser = serial.Serial()
        self.Port = "ttyS1"
        self.Baud = "9600" #["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        self.Flow = "NONE" #["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        self.Parity = "NONE" #["NONE", "ODD", "EVEN"]
        self.Timeout = 1

    def Get_Port(self):
        return self.Port
    def Set_Port(self, Port):
        self.Port = Port
    def Get_Possible_Ports(self):
        Possible_Ports = []
        for p in (comports()):
            Possible_Ports.append(p.name)
        return(Possible_Ports)

    def Get_Baud(self):
        return self.Baud
    def Set_Baud(self, Baud):
        self.Baud = Baud
    def Get_Possible_Bauds(self):
        Possible_Bauds = ["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        return Possible_Bauds

    def Get_Flow(self):
        return self.Flow
    def Set_Flow(self, Flow):
        self.Flow = Flow
    def Get_Possible_Flows(self):
        Possible_Flows = ["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        return Possible_Flows

    def Get_Parity(self):
        return self.Parity
    def Set_Parity(self, Parity):
        self.Parity = Parity
    def Get_Possible_Paritys(self):
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
            if(self.Flow == "Dsr/Dtr"):
                self.ser.dsrdtr = True
            elif(self.Flow == "Rts/Cts"):
                self.ser.rtscts = True
            elif(self.Flow == "Xon/Xoff"):
                self.ser.xonxoff = True
            if(self.Parity == "NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(self.Parity == "ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(self.Parity == "EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = self.Timeout
            try:
                self.ser.open()
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant be opened!"
            print(self.ser.is_open)
            print(self.ser.port)
        return Error

    def Close(self):
        Error = None
        if(self.ser.is_open):
            self.ser.close()
        else:
            Error = "Port: " + '/dev/' + self.Port + " Cant be closed, was already closed."
        return Error

    def Write(self, text):
        Error = None
        if(self.ser.is_open):
            try:
                self.ser.write(text.encode("utf-8"))
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant transmit!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant transmit, because port is not open!"
        return Error

    def Write_Line(self, text):
        Error = None
        if(self.ser.is_open):
            try:
                self.ser.write((text + "\r\n").encode("utf-8"))
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant transmit!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant transmit, because port is not open!"
        return Error

    def Read(self):
        Error = None
        Text = ""
        if(self.ser.is_open):
            try: 
                Text = self.ser.read().decode("utf-8")
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant recive, because port is not open!"
        return Error, Text

    def Read_Line(self):
        Error = None
        Text = ""
        if(self.ser.is_open):
            try: 
                Text = self.ser.readline().decode("utf-8")
            except:
                Error = "Port: " + '/dev/' + self.Port + " cant recive!"
        else:
            Error = "Port: " + '/dev/' + self.Port + " cant recive, because port is not open!"
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


    def RS232_configurator_card_content(Variables):
        RS232_connection: RS232 = Variables[0]
        state = {'value': 'OPTION 1'}
        COM_Port_list = RS232_connection.Get_Possible_Ports()

        
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
                    COM_Port_list = RS232_connection.Get_Possible_Ports()
                    select_Port.options = COM_Port_list
                    RS232_connection.Set_Port(state['value'])
                    print('Selected:', '/dev/' + state['value'])


                if RS232_connection.Get_Port() in COM_Port_list:
                    Start_Value = RS232_connection.Get_Port()
                else:
                    Start_Value = COM_Port_list[0]

                select_Port = ui.select(
                    options=COM_Port_list,
                    value=Start_Value,
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
                    RS232_connection.Set_Baud(state['value'])
                    print('Selected:', state['value'])

                select_Baud = ui.select(
                    options=["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"],
                    value=RS232_connection.Get_Baud(),
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
                    RS232_connection.Set_Port(state['value'])
                    print('Selected:', state['value'])

                select_Flow = ui.select(
                    options=["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"],
                    value=RS232_connection.Get_Flow(),
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
                    RS232_connection.Set_Parity(state['value'])
                    print('Selected:', state['value'])

                select_Parity = ui.select(
                    options=["NONE", "ODD", "EVEN"],
                    value=RS232_connection.Get_Parity(),
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
                    RS232_connection.Set_Timeout(str(state['value']))
                    print('Selected:', state['value'])

                number_Timeout = ui.number(value=RS232_connection.Get_Timeout(),
                    on_change=Timeout_updated
                ).classes('yellow-input').props('borderless').style('''
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
                        RS232_connection.Open()
                        print("Connect")

                    create_button('CONNECT', '#003366', '140px').on(
                        'click',
                        Connect_pushed
                    )

                with ui.column().style('width: 150px;'):
                
                    def Disconnect_pushed():
                        RS232_connection.Close()
                        print("DisConnect")

                    create_button('DISCONNECT', '#003366', '140px').on(
                        'click',
                        Disconnect_pushed
                    )
        

                
    create_card(
        'RS-232 Configurator',
        width='400px',
        height='500px',
        content=RS232_configurator_card_content,
        content_varriables=[RS232_1]
    )

    def RS232_communicator_card_content(Variables):
        RS232_connection: RS232 = Variables[0]

        text_input = ui.input() \
            .props('borderless') \
            .classes('yellow-input') \
            .style('''
                width: 100%;
                background-color: #3399ff;
                color: white;
                border: 2px solid white;
                border-radius: 0;
                font-size: 24px;
                font-weight: bold !important;
                padding-left: 12px !important;
            ''')

        def Connect_pushed():
            RS232_connection.Write_Line(text_input.value)
            text_output.value = RS232_connection.Read_Line()[1]

        create_button(
            'SUBMIT',
            '#003366',
            '150px'
        ).on(
            'click',
            Connect_pushed
        )

        text_output = ui.input() \
                    .props('borderless') \
                    .classes('yellow-input') \
                    .style('''
                        width: 100%;
                        background-color: #3399ff;
                        color: white;
                        border: 2px solid white;
                        border-radius: 0;
                        font-size: 24px;
                        font-weight: bold !important;
                        padding-left: 12px !important;
                    ''')
        

    create_card(
            'RS-232 Communicator',
            width='400px',
            height='400px',
            content=RS232_communicator_card_content,
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
