# CLAUDE.md

Guidance for working in this repository.

## What this is

`peter-webgui`: a reusable [NiceGUI](https://nicegui.io) (>=3.0) widget library and instrument-automation toolkit, plus two GUI apps for old HP/Agilent bench instruments (34401A multimeter, 34970A data logger) that talk SCPI over RS-232. Python >=3.10, src layout, setuptools.

## Commands

```bash
source .venv/bin/activate          # venv already exists, package installed editable
pip install -e .[dev]              # (re)install; extras: ksp (krpc), usb (pyusb), dev
hp34401a-gui                       # console script -> peter_webgui.apps.hp34401a_gui:main
hp34970a-gui                       # console script -> peter_webgui.apps.hp34970a_gui:main
multipage-demo                     # 5-page navigation demo -> peter_webgui.apps.multipage_demo:main
delta-v1                           # Delta board app (Main, RS-232, I2C, SPI, RS-485, GPIO, CAN, Status) -> peter_webgui.apps.delta_v1:main
python -m peter_webgui.visuals     # widget demo page (the __main__ block)
python -m peter_webgui.trace_manager  # trace/chart demo page
python -m peter_webgui.instrument_visuals  # Numeric_Display demo on port 8082
python -m build                    # sdist + wheel into dist/
```

There are no tests yet (`pytest` is only listed in the `dev` extra). Nothing is checked in CI. The project is not a git repo at the moment.

Apps call `ui.run(reload=False)` and serve on NiceGUI's default port, 8080.

## Layout

```
src/peter_webgui/
  visuals.py        widget layer (imported everywhere as WGV)
  trace_manager.py  ECharts chart + pandas data containers (TM)
  communicator.py   SCPI request/response queue + log GUI
  rs232.py          pyserial wrapper + RS232_GUI
  settings.py       CSV-backed key/value settings + editor GUI
  instrument_visuals.py  instrument-level widgets (IV): Error_Log, Instrument_Finder, Numeric_Display
  svg.py            tiny SVG string builder (lines/rects/text/gates/bit groups)
  timing.py         timestamp + perf_counter helpers
  drivers/          agilent_34401a.py, agilent_34970a.py
  apps/             hp34401a_gui.py, hp34970a_gui.py, multipage_demo.py, delta_v1.py (entry points);
                    delta_buses.py: the Delta bus pages (Config_GUI, Bus_Log + one subclass per bus, help card, BUSES)
examples/           standalone experiments, not packaged (serial, USB, KSP/kRPC, SVG demo)
docs_legacy/        34970A user guide PDF
```

## Architecture

**Data flow for an instrument:**
`App` → `drivers.*.Instrument` → `SCPI_Message` → `Communicator.Message_out_request()` → queue → `RS232.Write_Line` … `RS232.Read_Line` → `Message_in_worker` → the callback the caller passed in.

- **Everything is asynchronous and uses callbacks.** Driver reads never return a value. `SCPI_Message.Read(Target_Function, *args)` sends `CMD? args` and the reply string is later passed to `Target_Function`. Chained reads, like `Instrument.Poll` → `Poll_2` → `Poll_3`, are continuation callbacks.
- **`Communicator`** (communicator.py) keeps two numpy object arrays: a request queue and an "in flight" list, capped by `max_number_of_messages_out`. Two worker methods must be pumped periodically:
  - `Message_out_worker` sends the next request, respecting `message_delay_after` (commands use 0.5 s).
  - `Message_in_worker` reads a line, pairs it FIFO with the oldest sent message, and handles timeouts. A request with `timeout == 0` gets no reply, so it is retired on the next empty read.
  - hp34401a pumps both workers from daemon threads (10 ms loop). hp34970a pumps them with `ui.timer(0.1, ...)`.
  - `Message_out_request(..., callback_args=(), callback_kwargs=None)` carries extra values with a request. The reply is delivered as `callback_function(message_in, *callback_args, **callback_kwargs)`.
  - The optional `generate_log_function` (one slot, `Set_generate_log_function`) feeds `Communicator_Log`, an AG Grid of all traffic. `Add_log_function` / `Remove_log_function` add further listeners, so several log widgets can watch one communicator.
  - `Communicator_Log_v2(name, communicator)` is a card with a multi-line command box (one command per line, where lines ending in `?` are queries) and a log grid with statuses OK / Sent / Timeout / Unexpected. It adds itself with `Add_log_function` (and removes itself when its browser tab's client is deleted) and refreshes its grid with its own timer. Subclasses can override `Columns`, `Highlight_statuses`, `Send_all` and `Log`, as `I2C_Log` in `apps/delta_v1.py` does. `python -m peter_webgui.communicator` runs a demo with a simulated instrument on port 8081.
- **Drivers** define every SCPI command as an attribute, e.g. `self.MEASure_VOLTage_DC = SCPI_Message(self, 'MEASure:VOLTage:DC')`. Use `.Write(*args)`, `.Read(cb, *args)`, `.Set()` (adds ` ON`) or `.Reset()` (adds ` OFF`). `Instrument.Interface` is the `Communicator`, not the serial port. Status registers are modeled by `SCPI_Status_Byte` / `SCPI_Status_Bit`, with event/enable values and "changed" flags that the GUI polls.
- **Large parts of both driver files are dead code inside triple-quoted strings**, an older synchronous API: 34401a from about line 551 to the end, 34970a from about line 453. Some methods in `SCPI_Message` (`Read_Bytes`, `Read_Bits`, …) are commented out the same way. Don't "fix" code inside those strings by mistake.
- **Settings** (settings.py): `Settings(name)` loads or creates `<cwd>/<name>.csv` with `Name,Value` columns.
  - `Get_setting(key, default)` returns the stored value, or registers the default. Values come back as strings or pandas scalars, so cast them (`float(...)`, `int(...)`).
  - `Update_from(key, getter)` registers a getter that `Update_settings()` pulls from when saving.
  - `Save_if_changed()` pulls the getters and writes the CSV only if something changed. `delta_v1` runs it from `app.timer(1, ...)`, so every input saves itself. Page widgets are rebuilt for each browser tab, so they write their values into a module-level `State` dict, and the getter reads from there.
  - `*_Settings.csv` is gitignored. The apps write `HP34401A_Settings.csv` / `HP34970A_Settings.csv` into whatever directory you launch from.
- **Apps run hardware/setup code at import time.** At module level they create the Settings, RS232, Communicator and Instrument objects and call `Communicator_1.Start()`. The UI is built in `@ui.page('/') main_page()`, with a `ui.timer` that refreshes the GUI. Importing an app module has side effects.

## Widget conventions (visuals.py)

- Dark theme constants: `Default_page_color` `#000000`, `Default_background_color` `#403636`, `Default_border_color` `#FFFFFF`, accent `Default_color` `#B12C2C`. Sizes are in pixels, passed as ints and turned into CSS by `Number_to_Pixel`.
- Classes wrap a NiceGUI element and expose it as `*_element`: `Button.Button_element`, `Grid.Grid_element`, `Text_input.Text_input_element`, `Number_input.Number_input_element`, `Card.Card_element`, `TM.Chart.Echart_element`. Reach through to these for NiceGUI APIs, e.g. `grid.Grid_element.options['rowData'] = df.to_dict('records')`.
- `Page(path, title=, background_color=, layout=None|'row'|'column', favicon=)` sets up a themed page. Use it as a decorator (`@WGV.Page('/', title=...)` registers the `@ui.page`) or as `with WGV.Page(...):` inside a page function. A module-level `with` is not supported, because NiceGUI rebuilds a page for every client. `favicon` (an emoji, an image path, a URL or inline SVG) only applies in decorator mode.
- `Page_Selector([(path, text), ...], current_path=)` is a 320 × 450 card (the same size as `RS232_GUI`) with one full-width navigation button per page. The current page's button uses the accent colour. See `apps/multipage_demo.py`.
- `Grid(data, column_width=None|px|{column: px})`: None fits the columns to the grid width. A number or a dict sets fixed widths. `Grid.Set_column_width(...)` changes them later. Colours come from AG Grid theme variables (`--ag-*`) set on the element, and the column-resize bars run the full height of the grid.
- `Card(name=...)` is a context manager: a bordered box with its title on the top edge. Lay out with `with WGV.Card(...): with ui.row(): ...`.
- Label helpers are functions, not classes: `Create_Label_Left/Right/Center[_Bold]`, `Create_Dropdown_Card[_With_Name]`, `Create_Radio_Button`.
- Blinking: append elements to `WGV.Blinkable`, set `.Blinking`, and run `ui.timer(0.1, WGV.Blink)` together with `ui.timer(..., WGV.Time_update)`.
- `SVG_Box(svg)` shows an `svg.SVG` builder. Rebuild `svg.svg` and call `.Update()` to redraw.
- Code style throughout is `Capitalized_Snake_Case` for methods and module aliases (`WGV`, `TM`, `RS232`, `Time`). Match it in new code.

## Trace data (trace_manager.py)

- `Trace_Data(x_unit, y_unit)` is one wide DataFrame with paired columns `<name>_x[<unit>]` / `<name>_y[<unit>]` per trace. `Add_measurement_point(name, x, y)` creates the trace if needed. It also offers `Sum_Traces` and `Interpolate_Trace`.
- `General_Data(columns)` is a plain row log, used by `Communicator_Log`.
- Both set a `.changed` flag. The GUI checks it in a timer, refreshes, then calls `Reset_Changed()`.
- `Chart.update_from_df` expects the alternating x/y column layout.
- `Manager_Basic` / `Manager_Basic_No_Buttons` combine chart, grid and save/load controls.

## Gotchas

- Port names are stored without a path (`ttyUSB0`, `COM3`). `rs232.Port_Path()` adds `/dev/` in front unless the OS is Windows (`rs232.Windows = os.name == 'nt'`, set automatically) or the name already starts with `/dev/`.
- `RS232.Find_IDE(maker, model, serial_no)` scans every port with `*IDN?`. It closes the port when done and returns `(port, idn_fields)`.
- Demo `__main__` blocks read and write files in `examples/data/` through `visuals.EXAMPLE_DATA_DIR`, which is worked out from the location of `__file__`. That only works from a source checkout or an editable install, not a wheel install.
