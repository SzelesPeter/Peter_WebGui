#Imports for the GUI to work:
from nicegui import ui
from datetime import datetime

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
            border_color = "#FFFFFF",
            content=card_content
        )

    ui.timer(0.001, Time_update)
    ui.timer(0.1, Blink)

ui.run()