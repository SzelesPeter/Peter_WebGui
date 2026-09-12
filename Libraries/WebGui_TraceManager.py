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
                'top': 50,
                'left': 50,
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

        self.Echart_element = ui.echart(self.Options).style(f'width: {width}; height: {height};')

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

# ---------- TEST CARD ----------
def test_card_content():

    points = 120
    phase = 0

    x = list(range(points))

    chart = ui.echart({
        'backgroundColor': 'black',

        'animation': False,

        'xAxis': {
            'type': 'category',
            'data': x,
            'axisLine': {'lineStyle': {'color': 'white'}},
            'splitLine': {'show': False},
            'axisLabel': {'show': False},
        },

        'yAxis': {
            'type': 'value',
            'min': -1.5,
            'max': 1.5,

            'axisLine': {'lineStyle': {'color': 'white'}},

            'splitLine': {
                'lineStyle': {
                    'color': '#333333'
                }
            },

            'axisLabel': {'color': 'white'},
        },

        'legend': {
            'textStyle': {
                'color': 'white'
            }
        },

        'series': [
            {
                'name': 'Wave 1',
                'type': 'line',
                'data': [],
                'smooth': True,
                'showSymbol': False,

                'lineStyle': {
                    'width': 3,
                    'color': '#ffff00'
                },
            },
            {
                'name': 'Wave 2',
                'type': 'line',
                'data': [],
                'smooth': True,
                'showSymbol': False,

                'lineStyle': {
                    'width': 3,
                    'color': '#3399ff'
                },
            }
        ]
    }).style('width: 100%; height: 100%; margin-top: 10px;')

    def update_chart():
        nonlocal phase

        y1 = [sin(i * 0.15 + phase) for i in x]
        y2 = [0.7 * sin(i * 0.15 + phase + 1.8) for i in x]

        chart.options['series'][0]['data'] = y1
        chart.options['series'][1]['data'] = y2

        chart.update()

        phase += 0.15

    update_chart()

    # Update every 50 ms
    ui.timer(0.05, update_chart)



@ui.page('/')
def main_page():
    # Black page background
    ui.query('body').style('background-color: black;')

    WebGui_Visuals.Create_Card(
        'TEST',
        width='700px',
        height='420px',
        content=test_card_content
    )
ui.run()
"""