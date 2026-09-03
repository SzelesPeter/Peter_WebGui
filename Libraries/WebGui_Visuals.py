#Imports for the GUI to work:
from nicegui import ui
from datetime import datetime
#Imports for Grid
import pandas as pd
import uuid

Default_page_color = "#000000"
Default_background_color = "#403636"
Default_border_color = "#FFFFFF"
Default_color = "#B12C2C"
Default_width = '400px'
Default_height = '62px'
Default_box_width = '1000px'
Default_box_height = '400px'
Default_font_size = '20px'

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
    def __init__(self, function_when_pressed, name = '', width = Default_width, height = Default_height, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color):
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
                font-size: {font_size} !important;
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
    def __init__(self, width = Default_width, height = Default_height, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color, default_text = ''):
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
                font-size: {font_size};
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

class Progress_bar:
    def __init__(self, width = Default_width, height = Default_height, font_size = Default_font_size, color = Default_color, background_color = Default_background_color, border_color = Default_border_color):
        self.color = color
        self.background_color = background_color
        self.border_color = border_color
        self.Highlighted = False
        self.Blinking = False

        self.Progress_bar_element = ui.linear_progress(value=0).props(f'color={self.color}').style(f'''
            background-color: {self.background_color};
            width: {width};
            height: {height};
            font-weight: bold !important;
            font-size: {font_size} !important;
            border: 4px solid {self.border_color};
        ''')

        Blinkable.append(self)

    def Set_value(self, value):
        self.Progress_bar_element.set_value(value)

    def Highlight(self, state):
        if(state):
            self.Progress_bar_element.set_text_color(self.border_color) #set_text_color sets bar color for some reson!!!
        else:
            self.Progress_bar_element.set_text_color(self.color) #set_text_color sets bar color for some reson!!!
        self.Highlighted = state

def Create_Label(text, font_size = Default_font_size, color = Default_border_color):
    return ui.label(text).style(f'color: {color}; font-size: {font_size};')

class Number_input:
    def __init__(self, width = Default_width, height = Default_height, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color, default_value = 0):

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
                border: 4px solid {border_color};
                border-right: none;
                border-radius: 0;
        
                font-size: {font_size} !important;
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


def Create_Radio_Button(function_to_call, options = [], font_size = Default_font_size, border_color = Default_border_color):
    return ui.radio(
        options=options,
        value=options[0],
        on_change=lambda e: function_to_call(e.value)
    ).style(f'''
        color:  {border_color};
        font-size: {font_size};
        font-weight: bold;
    ''').props('dark')

def Create_Dropdown_Card(function_to_call, options = [], width = Default_width, font_size = Default_font_size, color = Default_color, background_color = Default_background_color, border_color = Default_border_color):
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
        color: {color};
        border: 2px solid white;
        border-radius: 0;
        font-size: {font_size};
        font-weight: bold;
    ''').props('outlined dense dark')


def Create_Grid(data, width=Default_box_width, height=Default_box_height, editable = False, header_color = Default_color, background_color = Default_background_color, border_color = Default_border_color):

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


def Create_Card(title=None, width=Default_box_width, height=Default_box_height, background_color = Default_page_color, border_color = Default_border_color, content=None, content_varriables=None):
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



@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {Default_page_color};')

    with ui.row():
        with ui.column():

            def card_content():
                def function_when_pressed():
                    print("OWO")
                    B1.Blinking = not(B1.Blinking)
                    T2.Blinking = not(T2.Blinking)
                    P1.Blinking = not(P1.Blinking)

                B1 = Button(function_when_pressed, name='Button')
                T2 = Text_input(default_text='Default text owo')
                L1 = Create_Label("Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.")

            Create_Card(
                    'Card with TITLE',
                    content=card_content
                )

            N1 = Number_input()
            L2 = Create_Label('The quick brown fox jumps over the lazy dog.')

            def nothing(lol):
                print(lol)
                pass
            
            Create_Radio_Button(function_to_call = nothing, options = ['a', 'b', 'c'])
            Create_Dropdown_Card(function_to_call = nothing, options = ['a', 'b', 'c'])

        with ui.column():

            data = pd.read_csv('/home/peter/Documents/Python/Projects/TestBeam/GUI/data.csv')
            Create_Grid(data=data)

            P1 = Progress_bar()
            P1.Set_value(0.7)


            # ---------- CLOCK PANEL ----------
            time_label = Create_Label(text='', font_size='100px', color=Default_color)
            date_label = Create_Label(text='', font_size='80px')

    def Update_clock():
        time_label.set_text(Time.strftime('%H:%M:%S.%f'))
        date_label.set_text(Time.strftime('%Y-%m-%d'))


    ui.timer(0.001, Time_update)
    ui.timer(1, Update_clock)
    ui.timer(0.1, Blink)

ui.run()
