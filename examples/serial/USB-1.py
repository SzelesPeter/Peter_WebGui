#Imports for Serial communication to work:
import usb.core
import usb.util
#Imports for the GUI to work:
from nicegui import ui



        
class USB:
    def __init__(self):

        self.Device = None
        self.Devices = []
        self.IdVendor = 0x0403
        self.IdProduct = 0x6001
        self.Configuration = None
        self.Interface = None
        self.Endpoint = None

    def Get_IdVendor(self):
        return self.IdVendor
    def Set_IdVendor(self, IdVendor):
        self.IdVendor = IdVendor

    def Get_IdProductr(self):
        return self.IdProduct
    def Set_IdProduct(self, IdProduct):
        self.IdProduct = IdProduct


    def Find_Device(self):
        Error = None
        self.Devices = [] 
        self.Devices.append(usb.core.find(idVendor=self.IdVendor, idProduct=self.IdProduct))
        if (self.Devices == []):
            Error = "USB device with VendorId: " + str(self.IdVendor) + " ProductId: " + str(self.IdVendor) + " cant be found!"
            print("USB device with VendorId: " + str(self.IdVendor) + " ProductId: " + str(self.IdVendor) + " cant be found!")
        else:
            for dev in self.Devices:
                print(dev)
            
        return Error

    def Set_Configuration(self):
        Error = None
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.Device.set_configuration()
        return Error

    def Get_Configuration(self):
        Error = None
        self.Configuration = self.Device.get_active_configuration()
        return Error

    def Set_Interface(self):
        Error = None
        self.Interface = self.Configuration[(0,0)]
        return Error

    def Set_Endpoint(self):
        Error = None
        self.Endpoint = usb.util.find_descriptor(
            self.Interface,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
        return Error

    def Write(self, Text):
        Error = None
        try:
            self.Endpoint.write(Text)
        except:
            Error = "USB device with VendorId: " + str(self.IdVendor) + " ProductId: " + str(self.IdVendor) + " cant be written to!"
        return Error

    def Write_to_Endpoint(self, Endpoint, Text):
        Error = None
        try:
            self.Device.write(Endpoint, Text)
        except:
            Error = "USB device with VendorId: " + str(self.IdVendor) + " ProductId: " + str(self.IdVendor) + " cant be written to!"
        return Error

    def Read_from_Endpoint(self, Endpoint):
        Error = None
        Text = ""
        try:
            Text = self.Device.read(Endpoint)
        except:
            Error = "USB device with VendorId: " + str(self.IdVendor) + " ProductId: " + str(self.IdVendor) + " cant be written to!"
        return Error, Text



USB_1 = USB()


USB_1.Find_Device()
USB_1.Device = USB_1.Devices[0]
USB_1.Set_Configuration()
USB_1.Get_Configuration()
USB_1.Set_Interface()
USB_1.Set_Endpoint()

USB_1.Write("test")
print(USB_1.Read_from_Endpoint(1))


"""
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

"""