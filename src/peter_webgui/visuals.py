#Imports for the GUI to work:
from nicegui import ui
from datetime import datetime
#Imports for Grid
import pandas as pd
import uuid

import os
import functools
import inspect
from pathlib import Path

from peter_webgui import svg as SVG

# Project root (…/peter_webgui), used by the demo blocks to find examples/data.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DATA_DIR = PROJECT_ROOT / 'examples' / 'data'

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

        # The text colour reaches the native <input> through --wgv-text-color (same as Text_area). Without it the text
        # takes Quasar's default dark colour unless some other widget on the page happens to add CSS for it.
        self.Text_input_element  = ui.input() \
            .props('borderless input-style="color: var(--wgv-text-color); font-size: inherit; font-weight: inherit;"') \
            .style(f'''
                --wgv-text-color: {self.border_color};
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
                --wgv-text-color: {self.background_color};
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 3px solid {self.background_color} !important;
            ''')
        else:
            self.Text_input_element.style(f'''
                --wgv-text-color: {self.border_color};
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: 3px solid {self.border_color} !important;
            ''')
        self.Highlighted = state

class Text_area:
    """Multi-line text input in the same style as Text_input.

    Enter adds a new line. height is the size of the whole box, and text longer than that scrolls.
    function_when_changed(text) is called on every edit.

        T = WGV.Text_area(width=600, height=150, default_text='line 1\nline 2')
        T.Get_text()   # 'line 1\nline 2'
        T.Get_lines()  # ['line 1', 'line 2']
    """
    def __init__(self, width = 500, height = 150, font_size = Default_font_size, background_color = Default_background_color, border_color = Default_border_color, default_text = '', function_when_changed = None):
        self.background_color = background_color
        self.border_color = border_color
        self.Highlighted = False
        self.Blinking = False
        self.function_when_changed = function_when_changed

        border_width = 3
        padding = 8
        # Quasar colours the field's inner control with the theme's primary blue, and 'inherit' would pick that up,
        # so the text colour reaches the native textarea through the --wgv-text-color variable instead.
        text_height = height - 2 * (border_width + padding)

        self.Text_area_element = ui.textarea(value=default_text,
                                             on_change=lambda e: self.function_when_changed(e.value) if self.function_when_changed else None) \
            .props(f'borderless input-style="color: var(--wgv-text-color); font-size: inherit; font-weight: inherit; '
                   f'height: {Number_to_Pixel(text_height)}; min-height: {Number_to_Pixel(text_height)}; resize: none; line-height: 1.4;"') \
            .style(f'''
                --wgv-text-color: {self.border_color};
                background-color: {self.background_color} !important;
                color: {self.border_color} !important;
                border: {Number_to_Pixel(border_width)} solid {self.border_color} !important;
                border-radius: 0 !important;

                width: {Number_to_Pixel(width)};
                height: {Number_to_Pixel(height)} !important;
                padding: {Number_to_Pixel(padding)} 14px !important;
                font-size: {Number_to_Pixel(font_size)} !important;
                font-weight: bold !important;
            ''')
        Blinkable.append(self)

    def Get_text(self):
        return self.Text_area_element.value or ''

    def Get_lines(self):
        return self.Get_text().splitlines()

    def Set_text(self, text):
        self.Text_area_element.set_value(text)

    def Highlight(self, state):
        if(state):
            self.Text_area_element.style(f'''
                --wgv-text-color: {self.background_color};
                background-color: {self.border_color} !important;
                color: {self.background_color} !important;
                border: 3px solid {self.background_color} !important;
            ''')
        else:
            self.Text_area_element.style(f'''
                --wgv-text-color: {self.border_color};
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
                            f'borderless input-style="color: {border_color}; font-size: inherit; font-weight: inherit;"'
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
                            f'borderless input-style="color: {border_color}; font-size: inherit; font-weight: inherit;"'
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
        if value is None:   # box emptied while typing
            return
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
            value=options[0] if options else None,
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
            value=options[0] if options else None,
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

def Grid_column_def(column, editable = False, column_width = None):
    """AG Grid column definition for one column.

    column_width: None (no fixed width), a number of pixels for every column,
    or a dict {column name: pixels} for some columns (the others get AG Grid's default of 200 px).
    """
    column_def = {'field': str(column), 'editable': editable}
    if isinstance(column_width, dict):
        if column in column_width:
            column_def['width'] = column_width[column]
        elif str(column) in column_width:
            column_def['width'] = column_width[str(column)]
    elif column_width is not None:
        column_def['width'] = column_width
    return column_def

def Create_Grid(data, width=Default_box_width, height=Default_box_height, editable = False, header_color = Default_color, background_color = Default_background_color, border_color = Default_border_color, column_width = None):
    """AG Grid styled like the other WGV widgets.

    column_width: None (default) stretches the columns to fill the grid width. A number gives every column that
    width in pixels, and a dict {column name: pixels} sets individual columns. With a fixed width the columns may
    not fill the grid, or may need horizontal scrolling.
    """

    grid_id = f"dashboard-grid-{uuid.uuid4().hex}"

    # AG Grid (v33+, NiceGUI 3/4) takes its colours from theme CSS variables. Setting them on the grid element
    # covers every part of it, including the empty space below the last row, which otherwise stays white.
    theme_variables = f'''
        --ag-background-color: {background_color};
        --ag-odd-row-background-color: {background_color};
        --ag-chrome-background-color: {background_color};
        --ag-header-background-color: {header_color};
        --ag-foreground-color: {border_color};
        --ag-text-color: {border_color};
        --ag-header-text-color: {border_color};
        --ag-cell-text-color: {border_color};
        --ag-border-color: {border_color};
        --ag-row-border: 1px solid {border_color};
        --ag-column-border: none;            /* the full-height resize bars below draw the column lines */
        --ag-header-column-border: none;
        --ag-wrapper-border: none;
        --ag-wrapper-border-radius: 0;
        --ag-border-radius: 0;
        --ag-font-size: 18px;
        --ag-header-font-size: 20px;
        --ag-header-font-weight: bold;
        --ag-header-column-resize-handle-color: {border_color};
        --ag-header-column-resize-handle-width: 1px;
    '''
    grid_border_width = 2
    inner_height = height - 2 * grid_border_width

    ui.add_head_html(f'''
    <style>
        /* Bold cell text, and no rounded corners anywhere inside this grid */
        #{grid_id} .ag-cell {{
            font-weight: bold !important;
        }}
        #{grid_id},
        #{grid_id} * {{
            border-radius: 0 !important;
        }}

        /* Column-resize drag bars run the full height of the grid, not just the header.
           The header containers normally clip their contents, so let the bars hang out below them,
           and draw the header above the rows so the bars stay on top and can be dragged anywhere. */
        #{grid_id} .ag-header,
        #{grid_id} .ag-header-viewport,
        #{grid_id} .ag-header-container,
        #{grid_id} .ag-header-row,
        #{grid_id} .ag-header-cell {{
            overflow: visible !important;
        }}
        #{grid_id} .ag-header {{
            position: relative;
            z-index: 3;
        }}
        #{grid_id} .ag-header-cell-resize {{
            height: {Number_to_Pixel(inner_height)} !important;
        }}
        #{grid_id} .ag-header-cell-resize::after {{
            height: 100% !important;
            top: 0 !important;
        }}
    </style>
    ''')

    return ui.aggrid({
        'columnDefs': [Grid_column_def(col, editable, column_width) for col in data.columns],
        'rowData': data.to_dict('records'),
    }, auto_size_columns = column_width is None).props(f'id="{grid_id}"').style(f'''
        width: {Number_to_Pixel(width)};
        height: {Number_to_Pixel(height)};
        border: {Number_to_Pixel(grid_border_width)} solid {border_color};
        {theme_variables}
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
        border_color=Default_border_color,
        column_width=None
    ):
        """column_width: None (fit columns to the grid width), pixels for every column, or {column name: pixels}."""
        self.Editable = editable
        self.Column_width = column_width
        self.Grid_element = Create_Grid(
            data,
            width,
            height,
            editable,
            header_color,
            background_color,
            border_color,
            column_width
        )

    def Set_column_width(self, column_width):
        """Change the column widths: None (fit to the grid width), pixels for every column, or {column name: pixels}."""
        self.Column_width = column_width
        self.Grid_element.options['columnDefs'] = [
            Grid_column_def(col['field'], self.Editable, column_width)
            for col in self.Grid_element.options['columnDefs']
        ]
        self.Grid_element.auto_size_columns = column_width is None
        self.Grid_element.update()

    def update_from_df(self, df):
        self.Grid_element.options['columnDefs'] = [
            Grid_column_def(col, self.Editable, self.Column_width)
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
        column_defs.append(Grid_column_def(column_name, self.Editable, self.Column_width))

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
    

class Page:
    """A NiceGUI page with the WGV look: page title, background colour and an optional root container.

    As a decorator it registers the function with ``@ui.page`` and builds the page body inside this context:

        @WGV.Page('/', title='HP34401A', layout='row')
        def main_page():
            with WGV.Card('Settings'):
                ...

    As a context manager it is used inside a page function you registered yourself:

        @ui.page('/')
        def main_page():
            with WGV.Page(title='HP34401A'):
                ...

    A page body has to be a function, because NiceGUI builds a new copy of the page for each browser tab that
    opens it. A ``with WGV.Page(...)`` block at module level would run only once, so it is not supported.

    layout: None (no container), 'row' or 'column'.
    favicon: browser-tab icon. An emoji ('📟'), the path of a local image file, an http(s):// URL, a data URL
        or an inline '<svg ...>' string. None keeps the icon set by ui.run(favicon=...), or NiceGUI's default.
        The icon is set only when Page is used as a decorator. Inside a page you registered with ui.page
        yourself, pass favicon= to that ui.page call instead.
    Any other keyword arguments go to ``ui.page`` (e.g. dark=, response_timeout=).
    """
    def __init__(self, path = '/', title = None, background_color = Default_page_color, layout = None, favicon = '🦊', **page_kwargs):
        if layout not in (None, 'row', 'column'):
            raise ValueError(f"layout must be None, 'row' or 'column', not {layout!r}")
        self.path = path
        self.title = title
        self.background_color = background_color
        self.layout = layout
        self.favicon = favicon
        self.page_kwargs = page_kwargs
        self.Page_element = None

    def __enter__(self):
        if self.title:
            ui.page_title(self.title)
        ui.query('body').style(f'background-color: {self.background_color};')
        if self.layout == 'row':
            self.Page_element = ui.row()
        elif self.layout == 'column':
            self.Page_element = ui.column()
        if self.Page_element is not None:
            self.Page_element.__enter__()
        return self.Page_element

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.Page_element is not None:
            return self.Page_element.__exit__(exc_type, exc_value, exc_traceback)
        return False

    def _new_context(self):
        # A fresh instance per request, so pages built at the same time don't share Page_element.
        return Page(self.path, self.title, self.background_color, self.layout)

    def __call__(self, func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                with self._new_context():
                    return await func(*args, **kwargs)
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self._new_context():
                    return func(*args, **kwargs)
        # functools.wraps keeps func's signature, so ui.page still injects path params, client and request.
        ui.page(self.path, title=self.title, favicon=self.favicon, **self.page_kwargs)(wrapper)
        return func


class Page_Selector:
    """Card with one button per page, for switching between pages.

    pages: list of (path, button text) pairs, e.g. [('/', 'Home'), ('/chart', 'Chart')].
    current_path: path of the page this selector is on. Its button is drawn in the accent colour.
    The default size (320 x 450) matches RS232_GUI, so the two line up in a column.

        WGV.Page_Selector([('/', 'Home'), ('/chart', 'Chart')], current_path='/')
    """
    def __init__(self, pages, current_path = None, name = 'Pages', width = 320, height = 450, font_size = Default_font_size, background_color = Default_page_color, border_color = Default_border_color, button_color = Default_background_color, selected_color = Default_color, padding = 20, border_width = 3):
        self.pages = list(pages)
        self.current_path = current_path
        self.Buttons = {}
        button_width = width - 2 * (padding + border_width)
        # Fit all buttons into the card: 16 px gaps if they fit, otherwise 8 px gaps and, if still needed, lower buttons.
        inner_height = height - 2 * (padding + border_width)
        count = max(len(self.pages), 1)
        gap = 16 if count * Default_height + (count - 1) * 16 <= inner_height else 8
        button_height = min(Default_height, (inner_height - (count - 1) * gap) // count)
        self.Card = Card(name=name, width=width, height=height, background_color=background_color, border_color=border_color, padding=padding, border_width=border_width)
        with self.Card:
            with ui.column().style(f'gap: {Number_to_Pixel(gap)};'):
                for path, text in self.pages:
                    self.Buttons[path] = Button(lambda p=path: self.Go_to(p), name=text, width=button_width, height=button_height,
                                                font_size=font_size,
                                                background_color=selected_color if path == current_path else button_color,
                                                border_color=border_color)

    def Go_to(self, path):
        ui.navigate.to(path)


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


class File_Manager:
    """Card for picking a file in a folder and loading / saving it.

    Rows: folder path, file extensions, file dropdown (+ Refresh), filename for Save As,
    then the Load / Save / Save As buttons and a status line.

    load_function(path) and save_function(path) get a pathlib.Path and do the actual reading/writing.
    - Load:    load_function(<folder>/<selected file>)
    - Save:    save_function(<folder>/<selected file>)   (overwrites the selected file)
    - Save As: save_function(<folder>/<filename box>)    (adds the first extension if the name has none)

    Extensions are separated by commas, spaces or semicolons, with or without the dot ('csv, .txt').
    Leave the box empty to list every file.

        def Load(path): df = pd.read_csv(path)
        def Save(path): df.to_csv(path, index=False)
        FM = WGV.File_Manager(Load, Save, folder=os.getcwd(), extensions='.csv')
    """
    def __init__(self, load_function = None, save_function = None, name = 'Files', folder = None, extensions = '.csv', filename = '',
                 width = 640, height = 410, label_width = 110, font_size = Default_font_size,
                 background_color = Default_background_color, border_color = Default_border_color, padding = 20, border_width = 3):
        self.load_function = load_function
        self.save_function = save_function
        self.Files = []

        gap = 8
        inner_width = width - 2 * (padding + border_width)
        input_width = inner_width - label_width - gap
        refresh_width = 100
        select_width = input_width - refresh_width - gap
        button_width = (inner_width - 2 * gap) // 3

        self.Card = Card(name=name, width=width, height=height, padding=padding, border_width=border_width, border_color=border_color)
        with self.Card:
            with ui.row().classes('gap-2 items-center no-wrap'):
                Create_Label_Right_Bold('Folder:', font_size=font_size, width=label_width)
                self.Folder_input = Text_input(width=input_width, font_size=font_size, background_color=background_color, border_color=border_color,
                                               default_text=str(folder if folder is not None else os.getcwd()))
            with ui.row().classes('gap-2 items-center no-wrap'):
                Create_Label_Right_Bold('Extensions:', font_size=font_size, width=label_width)
                self.Extensions_input = Text_input(width=input_width, font_size=font_size, background_color=background_color, border_color=border_color,
                                                   default_text=extensions)
            with ui.row().classes('gap-2 items-center no-wrap'):
                Create_Label_Right_Bold('File:', font_size=font_size, width=label_width)
                self.File_select = Create_Dropdown_Card(function_to_call=self._File_selected, options=[], width=select_width, font_size=font_size,
                                                        background_color=background_color, border_color=border_color)
                self.Refresh_button = Button(self.Refresh, name='Refresh', width=refresh_width, font_size=font_size,
                                             background_color=background_color, border_color=border_color)
            with ui.row().classes('gap-2 items-center no-wrap'):
                Create_Label_Right_Bold('Filename:', font_size=font_size, width=label_width)
                self.Filename_input = Text_input(width=input_width, font_size=font_size, background_color=background_color, border_color=border_color,
                                                 default_text=filename)
            with ui.row().classes('gap-2 items-center no-wrap'):
                self.Load_button = Button(self.Load, name='Load', width=button_width, font_size=font_size,
                                          background_color=background_color, border_color=border_color)
                self.Save_button = Button(self.Save, name='Save', width=button_width, font_size=font_size,
                                          background_color=background_color, border_color=border_color)
                self.Save_As_button = Button(self.Save_As, name='Save As', width=button_width, font_size=font_size,
                                             background_color=background_color, border_color=border_color)
            self.Status_label = ui.label('').style(f'color: {border_color}; font-size: {Number_to_Pixel(font_size - 2)}; width: {Number_to_Pixel(inner_width)};')

        # Re-list the files whenever the folder or the extension list changes.
        self.Folder_input.Text_input_element.on_value_change(lambda e: self.Refresh())
        self.Extensions_input.Text_input_element.on_value_change(lambda e: self.Refresh())
        self.Refresh()

    # ---------- getters ----------
    def Get_folder(self):
        return Path(os.path.expanduser((self.Folder_input.Text_input_element.value or '').strip() or '.'))

    def Get_extensions(self):
        text = self.Extensions_input.Text_input_element.value or ''
        parts = text.replace(',', ' ').replace(';', ' ').split()
        return ['.' + p.lstrip('.').lower() for p in parts if p.lstrip('.')]

    def Get_selected_path(self):
        if not self.File_select.value:
            return None
        return self.Get_folder() / self.File_select.value

    def Set_status(self, text, error = False):
        self.Status_label.set_text(text)
        self.Status_label.style(f'color: {Default_color if error else Default_border_color};')

    # ---------- file list ----------
    def Refresh(self):
        folder = self.Get_folder()
        if not folder.is_dir():
            self.Files = []
            self.File_select.set_options([], value=None)
            self.Set_status(f'Folder not found: {folder}', error=True)
            return
        extensions = self.Get_extensions()
        try:
            self.Files = sorted((p.name for p in folder.iterdir()
                                 if p.is_file() and (not extensions or p.suffix.lower() in extensions)), key=str.lower)
        except OSError as e:
            self.Files = []
            self.File_select.set_options([], value=None)
            self.Set_status(f'Cannot read folder: {e}', error=True)
            return
        current = self.File_select.value
        self.File_select.set_options(self.Files, value=current if current in self.Files else (self.Files[0] if self.Files else None))
        self.Set_status(f'{len(self.Files)} file(s) in {folder}')

    def _File_selected(self, value):
        # Copy the picked name into the Save As box, so "Save As" starts from it.
        if value:
            self.Filename_input.Text_input_element.value = value

    # ---------- buttons ----------
    def Load(self):
        path = self.Get_selected_path()
        if path is None:
            self.Set_status('No file selected', error=True)
            return
        self._Call(self.load_function, path, 'Loaded')

    def Save(self):
        path = self.Get_selected_path()
        if path is None:
            self.Set_status('No file selected, use Save As', error=True)
            return
        self._Call(self.save_function, path, 'Saved')

    def Save_As(self):
        name = (self.Filename_input.Text_input_element.value or '').strip()
        if not name:
            self.Set_status('Enter a filename for Save As', error=True)
            return
        extensions = self.Get_extensions()
        if not Path(name).suffix and extensions:
            name += extensions[0]
        folder = self.Get_folder()
        if not folder.is_dir():
            self.Set_status(f'Folder not found: {folder}', error=True)
            return
        path = folder / name
        if self._Call(self.save_function, path, 'Saved'):
            self.Refresh()
            if path.name in self.Files:
                self.File_select.set_value(path.name)
            self.Set_status(f'Saved {path}')

    def _Call(self, function, path, verb):
        # verb is 'Loaded' or 'Saved', used in the status line.
        action = 'Load' if verb == 'Loaded' else 'Save'
        if function is None:
            self.Set_status(f'No {action.lower()} function set', error=True)
            return False
        try:
            function(path)
        except Exception as e:
            self.Set_status(f'{action} {path.name} failed: {e}', error=True)
            return False
        self.Set_status(f'{verb} {path}')
        return True


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

                data = pd.read_csv(EXAMPLE_DATA_DIR / 'test_data.csv')
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