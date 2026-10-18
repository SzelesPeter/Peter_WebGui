from nicegui import ui
import WebGui_Visuals as WGV
#For data
import pandas as pd
#For custom colored input elements
import uuid
# For testing graphs
from math import sin
import numpy as np
import random

import sys, os


class Chart:
    def __init__(self, name = '', xaxis_name = '', yaxis_name = '', width=WGV.Default_box_width, height=WGV.Default_box_height, background_color = WGV.Default_page_color, grid_color = WGV.Default_background_color, text_color = WGV.Default_border_color):

        self.Options = {
            'animation': False,
            'title': {
                'text': name,
                'top': '0',
                'left': 'center',
                'textStyle': {'color': text_color}
            },
            'legend': {
                'top': 20,
                'left': 70,
                'textStyle': {'color': text_color}
            },

            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross',
                },
            },

            'backgroundColor': background_color,
            'xAxis': {
                'type': 'value',
                'name': xaxis_name,

                # Automatic range
                'max': 'dataMax',
                'min': 'dataMin',

                'axisLabel': {
                    'show': True,
                    'textStyle': {'color': text_color}
                },

                'axisLine': {'lineStyle': {'color': text_color}},

                'splitLine': {
                    'show': True,
                    'lineStyle': {'color': grid_color}
                },
            },
            'yAxis': {
                'type': 'value',
                'name': yaxis_name,

                'min': 'dataMin',
                'max': 'dataMax',

                'axisLabel': {
                    'show': True,
                    'textStyle': {'color': text_color}
                },

                'axisLine': {'lineStyle': {'color': text_color}},

                'splitLine': {
                    'show': True,
                    'lineStyle': {'color': grid_color}
                },
            },
            'grid': {
                'left': 40,
                'right': 40,
                'top': 40,
                'bottom': 40,
                'containLabel': False,
            },
            'series': [],
        }

        self.Echart_element = ui.echart(self.Options).style(f'width: {WGV.Number_to_Pixel(width)}; height: {WGV.Number_to_Pixel(height)};')

    def set_xaxis_range(self, min: int = None, max: int = None):
        if (min != None):
            self.Echart_element.options['xAxis']['min'] = str(min)
        else:
            self.Echart_element.options['xAxis']['min'] = 'dataMin'
        if (max != None):
            self.Echart_element.options['xAxis']['max'] = str(max)
        else:
            self.Echart_element.options['xAxis']['max'] = 'dataMax'

    def set_yaxis_range(self, min: int = None, max: int = None):
        if (min != None):
            self.Echart_element.options['yAxis']['min'] = str(min)
        else:
            self.Echart_element.options['yAxis']['min'] = 'dataMin'
        if (max != None):
            self.Echart_element.options['yAxis']['max'] = str(max)
        else:
            self.Echart_element.options['yAxis']['max'] = 'dataMax'

    def add_trace(self, name, data, digital = False, color = None, lineWidth = 1, symbolsize = 0, symbol = 'circle', showLabel = False, fillArea = False):
        exists = False
        settings = {
                    'name': name,
                    'type': 'line',
                    'data': data,
                    'lineStyle': {
                        'width': lineWidth,
                    },
                    'symbol': symbol,
                    'symbolSize': symbolsize,
                    'showSymbol': True,
                    'label': {
                        'show': showLabel,
                    },
                }
        if fillArea:
            settings['areaStyle'] = {}
        if color != None:
            settings['lineStyle']['color'] = color
            settings['itemStyle'] = {}
            settings['itemStyle']['color'] = color
        if digital:
            settings['step'] = 'end'
             
        
        for trace in self.Echart_element.options['series']:
            if trace['name'] == name:
                self.Echart_element.options['series'].remove(trace)
                self.Echart_element.options['series'].append(settings)
                exists = True
        if exists == False:
            self.Echart_element.options['series'].append(settings)
        self.Echart_element.update()
        return exists



    def remove_trace(self, name):
        if name != 'no trace found':
            for trace in self.Echart_element.options['series']:
                        if trace['name'] == name:
                            self.Echart_element.options['series'].remove(trace)
            self.Echart_element.update()

    def remove_all_traces(self):
        self.Echart_element.options['series'] = []
        self.Echart_element.update()

    def get_trace_names(self):
        names = []
        for trace in self.Echart_element.options['series']:
            names.append(trace['name'])
        if names == []:
            return ['no trace found']
        else:
            return names

    def move_trace_x(self, name, value):
        if name != 'no trace found':
            for trace in self.Echart_element.options['series']:
                        if trace['name'] == name:
                            for point in trace['data']:
                                point[1] = point[1] + value
            self.Echart_element.update()

    def move_trace_y(self, name, value):
        if name != 'no trace found':
            for trace in self.Echart_element.options['series']:
                        if trace['name'] == name:
                            for point in trace['data']:
                                point[0] = point[0] + value
            self.Echart_element.update()

    def update_from_df(self, df):
        self.remove_all_traces()

        # Every odd column (0-based index) is a time column,
        # followed by its corresponding voltage column.
        for i in range(0, len(df.columns) - 1, 2):
            time_col = df.columns[i]
            voltage_col = df.columns[i + 1]

            valid = df[time_col].notna() & df[voltage_col].notna()

            data = [
                [x, y]
                for x, y in zip(
                    df.loc[valid, time_col],
                    df.loc[valid, voltage_col]
                )
            ]

            self.add_trace(
                name=str(voltage_col),
                data=data,
                digital=False,
                symbol='none',
                lineWidth=2
            )

class Manager_Basic:
    def __init__(self, name = '', save_path = '', save_name = '', load_path = '', load_name = '', xaxis_name = '', yaxis_name = '', width=WGV.Default_box_width, height=WGV.Default_box_height, background_color = WGV.Default_page_color, grid_color = WGV.Default_background_color, text_color = WGV.Default_border_color):
        with WGV.Card(name= name, width=width, height=height):
            self.save_path = save_path
            self.save_name = save_name
            self.load_path = load_path
            self.load_name = load_name
            self.df = pd.DataFrame()
            self.Chart_1 = Chart(name = '', xaxis_name= 'X', yaxis_name= 'Y', width=width-40, height=height/2-50)
            self.Grid_1 = WGV.Grid(data=self.df,width= 960,height=height/2-250, editable = True)

            with ui.row():
                B_update = WGV.Button(lambda: self.Update_Data_from_Grid(), name='Update', width= 120)
                WGV.Create_Label_Left_Bold(text = 'Trace name:', width = 90)
                self.TI_new_trace = WGV.Text_input(width = 200)
                B_new_trace = WGV.Button(lambda: self.new_trace(self.TI_new_trace.Text_input_element.value), name='New Trace', width= 160)
                B_new_row = WGV.Button(lambda: self.new_row(), name='New Row', width= 160)

            with ui.row():
                WGV.Create_Label_Left_Bold(text = 'Save path:', width = 80)
                self.TI_save_path = WGV.Text_input(width = 340)
                self.TI_save_path.Text_input_element.value = self.save_path
                WGV.Create_Label_Left_Bold(text = 'Save name:', width = 90)
                self.TI_save_name = WGV.Text_input(width = 200)
                self.TI_save_name.Text_input_element.value = self.save_name
                B_save = WGV.Button(lambda: self.Save_Data_to_File(), name='Save to file', width= 170)
            with ui.row():
                WGV.Create_Label_Left_Bold(text = 'Load path:', width = 80)
                self.TI_load_path = WGV.Text_input(width = 340)
                self.TI_load_path.Text_input_element.value = self.load_path
                WGV.Create_Label_Left_Bold(text = 'Load name:', width = 90)
                self.TI_load_name = WGV.Text_input(width = 200)
                self.TI_load_name.Text_input_element.value = self.load_name
                B_load = WGV.Button(lambda: self.Load_Data_from_File(), name='Load from file', width= 170)

    def new_trace(self, name):
        self.df[name+'_t'] = None
        self.df[name] = None
        self.Grid_1.update_from_df(self.df)
    def new_row(self):
        new_row = {column: None for column in self.df.columns}
        self.df.loc[len(self.df)] = new_row
        self.Grid_1.update_from_df(self.df)
    async def Update_Data_from_Grid(self):
        self.df = await self.Grid_1.data_to_df()
        self.Chart_1.update_from_df(self.df)
    def Save_Data_to_File(self):
        self.save_path = self.TI_save_path.Text_input_element.value
        self.save_name = self.TI_save_name.Text_input_element.value
        self.df.to_csv(os.path.join(self.save_path, self.save_name + ".csv"), sep=",", index=False)
    def Load_Data_from_File(self):
        self.load_path = self.TI_load_path.Text_input_element.value
        self.load_name = self.TI_load_name.Text_input_element.value
        self.df = pd.read_csv(os.path.join(self.load_path, self.load_name + ".csv"), sep=",")
        self.Chart_1.update_from_df(self.df)
        self.Grid_1.update_from_df(self.df)

    def Add_measurement_point(self, name, x, y):
        if name not in self.df.columns:
            self.df[name+'_t'] = None
            self.df[name] = None
        empty_rows = self.df[name+'_t'].isna()
        if empty_rows.any():
            # Overwrite the first empty value
            idx = self.df.index[empty_rows][0]
            self.df.loc[idx, name+'_t'] = x
            self.df.loc[idx, name] = y
        else:
            # Create a new row
            new_row = {column: None for column in self.df.columns}
            new_row[name+'_t'] = x
            new_row[name] = y
            self.df.loc[len(self.df)] = new_row

        self.Chart_1.update_from_df(self.df)
        self.Grid_1.update_from_df(self.df)


"""
counter = 0


@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style(f'background-color: {WGV.Default_page_color};')

    with WGV.Card(name= 'Charts', width='2050px', height='440px'):
        with ui.row().classes('gap-0 p-0 m-0'): # column with no spaceing
            chart1 = Chart(name = 'Chart 1', xaxis_name= 'X', yaxis_name= 'Y')
            chart2 = Chart(name = 'Chart 2')


    

    

    def create_data():
        data = []
        x = list(range(100))
        rand1 = random.randint(1, 50)
        rand2 = random.randint(1, 50)
        rand3 = random.randint(-180, 180)
        for i in x:
            data.append([i, rand1*sin((i/rand2)+(rand3/100)) + (random.randint(-100, 100)/200)])
        return data

    def create_digital_data():
            data = []
            x = list(range(10))
            for i in x:
                data.append([i, random.randint(0, 1)])
            return data

    
    L1 = WGV.Create_Label('Chart1')
    with ui.row():
        B3 = WGV.Button(lambda: chart1.remove_all_traces(), name='Remove all')
        B5 = WGV.Button(lambda: chart1.add_trace('Same', create_digital_data(), digital= True), name='Same random')


    L2 = WGV.Create_Label('Chart2')
    with ui.row():
        B1 = WGV.Button(lambda: chart2.set_xaxis_range(-50, 200), name='Set xAxes')
        B2 = WGV.Button(lambda: chart2.set_yaxis_range(-50, 200), name='Set yAxes')

    with ui.row():
        B3 = WGV.Button(lambda: chart2.remove_all_traces(), name='Remove all')
        B4 = WGV.Button(lambda: button_press(), name='New random')
        B5 = WGV.Button(lambda: chart2.add_trace('Same', create_data()), name='Same random')
        B6 = WGV.Button(lambda: chart2.set_yaxis_range(-50, 200), name='Set yAxes')
        def D1_funct(name):
            chart2.remove_trace(name)
            D1.set_options(chart2.get_trace_names())
            D2.set_options(chart2.get_trace_names())
        D1 = WGV.Create_Dropdown_Card(function_to_call = D1_funct, options = chart2.get_trace_names())

    with ui.row():
        selected_trace = chart2.get_trace_names()[0]
        def D2_funct(name):
            selected_trace = name
            L3.set_text(selected_trace)
        D2 = WGV.Create_Dropdown_Card(function_to_call = D2_funct, options = chart2.get_trace_names())
        L3 = WGV.Create_Label(selected_trace, '30px')
        N1 =  WGV.Number_input()
        B7 = WGV.Button(lambda: chart2.move_trace_x(D2.value, N1.Number_input_element.value), name='Move trace X')
        N2 =  WGV.Number_input()
        B8 = WGV.Button(lambda: chart2.move_trace_y(D2.value, N2.Number_input_element.value), name='Move trace Y')

    def button_press():
        global counter
        chart2.add_trace(str(counter), create_data())
        counter = counter+1
        D1.set_options(chart2.get_trace_names())
        D2.set_options(chart2.get_trace_names())





ui.run()

"""




