"""Five-page demo app: a WGV.Page_Selector card on the left switches between pages.

Each page is its own URL (/, /chart, /data, /controls, /about), registered with WGV.Page. The selector's buttons
call ui.navigate.to, so the browser's back/forward buttons and bookmarks work. To add a page, write a builder
function and add it to PAGES.
"""
import math

import pandas as pd
from nicegui import ui

from peter_webgui import visuals as WGV
from peter_webgui import trace_manager as TM
from peter_webgui import timing as Time


# ----------------------------------------------------------------------------------------------------------
# Page contents
# ----------------------------------------------------------------------------------------------------------

def home_page():
    with WGV.Card('Home', width=1000, height=200):
        WGV.Create_Label_Left('Use the buttons on the left to switch between the five pages.', width=900)
        clock = WGV.Create_Label_Left('', font_size=40, width=900, color=WGV.Default_color)
        ui.timer(0.1, lambda: clock.set_text(Time.Get_Time_text()))


def chart_page():
    with WGV.Card('Chart', width=1000, height=450):
        chart = TM.Chart(name='Sine', xaxis_name='x', yaxis_name='y', width=960, height=380)
        chart.add_trace('sin(x)', [[x / 10, math.sin(x / 10)] for x in range(0, 200)], symbol='none', lineWidth=2)
        chart.add_trace('cos(x)', [[x / 10, math.cos(x / 10)] for x in range(0, 200)], symbol='none', lineWidth=2)


def data_page():
    df = pd.DataFrame({
        'Channel': ['101', '102', '103', '104'],
        'Measurement': ['DC V', 'AC V', 'Ω 2W', 'DC I'],
        'Value': [1.234, 0.567, 1000.0, 0.012],
    })
    with WGV.Card('Data', width=1000, height=400):
        WGV.Grid(data=df, width=960, editable=True)


def controls_page():
    with WGV.Card('Controls', width=1000, height=300):
        status = WGV.Create_Label_Left('Nothing pressed yet', width=900)
        with ui.row():
            WGV.Button(lambda: status.set_text('Button pressed at ' + Time.Get_Time_text()), name='Press me', width=180)
            WGV.Checkbox(name='Option', function_when_changed=lambda v: status.set_text(f'Option: {v}'))
        progress = WGV.Progress_bar(width=900)
        progress.Set_value(0.42)


def about_page():
    with WGV.Card('About', width=1000, height=200):
        WGV.Create_Label_Left('peter-webgui multipage demo', font_size=24, width=900)
        WGV.Create_Label_Left('Built with WGV.Page, WGV.Card and WGV.Button on NiceGUI.', width=900)


# (path, button text, builder)
PAGES = [
    ('/',         'Home',     home_page),
    ('/chart',    'Chart',    chart_page),
    ('/data',     'Data',     data_page),
    ('/controls', 'Controls', controls_page),
    ('/about',    'About',    about_page),
]


def register_page(path, name, builder):
    # A separate function per page so each page function closes over its own path/builder. Default arguments
    # (def page(path=path)) would not work here: ui.page would turn them into query parameters.
    @WGV.Page(path, title=f'Multipage demo - {name}', layout='row')
    def page():
        WGV.Page_Selector([(p, n) for p, n, _ in PAGES], current_path=path)
        with ui.column():
            builder()


def register_pages():
    for path, name, builder in PAGES:
        register_page(path, name, builder)


register_pages()


def main():
    ui.run(title='Multipage demo', reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
