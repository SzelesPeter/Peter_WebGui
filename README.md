# Peter_WebGui

A universal web GUI for embedded projects and instrument automation, built on [NiceGUI](https://nicegui.io).

## Install

```bash
pip install .                 # from a clone
pip install -e .              # editable, for development
pip install git+https://github.com/<you>/Peter_WebGui.git
```

## Use

```bash
hp34401a-gui      # HP/Agilent 34401A multimeter GUI
hp34970a-gui      # HP/Agilent 34970A data logger GUI
```

Settings are stored as `<Name>_Settings.csv` in the **current working directory**.

```python
from peter_webgui import visuals as WGV, rs232, settings, trace_manager
from peter_webgui.drivers import agilent_34401a
```

## Layout

```
src/peter_webgui/
    visuals.py         NiceGUI widgets (cards, buttons, grids, ...)
    trace_manager.py   trace/plot data handling
    communicator.py    message queue + log GUI
    rs232.py           serial port wrapper + GUI
    settings.py        CSV-backed settings + editor GUI
    svg.py             SVG register/diagram viewer
    timing.py          time helpers
    drivers/           Agilent 34401A / 34970A drivers
    apps/              runnable GUIs (console scripts)
examples/              experiments and demos (not installed)
```
