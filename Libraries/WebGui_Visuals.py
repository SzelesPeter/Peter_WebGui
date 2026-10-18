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
Default_width = 100
Default_height = 44
Default_box_width = 1000
Default_box_height = 400
Default_font_size = 16

Blinkable = []
Time = datetime.now()

def Number_to_Pixel(number: int) -> str:
    return (str(number) + 'px')

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
    def __init__(self, function_when_pressed, name = '', width = Default_width, height = Default_height, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color, text_color = Default_border_color):
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
        self.Highlighted = False
        self.Blinking = False

        self.Button_element  = ui.button(name) \
            .on('click',function_when_pressed) \
            .props('unelevated') \
            .style(f'''
                background-color: {self.background_color} !important;
                color: {self.text_color} !important;
                border: 3px solid {self.border_color} !important;
                border-radius: 0 !important;

                width: {Number_to_Pixel(width)};
                height: {Number_to_Pixel(height)};
                font-weight: bold;
                font-size: {Number_to_Pixel(font_size)} !important;
            ''')
        Blinkable.append(self)

    def Highlight(self, state):
        if(state):
            self.Button_element.style(f'''
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 3px solid {self.background_color} !important;
            ''')
        else:
            self.Button_element.style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 3px solid {self.border_color} !important;
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
                border: 3px solid {self.border_color} !important;
                border-radius: 0 !important;

                width: {Number_to_Pixel(width)};
                padding: 0 14px !important;
                height: {Number_to_Pixel(height)} !important;
                line-height: {Number_to_Pixel(height)} !important;
                font-size: {Number_to_Pixel(font_size)} !important;
                font-weight: bold !important;
                color: {self.border_color} !important;
            ''')
        
        self.Text_input_element.value = default_text
        Blinkable.append(self)

    def Highlight(self, state):
        if(state):
            self.Text_input_element.style(f'''
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 3px solid {self.background_color} !important;
            ''')
        else:
            self.Text_input_element.style(f'''
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 3px solid {self.border_color} !important;
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
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
            font-weight: bold !important;
            font-size: {Number_to_Pixel(font_size)} !important;
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

def Create_Label_Left(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

def Create_Label_Right(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center justify-end').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center justify-end').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

def Create_Label_Center(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center justify-center').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center justify-center').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

def Create_Label_Left_Bold(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

def Create_Label_Right_Bold(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center justify-end').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center justify-end').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

def Create_Label_Center_Bold(text, font_size = Default_font_size, width = Default_width, height = Default_height, color = Default_border_color, background_color = None):
    if(background_color != None):
        return ui.label(text).classes('w-full h-full flex items-center justify-center').style(f'''
            background-color: {background_color} !important;
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')
    else:
        return ui.label(text).classes('w-full h-full flex items-center justify-center').style(f'''
            color: {color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
        ''')

class Number_input:
    def __init__(self, name = None, button_function = None, number_function = None, text_width = Default_width, number_width = Default_width, height = Default_height, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color, default_value = 0, min = -1, max = 1):
        self.min = min
        self.max = max

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
            .q-field__native {
                transform: translateY(-5px);
            }
        ''')

        
        with ui.row().style(f'''
            width: {Number_to_Pixel(text_width+number_width+49)};
            height: {Number_to_Pixel(height)};
            gap: 0;
        '''):
            
            with Card(width= text_width+number_width+4, height= 44,background_color= background_color,padding= 0,border_width= 2):
                with ui.row().style(f'''
                            width: {Number_to_Pixel(text_width+number_width)};
                            height: {Number_to_Pixel(height)};
                            gap: 0;
                        '''):
                    if name:
                        Create_Label_Right_Bold(text = name, width = text_width)
                    if number_function != None:
                        self.Number_input_element = ui.number(on_change =lambda e: self.validate(e.value, number_function)).props(
                            'borderless'
                        ).style(f'''
                            flex: 1;
                            height: {Number_to_Pixel(height-4)};
                            width: {Number_to_Pixel(number_width)};

                            background-color: {background_color};
                            border: 0px solid {border_color};
                            border-right: none;
                            border-radius: 0;

                            font-size: {Number_to_Pixel(font_size)} !important;
                            font-weight: bold !important;
                            color: {border_color} !important;

                            padding-left: 12px;
                            padding-top: 0px;

                        ''')
                    else:
                        self.Number_input_element = ui.number(min = min, max = max).props(
                            'borderless'
                        ).style(f'''
                            flex: 1;
                            height: {Number_to_Pixel(height-4)};
                            width: {Number_to_Pixel(number_width)};

                            background-color: {background_color};
                            border: 0px solid {border_color};
                            border-right: none;
                            border-radius: 0;

                            font-size: {Number_to_Pixel(font_size)} !important;
                            font-weight: bold !important;
                            color: {border_color} !important;

                            padding-left: 12px;
                            padding-top: 0px;

                        ''')

                    self.Number_input_element.set_value(default_value)
        
            with ui.column().style(f'''
                width: 45px;
                height: {Number_to_Pixel(height)};
                gap: 0;
            '''):
        
                ui.button(
                    text='▲',
                    on_click=lambda: self.Number_input_element.set_value(
                        (self.Number_input_element.value or 0) + 1
                    )
                ).props('flat dense').style(f'''
                    width: 100%;
                    height: 50%;
                    min-height: 0;
                    font-size: {Number_to_Pixel(10)} !important;
        
                    background-color: {background_color};
                    color: {border_color} !important;
                    border: 2px solid {border_color};
                    border-bottom: 0px solid {border_color};
                    border-radius: 0;
                ''')
        
                ui.button(
                    text = '▼',
                    on_click=lambda: self.Number_input_element.set_value(
                        (self.Number_input_element.value or 0) - 1
                    )
                ).props('flat dense').style(f'''
                    width: 100%;
                    height: 50%;
                    min-height: 0;
                    font-size: {Number_to_Pixel(10)} !important;
        
                    background-color: {background_color};
                    color: {border_color} !important;
                    border: 2px solid {border_color};
                    border-top: 2px solid {border_color};
                    border-radius: 0;
                ''')
            if button_function != None:
                self.B1 = Button(lambda: self.validate(e.value, button_function), name='Set', width= 80, background_color = background_color)
    def validate(self,value, function):
        if value > self.max:
            value = self.max
            self.Number_input_element.set_value(self.max)
        if value < self.min:
            value = self.min
            self.Number_input_element.set_value(self.min)
        function(value)

def Create_Radio_Button(function_to_call, options = [], font_size = Default_font_size, border_color = Default_border_color):
    return ui.radio(
        options=options,
        value=options[0],
        on_change=lambda e: function_to_call(e.value)
    ).style(f'''
        color:  {border_color};
        font-size: {Number_to_Pixel(font_size)};
        font-weight: bold;
    ''').props('dark')

def Create_Dropdown_Card(function_to_call = None, options = [], width = Default_width, height = Default_height, font_size = Default_font_size, color = Default_color, background_color = Default_background_color, border_color = Default_border_color, border_width = 2, editable = False):
    # ---------- DROPDOWN CARD ----------
    ui.add_head_html(f'''
    <style>

    .q-select .q-field__control::before,
    .q-select .q-field__control::after,
    .q-select .q-field__native::before,
    .q-select .q-field__native::after {{
        border-bottom: none !important;
        box-shadow: none !important;
    }}

    .q-select .q-field__control {{
        border: none !important;
        box-shadow: none !important;
        padding-top: 5px !important;
        padding-left: 8px !important;
    }}
    .q-select__control {{
        background-color: {background_color} !important;
        border: {Number_to_Pixel(border_width)} solid {border_color} !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }}

    .q-field__native {{
        color: {border_color} !important;
        font-size: {Number_to_Pixel(font_size)} !important;
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

    if function_to_call != None:
        element = ui.select(
            options=options,
            value=options[0],
            on_change=lambda e: function_to_call(e.value),
            with_input=editable,
            new_value_mode='add-unique',
        ).style(f'''
            width: {Number_to_Pixel(width)} !important;
            height: {Number_to_Pixel(height)} !important;
            background-color: {background_color} !important;
            color: {color} !important;
            border: {Number_to_Pixel(border_width)} solid white;
            border-radius: 0 !important;
            font-size: {Number_to_Pixel(font_size)};
            font-weight: bold;
        ''').props('dense dark')

        element.on('click', element.update)
    else:
        element = ui.select(
            options=options,
            value=options[0],
        ).style(f'''
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)} !important;
            background-color: {background_color} !important;
            color: {color} !important;
            border: {Number_to_Pixel(border_width)} solid white;
            border-radius: 0 !important;
            font-size: {Number_to_Pixel(font_size)};
            font-weight: bold;
        ''').props('dense dark')

    return element

def Create_Dropdown_Card_With_Name(name, function_to_call= None, options = [], text_width = Default_width, dropdown_width = Default_width, font_size = Default_font_size, color = Default_border_color, background_color = Default_background_color, border_color = Default_border_color, editable = False):
    with Card(width= text_width+dropdown_width+14, height= 44,background_color= background_color,padding= 0,border_width= 2):
        with ui.row().classes('gap-0 p-0 m-0'): # column with no spaceing
            Create_Label_Right_Bold(text = name, font_size = font_size, width = text_width, height = 40, color = color, background_color = None)
            return Create_Dropdown_Card(function_to_call = function_to_call, options = options, width = dropdown_width, height = 32, font_size = font_size, color = color, background_color = background_color, border_color = border_color, border_width = 0, editable = editable)

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
        width: {Number_to_Pixel(width)};
        height: {Number_to_Pixel(height)};
        border: 2px solid {border_color};
    ''')

class Grid:
    def __init__(
        self,
        data,
        width=Default_box_width,
        height=Default_box_height,
        editable=False,
        header_color=Default_color,
        background_color=Default_background_color,
        border_color=Default_border_color
    ):
        self.Editable = editable
        self.Grid_element = Create_Grid(
            data,
            width,
            height,
            editable,
            header_color,
            background_color,
            border_color
        )

    def update_from_df(self, df):
        self.Grid_element.options['columnDefs'] = [
            {
                'field': str(col),
                'editable': self.Editable
            }
            for col in df.columns
        ]

        self.Grid_element.options['rowData'] = df.to_dict('records')
        self.Grid_element.update()

    async def data_to_df(self):
        grid_data = await self.Grid_element.get_client_data(
            timeout=5,
            method='all_unsorted'
        )
        # Convert the grid data to a pandas DataFrame
        return pd.DataFrame(grid_data)
    

    def add_column(self, column_name, default_value=None):
        """Add a column to the grid, optionally filling it with a default value."""
        column_defs = self.Grid_element.options['columnDefs']
        row_data = self.Grid_element.options['rowData']

        if any(col['field'] == str(column_name) for col in column_defs):
            raise ValueError(f"Column '{column_name}' already exists.")

        # Add the new column definition
        column_defs.append({
            'field': str(column_name),
            'editable': self.Editable
        })

        # Populate the new column in every existing row
        for row in row_data:
            row[str(column_name)] = default_value

        self.Grid_element.options['columnDefs'] = column_defs
        self.Grid_element.options['rowData'] = row_data

    def add_row(self, row=None):
        """Add a row as a dictionary, or an empty row if no data is provided."""
        column_defs = self.Grid_element.options['columnDefs']
        row_data = self.Grid_element.options['rowData']

        column_names = [col['field'] for col in column_defs]

        if row is None:
            row = {}

        # Ensure the new row contains every column
        new_row = {
            column: row.get(column, None)
            for column in column_names
        }

        # Reject unknown columns to catch potential typos
        unknown_columns = set(row.keys()) - set(column_names)
        if unknown_columns:
            raise ValueError(
                f"Unknown column(s): {', '.join(map(str, unknown_columns))}"
            )

        row_data.append(new_row)

        self.Grid_element.options['rowData'] = row_data

        self.Grid_element.run_grid_method(
        'ensureIndexVisible',
        len(self.Grid_element.options['rowData']) - 1,
        'bottom'
)
    


class Card:
    def __init__(self, name=None, width=Default_box_width, height=Default_box_height, background_color = Default_page_color, border_color = Default_border_color, content_varriables=None, padding = 20,border_width= 3):
        self.Name = name
        self.Card_element = ui.card().style(f'''
            background-color: {background_color};
            border: {Number_to_Pixel(border_width)} solid {border_color};
            border-radius: 0;
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)} !important;
            padding: {Number_to_Pixel(padding)};
            position: relative;
            overflow: visible;
        ''')

    def __enter__(self):
        # Enter the NiceGUI card context
        self.Card_element.__enter__()

        # Card title
        if(self.Name):
            ui.label(self.Name).style('''
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

        return self.Card_element
        

    def __exit__(self, exc_type, exc_value, exc_traceback):
         # Leave the NiceGUI card context
        return self.Card_element.__exit__(
            exc_type,
            exc_value,
            exc_traceback
        )
    




"""

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

                B1 = Button(function_when_pressed, name='Button', background_color=Default_color)
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
"""