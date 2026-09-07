from nicegui import ui
import WebGui_Visuals as WGV
#For data
import pandas as pd
#For custom colored input elements
import uuid
# For testing graphs
from math import sin
import numpy as np


class Chart:
    def __init__(self, width=WGV.Default_box_width, height=WGV.Default_box_height, background_color = WGV.Default_page_color, grid_color = WGV.Default_border_color, text_color = WGV.Default_border_color):

        self.Options = {
            'legend': {
                'top': 50,
                'left': 50,
            },
            'backgroundColor': 'black',
            'xAxis': {
                'type': 'value',
                'min': '0',
                'max': '100',
            },
            'yAxis': {
                'type': 'value',
                'min': '-20',
                'max': '80',
            },
            'grid': {
                'left': 40,
                'right': 20,
                'top': 20,
                'bottom': 40,
                'containLabel': False,
            },
            'series': [{
                    'name': 'Data',
                    'type': 'line',
                    'data': [
                        [10, 5],
                        [20, 15],
                        [40, 10],
                        [80, 30],
                    ],
                    'step': 'end',
                    'symbol': 'none',
                },
                {
                    'name': 'Data2',
                    'type': 'line',
                    'data': [
                        [10, 15],
                        [20, 25],
                        [30, 20],
                        [40, 40],
                    ],
                    'step': 'end',
                    'symbol': 'none',
            }],
        }

        self.Echart_element = ui.echart(self.Options).style('width: 800px; height: 200px;')
    def add_trace(self, name, data):
        self.Echart_element.options['series'].append({
            'name': name,
            'type': 'line',
            'data': data,
        })
        self.Echart_element.update()

    def remove_trace(self):
        self.Echart_element.options['series'].pop()
        self.Echart_element.update()

    def remove_all_traces(self):
        self.Echart_element.options['series'] = []
        self.Echart_element.update()









with ui.column().classes('gap-0 p-0 m-0'): # column with no spaceing









    chart2 = Chart()

x = list(range(100))

data1 = []
data2 = []
data3 = []

for i in x:
    data1.append([i, i ])
    data2.append([i, i * 0.5])
    data3.append([i, 10*sin(i/10)])

chart2.add_trace(
    'signal 1',
    data1
)

chart2.add_trace(
    'signal 2',
    data2
)

ui.button(
    'Remove signal 1',
    on_click=lambda: chart2.remove_trace(),
)

ui.button(
    'Remove all',
    on_click=lambda: chart2.remove_all_traces(),
)

ui.button(
    'Add signal 1',
    on_click=lambda: chart2.add_trace('signal 1', data3),
)



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