#Imports for the GUI to work:
from nicegui import ui
from datetime import datetime
#Imports for Grid
import pandas as pd
import uuid

import sys, os
Peter_WebGui_Path = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(Peter_WebGui_Path, 'Libraries'))
sys.path.append(os.path.join(os.path.join(Peter_WebGui_Path, 'Libraries'), 'Agilent drivers'))

import SVG

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
    

class SVG_Box:
    def __init__(self, svg :SVG.SVG, name='svg_image', width=Default_box_width, height=Default_box_height, background_color = Default_page_color, border_color = Default_border_color):
        self.svg = svg
        self.name = name
        '''
        ui.button(
            "Download SVG",
            on_click=lambda: ui.download(
                content=svg.encode("utf-8"),
                filename="status-register.svg",
                media_type="image/svg+xml",
            ),
        )
        '''
        self.element = ui.html(
            f'<div class="diagram-container">{self.svg.svg}</div>',
            sanitize=False,
        ).classes("w-full")
    def Update(self):
        self.element.content = f'<div class="diagram-container">{self.svg.svg}</div>'
    def Download(self):
        ui.download(
                content=self.svg.svg.encode("utf-8"),
                filename=self.name+".svg",
                media_type="image/svg+xml",
            )

class Checkbox:
    def __init__(
        self,
        name='',
        width=250,
        height=44,
        font_size=Default_font_size,
        background_color=Default_background_color,
        border_color=Default_border_color,
        checked_color=Default_color,
        text_color=Default_border_color,
        default_value=False,
        function_when_changed=None
    ):
        self.background_color = background_color
        self.border_color = border_color
        self.checked_color = checked_color
        self.text_color = text_color

        self.Highlighted = False
        self.Blinking = False

        self.Checkbox_element = ui.checkbox(
            name,
            value=default_value,
            on_change=lambda e: function_when_changed(e.value)
            if function_when_changed else None
        ).props('dark')

        self.Checkbox_element.style(f'''
            width: {Number_to_Pixel(width)};
            height: {Number_to_Pixel(height)};
            color: {self.text_color} !important;
            font-size: {Number_to_Pixel(font_size)} !important;
            font-weight: bold !important;
        ''')

        self._update_style()
        Blinkable.append(self)

    def _update_style(self):
        if self.Highlighted:
            background = self.border_color
            border = self.background_color
            text = self.background_color
        else:
            background = self.checked_color if self.Checkbox_element.value else self.background_color
            border = self.border_color
            text = self.text_color

        self.Checkbox_element.style(f'''
            color: {text} !important;
            font-weight: bold !important;
        ''')

    def Set_value(self, value):
        self.Checkbox_element.set_value(value)
        self._update_style()

    def Get_value(self):
        return self.Checkbox_element.value

    def Highlight(self, state):
        self.Highlighted = state
        self._update_style()







if __name__ in {"__main__", "__mp_main__"}: 


    import math

    # ==========================================================
    # Diagram drawing helpers
    # ==========================================================
    
    def draw_register(
        svg,
        x, y,
        title,
        subtitle,
        labels,
        indices,
        gate_x,
        row_height=25,
        box_width=134,
        enable_width=67,
        crossed_rows=None,
    ):
        """Draw a register, enable register, and its OR convergence gate."""
    
        crossed_rows = crossed_rows or []
    
        count = len(labels)
        height = count * row_height
    
        enable_x = x + box_width + 15
        gate_y = y + height / 2
    
        # Titles
        svg.text(
            x + box_width / 2, y - 35,
            title, 21, anchor="middle", weight="bold"
        )
    
        svg.text(
            x + box_width / 2, y - 12,
            subtitle, 17, anchor="middle"
        )
    
        svg.text(
            enable_x + enable_width / 2, y - 12,
            "Enable Register", 17, anchor="middle"
        )
    
        # Register outlines
        svg.rect(x, y, box_width, height)
        svg.rect(enable_x, y, enable_width, height)
    
        # Draw rows
        for i, label in enumerate(labels):
        
            yy = y + i * row_height
            cy = yy + row_height / 2
    
            # Horizontal row separator
            if i > 0:
                svg.line(x, yy, x + box_width, yy)
                svg.line(
                    enable_x, yy,
                    enable_x + enable_width, yy
                )
    
            # Register label
            svg.text(
                x + 5, cy + 5,
                label, 15
            )
    
            # Bit number
            if indices[i] is not None:
                svg.text(
                    x - 8, cy + 5,
                    str(indices[i]),
                    16,
                    anchor="end"
                )
    
            # Crossed enable row
            if i in crossed_rows:
                svg.line(
                    enable_x, yy,
                    enable_x + enable_width, yy + row_height,
                    width=1
                )
                svg.line(
                    enable_x, yy + row_height,
                    enable_x + enable_width, yy,
                    width=1
                )
    
        # Draw convergence lines
        for i in range(count):
        
            cy = y + i * row_height + row_height / 2
    
            # Lines start at enable register
            start_x = enable_x + enable_width
    
            # Spread the lines around the gate
            target_y = (
                gate_y + (i - (count - 1) / 2) * 11
            )
    
            dx = gate_x - start_x
            dy = target_y - gate_y
    
            length = math.hypot(dx, dy) or 1
    
            end_x = gate_x - 38 * dx / length
            end_y = gate_y + 38 * dy / length
    
            svg.line(
                start_x, cy,
                end_x, end_y,
                width=1
            )
    
        # OR gate
        svg.logic_gate(gate_x, gate_y)
    
        svg.text(
            gate_x + 18, gate_y - 16,
            '"OR"', 16
        )
    
        return {
            "x": x,
            "y": y,
            "width": box_width,
            "height": height,
            "enable_x": enable_x,
            "gate_x": gate_x,
            "gate_y": gate_y,
            "right": x + box_width,
            "bottom": y + height,
            "row_height": row_height,
        }
    
    
    # ==========================================================
    # Binary weights
    # ==========================================================
    
    def draw_binary_weights(svg):
    
        x, y = 718, 49
        w, h = 209, 179
    
        svg.text(
            x + w / 2, y - 10,
            "Binary Weights",
            21,
            anchor="middle",
            weight="bold"
        )
    
        svg.rect(x, y, w, h)
    
        left_x = x + 10
        right_x = x + 108
    
        for i in range(8):
        
            yy = y + 24 + i * 21
    
            left = f"2{['⁰','¹','²','³','⁴','⁵','⁶','⁷'][i]}  =  {2**i}"
            right = f"2{['⁸','⁹','¹⁰','¹¹','¹²','¹³','¹⁴','¹⁵'][i]}  =  {2**(i+8)}"
    
            svg.text(left_x, yy, left, 15)
            svg.text(right_x, yy, right, 15)
    
    
    # ==========================================================
    # Output buffer
    # ==========================================================
    
    def draw_output_buffer(svg):
    
        x, y = 574, 676
        w, h = 150, 129
    
        svg.text(
            x + w / 2, y - 14,
            "Output Buffer",
            22,
            anchor="middle",
            weight="bold"
        )
    
        svg.rect(x, y, w, h)
    
        row_height = h / 5
    
        for i in range(1, 5):
            svg.line(
                x, y + i * row_height,
                x + w, y + i * row_height
            )
    
    
    # ==========================================================
    # Main diagram
    # ==========================================================
    
    def create_diagram():
    
        svg = SVG.SVG(
            name="Status_Register_Diagram",
            width=950,
            height=850
        )
    
        svg.start()
    
        # ------------------------------------------------------
        # QUESTIONABLE DATA - 16 bits
        # ------------------------------------------------------
    
        questionable_labels = [
            "Voltage Overload",
            "Current Overload",
            "Not Used",
            "Not Used",
            "Not Used",
            "Not Used",
            "Not Used",
            "Not Used",
            "Not Used",
            "Ohms Overload",
            "Not Used",
            "Limit Test Fail LO",
            "Limit Test Fail HI",
            "Not Used",
            "Not Used",
            "Not Used",
        ]
    
        questionable_indices = [
            0, 1, None, None, None, None, None, None,
            None, 9, None, 11, 12, None, None, 15
        ]
    
        questionable = draw_register(
            svg,
            x=88,
            y=77,
            title="Questionable Data",
            subtitle="Event Register",
            labels=questionable_labels,
            indices=questionable_indices,
            gate_x=432,
            row_height=25,
        )
    
        svg.text(
            88, 505,
            "STAT:QUES:EVEN?",
            15
        )
    
        svg.text(
            238, 505,
            "STAT:QUES:ENAB <value>",
            15
        )
    
        svg.text(
            238, 523,
            "STAT:QUES:ENAB?",
            15
        )
    
        # ------------------------------------------------------
        # STANDARD EVENT - 8 bits
        # ------------------------------------------------------
    
        standard_labels = [
            "Operation Complete",
            "Not Used",
            "Query Error",
            "Device Error",
            "Execution Error",
            "Command Error",
            "Not Used",
            "Power On",
        ]
    
        standard_indices = [
            0, None, 2, 3, 4, 5, None, 7
        ]
    
        standard = draw_register(
            svg,
            x=88,
            y=604,
            title="Standard Event",
            subtitle="Event Register",
            labels=standard_labels,
            indices=standard_indices,
            gate_x=392,
            row_height=25,
        )
    
        svg.text(
            88, 825,
            "*ESR?",
            15
        )
    
        svg.text(
            238, 825,
            "*ESE <value>",
            15
        )
    
        svg.text(
            238, 843,
            "*ESE?",
            15
        )
    
        # ------------------------------------------------------
        # STATUS BYTE - 8 bits
        # ------------------------------------------------------
    
        status_labels = [
            "Not Used",
            "Not Used",
            "Not Used",
            "Questionable Data",
            "Message Available",
            "Standard Event",
            "Request Service",
            "Not Used",
        ]
    
        status_indices = [
            0, None, None, 3, 4, 5, 6, 7
        ]
    
        status = draw_register(
            svg,
            x=574,
            y=339,
            title="Status Byte",
            subtitle="Summary Register",
            labels=status_labels,
            indices=status_indices,
            gate_x=877,
            row_height=25,
            crossed_rows=[6],
        )
    
        svg.text(
            574, 583,
            "Serial Poll (SPOLL)",
            15
        )
    
        svg.text(
            574, 600,
            '"STB?',
            15
        )
    
        svg.text(
            723, 583,
            "*SRE <value>",
            15
        )
    
        svg.text(
            723, 600,
            "*SRE?",
            15
        )
    
        # ------------------------------------------------------
        # BINARY WEIGHTS
        # ------------------------------------------------------
    
        draw_binary_weights(svg)
    
        # ------------------------------------------------------
        # OUTPUT BUFFER
        # ------------------------------------------------------
    
        draw_output_buffer(svg)
    
        # ------------------------------------------------------
        # INTERCONNECTIONS
        # ------------------------------------------------------
    
        # Questionable Data OR -> Status Byte bit 3
        svg.line(470, 281, 486, 281)
        svg.line(486, 281, 486, 427)
        svg.line(486, 427, 574, 427)
    
        # Standard Event OR -> Status Byte bit 5
        svg.line(430, 704, 442, 704)
        svg.line(442, 704, 442, 477)
        svg.line(442, 477, 574, 477)
    
        # Status Byte Message Available -> Output Buffer
        svg.line(574, 452, 486, 452)
        svg.line(486, 452, 486, 740)
        svg.line(486, 740, 558, 740)
    
        # Status Byte OR output
        svg.line(915, 439, 928, 439)
        svg.line(928, 439, 928, 606)
        svg.line(928, 606, 530, 606)
        svg.line(530, 606, 530, 504)
        svg.line(530, 504, 574, 504)
    
        # ------------------------------------------------------
        # FINISH SVG
        # ------------------------------------------------------
    
        svg.end()
    
        return svg.svg





    @ui.page('/')
    def main_page():
        # Black page background
        ui.query('body').style(f'background-color: {Default_page_color};')

        with ui.row():
            with ui.column():

                with Card('Card with TITLE',):
                    def function_when_pressed():
                        print("OWO")
                        B1.Blinking = not(B1.Blinking)
                        T2.Blinking = not(T2.Blinking)
                        P1.Blinking = not(P1.Blinking)

                    B1 = Button(function_when_pressed, name='Button', background_color=Default_color)
                    T2 = Text_input(default_text='Default text owo')
                    L1 = Create_Label_Left("Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.", width= 700)


                N1 = Number_input()
                L2 = Create_Label_Left('The quick brown fox jumps over the lazy dog.', width= 700)

                def nothing(lol):
                    print(lol)
                    pass
                
                Create_Radio_Button(function_to_call = nothing, options = ['a', 'b', 'c'])
                Create_Dropdown_Card(function_to_call = nothing, options = ['a', 'b', 'c'])

            with ui.column():

                data = pd.read_csv('/home/fujitsu/Desktop/test_data.csv')
                Create_Grid(data=data)

                P1 = Progress_bar()
                P1.Set_value(0.7)


                # ---------- CLOCK PANEL ----------
                time_label = Create_Label_Left(text='', font_size='100px', color=Default_color)
                date_label = Create_Label_Left(text='', font_size='80px')

                instrument1 = [
                    "VOLTage",
                    "CURRent",
                    "NOT USED",
                    "POWer (OPP Tripped)",
                    "TEMPerature",
                    "NOT USED",
                    "NOT USED",
                    "NOT USED",
                    "NOT USED",
                    "OVP Tripped",
                    "FUSE Tripped",
                    "NOT USED",
                    "Ext.Triggered",
                    "Sense Connected",
                    "NOT USED",
                    "NOT USED *",
                ]

                instrument_summary = [
                    "Extension bit **",
                    "Instrument 2",
                    "Instrument 3",
                    "Instrument 4",
                    "Instrument 5",
                    "Instrument 6",
                    "Instrument 7",
                    "Instrument 8",
                    "Instrument 9",
                    "Instrument 10",
                    "Instrument 11",
                    "Instrument 12",
                    "Instrument 13",
                    "Instrument 14",
                    "Instrument 15",
                    "NOT USED",
                ]

                instrument_events = [
                    "Extension bit**",
                    "Instrument 2",
                    "Instrument 3",
                    "Instrument 4",
                    "Instrument 5",
                    "Instrument 6",
                    "Instrument 7",
                    "Instrument 8",
                    "Instrument 9",
                    "Instrument 10",
                    "Instrument 11",
                    "Instrument 12",
                    "Instrument 13",
                    "Instrument 14",
                    "NOT USED",
                    "NOT USED",
                ]

                status_summary = [
                    "Summary of VOLTage",
                    "Summary of CURRent",
                    "Summary of TIME",
                    "Summary of POWer",
                    "Summary of TEMPerature",
                    "Summary of FREQuency",
                    "Summary of PHASE",
                    "Summary of MODulation",
                    "Summary of CALibration",
                    "Available to designer",
                    "Available to designer",
                    "Available to designer",
                    "Available to designer",
                    "INSTRument Summary",
                    "Command Warning",
                    "NOT USED *",
                ]

                # --------------------------------------------------
                # Compose the diagram
                # --------------------------------------------------

                SVG_1 = SVG.SVG()
                def SVG_Create(text):
                    nonlocal SVG_1
                    SVG_1.delete_all()
                    SVG_1.start()
                    # Outer frame
                    SVG_1.rect(4, 4, SVG_1.width - 8, SVG_1.height - 8)
                    SVG_1.text(5, 25, text, 15)
                    # Upper-left: Instrument 1 event summary
                    g1 = SVG_1.bit_group(
                        30, 67, instrument1,
                        "STATus:QUEStionable:INSTrument:ISUMmary1",
                        side="left",
                        gate_x=570,
                    )

                    # Upper-right: instrument summary
                    g2 = SVG_1.bit_group(
                        770, 67, instrument_summary,
                        "STATus:QUEStionable:INSTrument",
                        side="right",
                        gate_x=1195,
                    )

                    # Lower-left: Instrument event summary
                    g3 = SVG_1.bit_group(
                        115, 525, instrument_events,
                        "",
                        side="left",
                        gate_x=570,
                    )

                    # Lower-right: overall status summary
                    g4 = SVG_1.bit_group(
                        770, 525, status_summary,
                        "STATus:QUEStionable",
                        side="right",
                        gate_x=1195,
                    )

                    # Extension / summary connections
                    SVG_1.line(g1["gate_x"] + 37, g1["gate_y"],
                         623, g1["gate_y"])
                    SVG_1.line(623, g1["gate_y"], 623, 104)
                    SVG_1.line(623, 104, g2["number_x"], 104)

                    SVG_1.line(g2["gate_x"] + 37, g2["gate_y"],
                         1277, g2["gate_y"])
                    SVG_1.line(1277, g2["gate_y"], 1277, 500)
                    SVG_1.line(1277, 500, g4["number_x"], 500)
                    SVG_1.line(g4["number_x"], 500, g4["number_x"], 525)

                    SVG_1.line(g3["gate_x"] + 37, g3["gate_y"],
                         660, g3["gate_y"])
                    SVG_1.line(660, g3["gate_y"], 660, 525)
                    SVG_1.line(660, 525, g4["number_x"], 525)

                    # Status byte output
                    SVG_1.line(g4["gate_x"] + 37, g4["gate_y"],
                         1300, g4["gate_y"], width=1.2)
                    SVG_1.add(
                        f'<polygon points="1300,{g4["gate_y"] - 6} '
                        f'1315,{g4["gate_y"]} 1300,{g4["gate_y"] + 6}" '
                        'fill="#222"/>'
                    )
                    SVG_1.text(1320, g4["gate_y"] - 20, "To Status Byte,", 23, weight="bold")
                    SVG_1.text(1320, g4["gate_y"] + 13, "Bit 3", 23, weight="bold")

                    # Notes
                    SVG_1.text(145, 422, "*)", 15)
                    SVG_1.text(178, 422, "The use of Bit 15 is not allowed", 16)
                    SVG_1.text(178, 442, "since some controllers may have", 16)
                    SVG_1.text(178, 462, "difficulty reading a 16 bit un-", 16)
                    SVG_1.text(178, 482, "signed integer. The value of this", 16)
                    SVG_1.text(178, 502, "bit shall always be 0.", 16)

                    SVG_1.text(430, 422, "**)", 15)
                    SVG_1.text(463, 422, "The extension bit is used, where", 16)
                    SVG_1.text(463, 442, "required, to summarize the events", 16)
                    SVG_1.text(463, 462, "in Instrument 15 and up. The", 16)
                    SVG_1.text(463, 482, "extension of the status structure", 16)
                    SVG_1.text(463, 502, "shall conform to IEEE 488.2", 16)

                    SVG_1.end()
                SVG_Create(Time.strftime('%H:%M:%S.%f'))
                SVG_1 = SVG.SVG()
                SVG_1.svg = create_diagram()
                SVG_Box_1 = SVG_Box(SVG_1)
                C1 = Checkbox()
                C2 = Checkbox()
                C3 = Checkbox()
                C4 = Checkbox('A')
                C4 = Checkbox('B')
                C5 = Checkbox('C')

        def Update_clock():
            time_label.set_text(Time.strftime('%H:%M:%S.%f'))
            date_label.set_text(Time.strftime('%Y-%m-%d'))
            SVG_Create(Time.strftime('%H:%M:%S.%f'))
            SVG_Box_1.Update()
            P1.Set_value(int(Time.strftime('%S'))/60)


        ui.timer(0.001, Time_update)
        ui.timer(1, Update_clock)
        ui.timer(0.1, Blink)

    ui.run()