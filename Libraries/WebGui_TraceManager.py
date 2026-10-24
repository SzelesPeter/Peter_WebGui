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
import numpy as np

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

class General_Data:
    def __init__(self, collums):
        self.df = pd.DataFrame()
        self.collums = collums
        self.New_Trace()        
        self.changed = False
    def Replace_All(self, df):
        self.df = df
        self.changed = True
    def New_Trace(self):
        df = pd.DataFrame()
        self.df = df
        for column in self.collums:
            self.df[column] = None
        self.changed = True
    def New_Row(self):
        new_row = {column: None for column in self.df.columns}
        self.df.loc[len(self.df)] = new_row
        self.changed = True
    def Save_Data_to_File(self, file_name, file_path):
        self.df.to_csv(os.path.join(file_path, file_name + ".csv"), sep=",", index=False)
    def Load_Data_from_File(self, file_name, file_path):
        self.df = pd.read_csv(os.path.join(file_path, file_name + ".csv"), sep=",")
        self.changed = True
    def Add_measurement_point(self, data):
        self.df.loc[len(self.df)] = data
        self.changed = True
    def Get_Trace_Data(self, name):
        return self.df[name].dropna(subset=[name]).reset_index(drop=True)
    def Reset_Changed(self):
        self.changed = False

class Trace_Data:
    def __init__(self, x_unit, y_unit):
        self.df = pd.DataFrame()
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.changed = False
    def Name_to_Xname(self, name):
        return name+'_x'+'['+self.x_unit+']'
    def Name_to_Yname(self, name):
        return name+'_y'+'['+self.y_unit+']'
    def Xname_to_name(self, x_name):
        suffix = f"_x[{self.x_unit}]"
        if x_name.endswith(suffix):
            return x_name[:-len(suffix)]
        raise ValueError(f"Invalid X column name: {x_name}")
    def Yname_to_name(self, y_name):
        suffix = f"_x[{self.y_unit}]"
        if y_name.endswith(suffix):
            return y_name[:-len(suffix)]
        raise ValueError(f"Invalid X column name: {y_name}")
    def Replace_All(self, df):
        self.df = df
        self.changed = True
    def New_Trace(self, name):
        self.df[self.Name_to_Xname(name)] = None
        self.df[self.Name_to_Yname(name)] = None
        self.changed = True
    def Delete_Trace(self, name):
        x_col = self.Name_to_Xname(name)
        y_col = self.Name_to_Yname(name)
        self.df.drop(columns=[x_col, y_col], errors='ignore', inplace=True)
        self.changed = True
    def New_Row(self):
        new_row = {column: None for column in self.df.columns}
        self.df.loc[len(self.df)] = new_row
        self.changed = True
    def Save_Data_to_File(self, file_name, file_path):
        self.df.to_csv(os.path.join(file_path, file_name + ".csv"), sep=",", index=False)
    def Load_Data_from_File(self, file_name, file_path):
        self.df = pd.read_csv(os.path.join(file_path, file_name + ".csv"), sep=",")
        self.changed = True
    def Add_measurement_point(self, name, x, y):
        x_col = self.Name_to_Xname(name)
        y_col = self.Name_to_Yname(name)
        # Create the trace if it doesn't exist
        if x_col not in self.df.columns or y_col not in self.df.columns:
            self.df[x_col] = None
            self.df[y_col] = None
        # Find the first empty X position for this trace
        empty_rows = self.df[x_col].isna()
        if empty_rows.any():
            idx = self.df.index[empty_rows][0]
        else:
            # Append a new row without overwriting existing data
            idx = len(self.df)
            self.df.loc[idx] = {col: None for col in self.df.columns}
        self.df.loc[idx, x_col] = x
        self.df.loc[idx, y_col] = y
        self.changed = True
    def Get_Trace_Names(self):
        suffix = f"_x[{self.x_unit}]"
        return [
            column[:-len(suffix)]
            for column in self.df.columns
            if column.endswith(suffix)
        ]
    def Sum_Traces(self, trace1, trace2):
        new_trace = trace1+'+'+trace2
        x1_col = self.Name_to_Xname(trace1)
        y1_col = self.Name_to_Yname(trace1)
        x2_col = self.Name_to_Xname(trace2)
        y2_col = self.Name_to_Yname(trace2)
        # Check that both traces exist
        if not all(col in self.df.columns for col in
                   [x1_col, y1_col, x2_col, y2_col]):
            raise ValueError("One or both traces do not exist.")
        x_new_col = self.Name_to_Xname(new_trace)
        y_new_col = self.Name_to_Yname(new_trace)
        # Extract valid measurement points
        trace1_data = self.df[[x1_col, y1_col]].dropna().astype(float)
        trace2_data = self.df[[x2_col, y2_col]].dropna().astype(float)
        if len(trace1_data) == 0 or len(trace2_data) == 0:
            raise ValueError("Both traces must contain measurement points.")
        # Sort trace2 by X and remove duplicate X values
        trace2_data = (
            trace2_data.sort_values(x2_col)
            .drop_duplicates(subset=x2_col, keep="first")
        )
        x1 = trace1_data[x1_col].to_numpy()
        y1 = trace1_data[y1_col].to_numpy()
        x2 = trace2_data[x2_col].to_numpy()
        y2 = trace2_data[y2_col].to_numpy()
        if len(x2) < 2:
            raise ValueError(
                "Trace2 must contain at least two distinct X values "
                "for interpolation and extrapolation."
            )
        # Interpolate within the range and extrapolate outside it
        y2_interpolated = np.interp(x1, x2, y2)
        # Linear extrapolation below the minimum X
        below = x1 < x2[0]
        y2_interpolated[below] = (
            y2[0] + (x1[below] - x2[0])
            * (y2[1] - y2[0]) / (x2[1] - x2[0])
        )
        # Linear extrapolation above the maximum X
        above = x1 > x2[-1]
        y2_interpolated[above] = (
            y2[-1] + (x1[above] - x2[-1])
            * (y2[-1] - y2[-2]) / (x2[-1] - x2[-2])
        )
        # Create the summed trace
        result = pd.DataFrame({
            x_new_col: x1,
            y_new_col: y1 + y2_interpolated
        })
        # Store the result in the main DataFrame
        self.df[x_new_col] = np.nan
        self.df[y_new_col] = np.nan
        self.df.loc[trace1_data.index, x_new_col] = result[x_new_col].to_numpy()
        self.df.loc[trace1_data.index, y_new_col] = result[y_new_col].to_numpy()
        self.changed = True
    def Get_Trace_Data(self, name):
        x_col = self.Name_to_Xname(name)
        y_col = self.Name_to_Yname(name)
        if x_col not in self.df.columns or y_col not in self.df.columns:
            raise ValueError(f"Trace '{name}' does not exist.")
        return self.df[[x_col, y_col]].dropna(subset=[x_col, y_col]).reset_index(drop=True)
    def Add_Trace_Data(self, df):
        # Add new columns and replace existing columns with matching names
        self.df = self.df.reindex(
            columns=self.df.columns.union(df.columns, sort=False)
        )
        for column in df.columns:
            self.df[column] = df[column].reindex(self.df.index)
        self.changed = True
    def Interpolate_Trace(self, trace1, trace2):
        # Column names
        x1_col = self.Name_to_Xname(trace1)
        y1_col = self.Name_to_Yname(trace1)
        x2_col = self.Name_to_Xname(trace2)
        y2_col = self.Name_to_Yname(trace2)
        # Check that both traces exist
        for col in [x1_col, y1_col, x2_col, y2_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' does not exist.")
        new_name = trace2 + "_int"
        x_new_col = self.Name_to_Xname(new_name)
        y_new_col = self.Name_to_Yname(new_name)
        if x_new_col in self.df.columns or y_new_col in self.df.columns:
            raise ValueError(f"Trace '{new_name}' already exists.")
        # Extract valid data points
        data1 = self.df[[x1_col, y1_col]].dropna().astype(float)
        data2 = self.df[[x2_col, y2_col]].dropna().astype(float)
        if len(data2) < 2:
            raise ValueError("Trace2 must contain at least two valid points.")
        # Sort by X and remove duplicate X values
        data2 = (
            data2.sort_values(x2_col)
            .drop_duplicates(subset=x2_col, keep="first")
        )
        if len(data2) < 2:
            raise ValueError("Trace2 must have at least two distinct X values.")
        x1 = data1[x1_col].to_numpy()
        x2 = data2[x2_col].to_numpy()
        y2 = data2[y2_col].to_numpy()
        # Interpolate within the range
        y_interpolated = np.interp(x1, x2, y2)
        # Linear extrapolation below the range
        below = x1 < x2[0]
        y_interpolated[below] = (
            y2[0] + (x1[below] - x2[0])
            * (y2[1] - y2[0]) / (x2[1] - x2[0])
        )
        # Linear extrapolation above the range
        above = x1 > x2[-1]
        y_interpolated[above] = (
            y2[-1] + (x1[above] - x2[-1])
            * (y2[-1] - y2[-2]) / (x2[-1] - x2[-2])
        )
        # Create the new trace with matching X values
        self.df[x_new_col] = np.nan
        self.df[y_new_col] = np.nan
        self.df.loc[data1.index, x_new_col] = x1
        self.df.loc[data1.index, y_new_col] = y_interpolated
        self.changed = True
    def Reset_Changed(self):
        self.changed = False




class Manager_Basic:
    def __init__(
        self,
        trace_data,
        name='',
        save_path='',
        save_name='',
        load_path='',
        load_name='',
        width=WGV.Default_box_width,
        height=WGV.Default_box_height*2,
        background_color=WGV.Default_page_color,
        grid_color=WGV.Default_background_color,
        text_color=WGV.Default_border_color
    ):
        self.trace_data = trace_data

        self.save_path = save_path
        self.save_name = save_name
        self.load_path = load_path
        self.load_name = load_name

        with WGV.Card(name=name, width=width, height=height):

            self.Chart_1 = Chart(
                name='',
                xaxis_name=f'X [{trace_data.x_unit}]',
                yaxis_name=f'Y [{trace_data.y_unit}]',
                width=width - 40,
                height=height / 2 - 50
            )

            self.Grid_1 = WGV.Grid(
                data=self.trace_data.df,
                width=960,
                height=height / 2 - 250,
                editable=True
            )

            with ui.row():
                WGV.Button(
                    lambda: self.Update_Data_from_Grid(),
                    name='Update',
                    width=120
                )

                WGV.Create_Label_Left_Bold(
                    text='Trace name:',
                    width=90
                )

                self.TI_new_trace = WGV.Text_input(width=200)

                WGV.Button(
                    lambda: self.new_trace(
                        self.TI_new_trace.Text_input_element.value
                    ),
                    name='New Trace',
                    width=160
                )

                WGV.Button(
                    lambda: self.new_row(),
                    name='New Row',
                    width=160
                )

            with ui.row():
                WGV.Create_Label_Left_Bold(
                    text='Save path:',
                    width=80
                )
                self.TI_save_path = WGV.Text_input(width=340)
                self.TI_save_path.Text_input_element.value = self.save_path

                WGV.Create_Label_Left_Bold(
                    text='Save name:',
                    width=90
                )
                self.TI_save_name = WGV.Text_input(width=200)
                self.TI_save_name.Text_input_element.value = self.save_name

                WGV.Button(
                    lambda: self.Save_Data_to_File(),
                    name='Save to file',
                    width=170
                )

            with ui.row():
                WGV.Create_Label_Left_Bold(
                    text='Load path:',
                    width=80
                )
                self.TI_load_path = WGV.Text_input(width=340)
                self.TI_load_path.Text_input_element.value = self.load_path

                WGV.Create_Label_Left_Bold(
                    text='Load name:',
                    width=90
                )
                self.TI_load_name = WGV.Text_input(width=200)
                self.TI_load_name.Text_input_element.value = self.load_name

                WGV.Button(
                    lambda: self.Load_Data_from_File(),
                    name='Load from file',
                    width=170
                )

        # Display the initial data
        self.Refresh_Display()

    def Refresh_Display(self):
        """Refresh both the grid and the chart."""
        self.Grid_1.update_from_df(self.trace_data.df)
        self.Chart_1.update_from_df(self.trace_data.df)

    def new_trace(self, name):
        """Create a new trace using Trace_Data."""
        if not name:
            return

        if name in self.trace_data.Get_Trace_Names():
            raise ValueError(f"Trace '{name}' already exists.")

        self.trace_data.New_Trace(name)
        self.Refresh_Display()

    def new_row(self):
        """Add a new row using Trace_Data."""
        self.trace_data.New_Row()
        self.Refresh_Display()

    async def Update_Data_from_Grid(self):
        """Save grid edits back into Trace_Data."""
        updated_df = await self.Grid_1.data_to_df()
        self.trace_data.Replace_All(updated_df)
        self.Refresh_Display()

    def Save_Data_to_File(self):
        """Save the Trace_Data object to CSV."""
        self.save_path = self.TI_save_path.Text_input_element.value
        self.save_name = self.TI_save_name.Text_input_element.value

        self.trace_data.Save_Data_to_File(
            self.save_name,
            self.save_path
        )

    def Load_Data_from_File(self):
        """Load CSV data into Trace_Data and refresh the display."""
        self.load_path = self.TI_load_path.Text_input_element.value
        self.load_name = self.TI_load_name.Text_input_element.value

        self.trace_data.Load_Data_from_File(
            self.load_name,
            self.load_path
        )

        self.Refresh_Display()

    def Add_measurement_point(self, name, x, y):
        """Add a measurement point and refresh the display."""
        self.trace_data.Add_measurement_point(name, x, y)
        self.Refresh_Display()

class Manager_Basic_No_Buttons:
    def __init__(
        self,
        trace_data,
        name='',
        save_path='',
        save_name='',
        load_path='',
        load_name='',
        width=WGV.Default_box_width,
        height=WGV.Default_box_height*2,
        background_color=WGV.Default_page_color,
        grid_color=WGV.Default_background_color,
        text_color=WGV.Default_border_color
    ):
        self.trace_data = trace_data

        self.save_path = save_path
        self.save_name = save_name
        self.load_path = load_path
        self.load_name = load_name

        with WGV.Card(name=name, width=width, height=height):
            with ui.row():
                self.Chart_1 = Chart(
                    name='',
                    xaxis_name=f'X [{trace_data.x_unit}]',
                    yaxis_name=f'Y [{trace_data.y_unit}]',
                    width=width /3*2 - 40,
                    height=height - 50
                )

                self.Grid_1 = WGV.Grid(
                    data=self.trace_data.df,
                    width=width /3 -40,
                    height=height - 50,
                    editable=True
                )
        # Display the initial data
        self.Refresh_Display()

    def Refresh_Display(self):
        """Refresh both the grid and the chart."""
        self.Grid_1.update_from_df(self.trace_data.df)
        self.Chart_1.update_from_df(self.trace_data.df)

    def new_trace(self, name):
        """Create a new trace using Trace_Data."""
        if not name:
            return

        if name in self.trace_data.Get_Trace_Names():
            raise ValueError(f"Trace '{name}' already exists.")

        self.trace_data.New_Trace(name)
        self.Refresh_Display()

    def new_row(self):
        """Add a new row using Trace_Data."""
        self.trace_data.New_Row()
        self.Refresh_Display()

    async def Update_Data_from_Grid(self):
        """Save grid edits back into Trace_Data."""
        updated_df = await self.Grid_1.data_to_df()
        self.trace_data.Replace_All(updated_df)
        self.Refresh_Display()

    def Save_Data_to_File(self):
        """Save the Trace_Data object to CSV."""
        self.save_path = self.TI_save_path.Text_input_element.value
        self.save_name = self.TI_save_name.Text_input_element.value

        self.trace_data.Save_Data_to_File(
            self.save_name,
            self.save_path
        )

    def Load_Data_from_File(self):
        """Load CSV data into Trace_Data and refresh the display."""
        self.load_path = self.TI_load_path.Text_input_element.value
        self.load_name = self.TI_load_name.Text_input_element.value

        self.trace_data.Load_Data_from_File(
            self.load_name,
            self.load_path
        )

        self.Refresh_Display()

    def Add_measurement_point(self, name, x, y):
        """Add a measurement point and refresh the display."""
        self.trace_data.Add_measurement_point(name, x, y)
        self.Refresh_Display()


if __name__ in {"__main__", "__mp_main__"}:
    @ui.page('/')
    def main_page():
        # Black page background
        ui.query('body').style(f'background-color: {WGV.Default_page_color};')

        trace_data = Trace_Data(
            x_unit='m',
            y_unit='V'
        )

        trace_data.Add_measurement_point('Trace1', 1, 10)
        trace_data.Add_measurement_point('Trace1', 2, 20)
        trace_data.Add_measurement_point('Trace1', 3, 30)
        trace_data.Add_measurement_point('Trace1', 4, 40)
        trace_data.Add_measurement_point('Trace2', 3, 10)
        trace_data.Add_measurement_point('Trace2', 4, 50)
        trace_data.Interpolate_Trace('Trace1', 'Trace2')
        trace_data.Sum_Traces('Trace1', 'Trace2')

        manager = Manager_Basic(
            trace_data=trace_data,
            name='Measurement Manager',
            save_path='/home/fujitsu/Desktop/tmp/',
            save_name='measurement'
        )

    ui.run()



