'''
from nicegui import ui

with ui.element('div').style(
    'position: relative; width: 400px; height: 200px;'
):
    # Background SVG
    ui.html("""
    <svg viewBox="0 0 400 200"
         width="400" height="200"
         style="position:absolute;left:0;top:0">
        <rect x="20" y="30" width="300" height="130"
              fill="#f5f5f5" stroke="black"/>
        <circle cx="180" cy="95" r="35"
                fill="white" stroke="black"/>
        <text x="180" y="100"
              text-anchor="middle" font-size="14">
            Bit 3
        </text>
    </svg>
    """, sanitize=False).style(
        'position:absolute;left:0;top:0;'
    )

    # Overlay button
    ui.button('Toggle', on_click=lambda: ui.notify('Bit 3 clicked')) \
        .style(
            'position:absolute;left:145px;top:75px;'
            'z-index:10;'
        )

ui.run()
'''

from nicegui import ui
from html import escape
import math

# --------------------------------------------------
# Diagram configuration
# --------------------------------------------------

WIDTH, HEIGHT = 1400, 850

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
# SVG drawing helpers
# --------------------------------------------------
class SVG:
    def __init__(self, name: str = None, width = WIDTH, height = HEIGHT, Default_background_color = "#FFFFFF", Default_border_color = "#000000"):
        self.name = name
        self.Default_background_color = Default_background_color
        self.Default_border_color = Default_border_color
        self.svg_parts = []
        self.svg = ""
        self.add(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" '
            f'width="100%" style="display:block;background:white">'
        )
    def add(self, content):
        self.svg_parts.append(content)
    def end(self):
        self.add("</svg>")
        self.svg = "".join(self.svg_parts)
    def delete_all(self):
        self.svg_parts = []
    def line(self, x1, y1, x2, y2, width=1, color="#222"):
        self.add(
            f'<line x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}"/>'
        )
    def rect(self, x, y, w, h, fill="white", stroke="#222"):
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
    def text(self, x, y, value, size=16, anchor="start",
             weight="normal", color="#222", rotate=None):
        transform = (
            f' transform="rotate({rotate} {x} {y})"'
            if rotate is not None else ""
        )
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}"{transform}>'
            f'{escape(value)}</text>'
        )
    def logic_gate(self, cx, cy):
        # OR-like convergence symbol used in the reference
        self.add(
            f'<circle cx="{cx}" cy="{cy}" r="37" '
            'fill="white" stroke="#222" stroke-width="1.2"/>'
        )
        self.add(
            f'<circle cx="{cx}" cy="{cy}" r="27" '
            'fill="white" stroke="#222" stroke-width="1"/>'
        )
        self.line(cx - 13, cy, cx + 13, cy)
        self.line(cx, cy - 13, cx, cy + 13)
    # --------------------------------------------------
    # Draw one 16-bit group
    # --------------------------------------------------
    def bit_group(self, 
        x, y, labels, title, side="left",
        gate_x=None, row_height=18.5,
    ):
        """
        x, y: top-left of group
        side: 'left' or 'right'
        gate_x: x position of convergence symbol
        """

        label_width = 275 if side == "left" else 180
        number_width = 26
        enable_width = 25

        label_x = x + label_width
        number_x = label_x + 5
        enable_x = number_x + number_width + 14

        first_y = y + 18
        group_height = row_height * 16

        if gate_x is None:
            gate_x = enable_x + enable_width + 170

        # Group heading
        self.text(x, y - 24, title, 25, weight="bold")

        # Number and enable columns
        self.rect(number_x, first_y - 14, number_width, group_height + 5)
        self.rect(enable_x, first_y - 14, enable_width, group_height + 5,
             fill="#e9e9e9")

        self.text(
            enable_x + enable_width / 2,
            first_y + group_height / 2 - 5,
            "enable",
            16,
            anchor="middle",
            rotate=-90,
        )

        # Draw all 16 bit positions
        for bit, label in enumerate(labels):
            yy = first_y + bit * row_height

            self.text(label_x, yy + 4, label, 15, anchor="end")
            self.line(label_x + 5, yy, number_x, yy)

            self.text(
                number_x + number_width / 2,
                yy + 4,
                str(bit),
                15,
                anchor="middle",
            )

            start_x = enable_x + enable_width
            start_y = yy

            # Lines converge towards the logic gate
            center_y = first_y + group_height / 2
            target_y = (
                center_y
                + (bit - 7.5) * (row_height * 0.82)
            )

            dx = gate_x - start_x
            dy = target_y - center_y
            length = math.hypot(dx, dy) or 1

            end_x = gate_x - 38 * dx / length
            end_y = center_y + 38 * dy / length

            self.line(start_x, start_y, end_x, end_y, width=0.9)

        gate_y = first_y + group_height / 2
        self.logic_gate(gate_x, gate_y)

        return {
            "left": x,
            "right": gate_x + 38,
            "top": y,
            "bottom": first_y + group_height,
            "gate_x": gate_x,
            "gate_y": gate_y,
            "number_x": number_x,
            "enable_x": enable_x,
        }


# --------------------------------------------------
# Compose the diagram
# --------------------------------------------------

SVG_1 = SVG()

# Outer frame
SVG_1.rect(4, 4, WIDTH - 8, HEIGHT - 8)

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




# --------------------------------------------------
# NiceGUI page
# --------------------------------------------------

ui.page_title("Status Register Diagram")



with ui.column().classes("w-full p-4 gap-3"):
    with ui.row().classes("w-full items-center justify-between"):
        ui.label("Status Register Viewer").classes(
            "text-2xl font-bold"
        )
        ui.button(
            "Download SVG",
            on_click=lambda: ui.download(
                content=svg.encode("utf-8"),
                filename="status-register.svg",
                media_type="image/svg+xml",
            ),
        )

    with ui.card().classes("w-full p-2"):
        ui.html(
            f'<div class="diagram-container">{svg}</div>',
            sanitize=False,
        ).classes("w-full")

ui.run(title="Status Register Viewer", reload=False)
