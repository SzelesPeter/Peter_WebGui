#Imports for Serial communication to work:
import serial
from serial.tools.list_ports import comports
#Imports for the GUI to work:
from nicegui import ui


def Update_COM_Port_list():
        values = []
        for p in (comports()):
            values.append(p.name)
        return(values)

class RS232:
    def __init__(self):

        self.ser = serial.Serial()
        self.Port = ""
        self.Baud = "" #["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "28800", "38400", "57600", "76800", "115200", "230400", "460800", "576000", "921600"]
        self.Flow = "" #["NONE", "Dsr/Dtr", "Rts/Cts", "Xon/Xoff"]
        self.Parity = "" #["NONE", "ODD", "EVEN"]
        self.timeout = 1


RS232_1 = RS232()




# --------------------------------- GUI ---------------------------------------------------




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
