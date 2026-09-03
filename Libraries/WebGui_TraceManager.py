from nicegui import ui
import WebGui_Visuals
#For data
import pandas as pd
#For custom colored input elements
import uuid
# For testing graphs
from math import sin



class Chart:
    def __init__(self):
        self.traces = {}

        self.element = ui.echart({
            'backgroundColor': 'black',
            'xAxis': {
                'type': 'category',
                'axisLine': {'lineStyle': {'color': 'white'}},
                'splitLine': {
                    'lineStyle': {
                        'color': "#626035"
                    }
                },
                'splitLine': {'show': True},
                'axisLabel': {'show': True},
                'axisLabel': {'color': 'white'},
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {'lineStyle': {'color': 'white'}},
                
                'splitLine': {
                    'lineStyle': {
                        'color': "#626035"
                    }
                },
    
                'axisLabel': {'color': 'white'},
            },
            'series': [],
        })

    def add_trace(self, name, x, y):
        self.traces[name] = {
            'name': name,
            'type': 'line',
            'data': y,
        }

        self.element.options['xAxis']['data'] = x
        self._refresh()

    def remove_trace(self, name):
        self.traces.pop(name, None)
        self._refresh()

    def remove_all_traces(self):
        self.traces.clear()
        self._refresh()

    def _refresh(self):
        self.element.options['series'] = list(self.traces.values())
        self.element.update()


chart = Chart()


x = list(range(100))

chart.add_trace(
    'signal 1',
    x,
    [i * 0.5 for i in x],
)

chart.add_trace(
    'signal 2',
    x,
    [i * 0.01 for i in x],
)

ui.button(
    'Remove signal 1',
    on_click=lambda: chart.remove_trace('signal 1'),
)

ui.button(
    'Remove all',
    on_click=lambda: chart.remove_all_traces(),
)

ui.button(
    'Add signal 1',
    on_click=lambda: chart.add_trace('signal 1', list(range(100)), [i * 0.05 for i in list(range(100))]),
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