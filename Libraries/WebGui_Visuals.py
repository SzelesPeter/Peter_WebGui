#Imports for the GUI to work:
from nicegui import ui
from datetime import datetime
#Imports for Grid
import pandas as pd
import uuid

Blinkable = []
Time = datetime.now()

def Time_update():
    global Time
    Time = datetime.now()
    #print(Time.strftime('%H:%M:%S.%f'))

def Blink():
    
    for Element in Blinkable:
        if(Element.Blinking):
            Element.Highlight( (int(Time.strftime('%f'))) > 500000 )
        else:
            Element.Highlight(False)

class Button:
    def __init__(self, name, width, height, background_color, border_color, function_when_pressed):
        self.background_color = background_color
        self.border_color = border_color
        self.Highlighted = False
        self.Blinking = False

        self.Button_element  = ui.button(name) \
            .on('click',function_when_pressed) \
            .props('unelevated') \
            .style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 4px solid {self.border_color} !important;
                border-radius: 0 !important;

                width: {width};
                height: {height};
                font-weight: bold;
                font-size: 20px !important;
            ''')
        Blinkable.append(self)

    def Highlight(self, state):
        if(state):
            self.Button_element.style(f'''
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 4px solid {self.background_color} !important;
            ''')
        else:
            self.Button_element.style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 4px solid {self.border_color} !important;
            ''')
        self.Highlighted = state


class Text_input:
    def __init__(self, width, height, background_color, border_color, default_text = ''):
        self.background_color = background_color
        self.border_color = border_color
        self.Highlighted = False
        self.Blinking = False

        self.Text_input_element  = ui.input() \
            .props('borderless') \
            .style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 4px solid {self.border_color} !important;
                border-radius: 0 !important;

                width: {width};
                height: {height};
                font-size: 24px;
                font-weight: bold !important;
                padding-left: 12px !important;
                color: {self.border_color} !important;
            ''')
        
        self.Text_input_element.value = default_text
        Blinkable.append(self)

    def Highlight(self, state):
        if(state):
            self.Text_input_element.style(f'''
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 4px solid {self.background_color} !important;
            ''')
        else:
            self.Text_input_element.style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 4px solid {self.border_color} !important;
            ''')
        self.Highlighted = state



class Number_input:
    def __init__(self, width, height, background_color, border_color, default_value = 0):

        ui.add_css('''
            input[type=number]::-webkit-inner-spin-button,
            input[type=number]::-webkit-outer-spin-button {
                -webkit-appearance: none !important;
                margin: 0 !important;
            }

            input[type=number] {
                -moz-appearance: textfield !important;
                appearance: textfield !important;
            }
        ''')

        
        with ui.row().style(f'''
            width: {width};
            height: {height};
            gap: 0;
        '''):

            self.Number_input_element = ui.number().props(
                'borderless'
            ).style(f'''
                flex: 1;
                height: {height};
                width: 100%;
        
                background-color: {background_color};
                border: 3px solid {border_color};
                border-right: none;
                border-radius: 0;
        
                font-size: 24px !important;
                font-weight: bold !important;
                color: {border_color} !important;
        
                padding-left: 12px;
            ''')

            self.Number_input_element.set_value(default_value)
        
            with ui.column().style(f'''
                width: 45px;
                height: {height};
                gap: 0;
            '''):
        
                ui.button(
                    icon='keyboard_arrow_up',
                    on_click=lambda: self.Number_input_element.set_value(
                        (self.Number_input_element.value or 0) + 1
                    )
                ).props('flat dense').style(f'''
                    width: 100%;
                    height: 50%;
                    min-height: 0;
        
                    background-color: {background_color};
                    color: {border_color};
        
                    border: 3px solid {border_color};
                    border-bottom: 2px solid {border_color};
                    border-radius: 0;
                ''')
        
                ui.button(
                    icon='keyboard_arrow_down',
                    on_click=lambda: self.Number_input_element.set_value(
                        (self.Number_input_element.value or 0) - 1
                    )
                ).props('flat dense').style(f'''
                    width: 100%;
                    height: 50%;
                    min-height: 0;
        
                    background-color: {background_color};
                    color: {border_color};
        
                    border: 3px solid {border_color};
                    border-top: 2px solid {border_color};
                    border-radius: 0;
                ''')


def Create_Radio_Button(function_to_call, options = [], font_size = '20px', border_color = "#FFFFFF"):
    return ui.radio(
        options=options,
        value=options[0],
        on_change=lambda e: function_to_call(e.value)
    ).style(f'''
        color:  {border_color};
        font-size: {font_size};
        font-weight: bold;
    ''').props('dark')

def Create_Dropdown_Card(function_to_call, options = [], width = '45px', font_size = '20px', background_color = "#000000", border_color = "#FFFFFF"):
    # ---------- DROPDOWN CARD ----------
    ui.add_head_html(f'''
    <style>
    .q-select__control {{
        background-color: {background_color} !important;
        border: 2px solid {border_color} !important;
        border-radius: 0 !important;
    }}

    .q-field__native {{
        color: {border_color} !important;
        font-size: {font_size} !important;
        font-weight: bold !important;
    }}

    .q-menu {{
        background-color: {background_color} !important;
        color: {border_color} !important;
    }}

    .q-item {{
        color: {border_color} !important;
    }}

    .q-item:hover {{
        background-color: {background_color} !important;
    }}
    </style>
    ''')

    ui.select(
        options=options,
        value=options[0],
        on_change=lambda e: function_to_call(e.value)
    ).style(f'''
        width: {width};
        background-color: {background_color};
        color: yellow;
        border: 2px solid white;
        border-radius: 0;
        font-size: 20px;
        font-weight: bold;
    ''').props('outlined dense dark')


def Create_Grid(data, width='700px', height='220px', editable = False, header_color = "#254959", background_color = "#2F2F2F", border_color = "#FFFFFF"):

    grid_id = f"dashboard-grid-{uuid.uuid4().hex}"

    ui.add_head_html(f'''
    <style>
        /* Only this specific AG Grid */
        #{grid_id} .ag-root-wrapper {{
            background-color: {background_color} !important;
            border-radius: 0 !important;
            border: none !important;
        }}

        /* Header */
        #{grid_id} .ag-header {{
            background-color: {header_color} !important;
        }}

        #{grid_id} .ag-header-cell {{
            border-right: 1px solid {border_color} !important;
        }}

        #{grid_id} .ag-header-cell-text {{
            color: {border_color} !important;
            font-size: 20px !important;
            font-weight: bold !important;
        }}

        /* Rows */
        #{grid_id} .ag-row {{
            background-color: {background_color} !important;
        }}

        #{grid_id} .ag-cell {{
            color: {border_color} !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-right: 1px solid {border_color} !important;
            border-top: 1px solid {border_color} !important;
        }}

        /* Remove rounded corners, but ONLY inside this grid */
        #{grid_id},
        #{grid_id} * {{
            border-radius: 0 !important;
        }}
    </style>
    ''')

    return ui.aggrid({
        'columnDefs': [
            {'field': col,
            'editable': editable
             }
            for col in data.columns
        ],
        'rowData': data.to_dict('records'),
    }).props(f'id="{grid_id}"').style(f'''
        width: {width};
        height: {height};
        border: 2px solid {border_color};
    ''')


def Create_Card(title=None, width='700px', height='220px', background_color = "#000000", border_color = "#FFFFFF", content=None, content_varriables=None):
    with ui.card().style(f'''
        background-color: {background_color};
        border: 3px solid {border_color};
        border-radius: 0;
        width: {width};
        height: {height};
        padding: 20px;
        position: relative;
        overflow: visible;
    '''):

        # Card title
        if(title):
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


"""
@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style('background-color: black;')

    

    def card_content():
        def function_when_pressed():
            print("OWO")
            B1.Blinking = not(B1.Blinking)
            B2.Blinking = not(B2.Blinking)

        B1 = Button('OWO', '140px', '40px', "#660000", "#FFFFFF", function_when_pressed)

        B2 = Text_input('140px', '80px', "#FFF200", "#FFFFFF", 'test')
        

    Create_Card(
            'Card with TITLE',
            width='200px',
            height='200px',
            border_color = "#FFE600",
            content=card_content
        )

    Create_Card(
            width='200px',
            height='200px',
            background_color= "#155F2F",
            border_color = "#FF0000",
            content=card_content
        )


    N1 = Number_input('200px', '65px', "#437D78", "#FFFFFF", 1234)

    def nothing(lol):
        print(lol)
        pass

    Create_Radio_Button(function_to_call = nothing, options = ['a', 'b', 'c'], font_size = '20px', border_color = "#C71EB6")
    Create_Dropdown_Card(function_to_call = nothing, options = ['a', 'b', 'c'], width = '300px', font_size = '20px',background_color = "#AA2727", border_color = "#FFFFFF")

    data = pd.read_csv('/home/peter/Documents/Python/Projects/TestBeam/GUI/data.csv')
    Create_Grid(data=data, width='700px', height='220px', background_color = "#14491D", border_color = "#FC0000")
    Create_Grid(data=data, width='700px', height='220px', editable = True, background_color = "#292929", border_color = "#FFFFFF")

    # ---------- CLOCK PANEL ----------
    time_label = ui.label()
    date_label = ui.label()
    # Styling
    time_label.style('''
        color: #ffff00;
        font-size: 32px;
        font-weight: bold;
        font-family: monospace;
        margin: 0;
        padding: 0;
        text-align: right;
    ''')
    date_label.style('''
        color: white;
        font-size: 16px;
        font-family: monospace;
        margin: 0;
        padding: 0;
        text-align: right;
    ''')

    def Update_clock():
        time_label.set_text(Time.strftime('%H:%M:%S.%f'))
        date_label.set_text(Time.strftime('%Y-%m-%d'))


    ui.timer(0.001, Time_update)
    ui.timer(1, Update_clock)
    ui.timer(0.1, Blink)

ui.run()
"""