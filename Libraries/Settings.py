
import sys, os
here = os.path.dirname(sys.path[0])

import pandas as pd


class Settings:
    def __init__(self, name, path = here, debug = None):
        self.name = name
        self.path = path
        self.debug = debug
        self.df = pd.DataFrame({
            "Name": [],
            "Value": []
        })

        filename = os.path.join(self.path, self.name + ".csv")

        try:
            self.df = pd.read_csv(filename)

        except FileNotFoundError:
            self.df.to_csv(filename, index=False)

    def Get_setting(self, name, value):
        try:
            value = self.df.loc[self.df["Name"] == name, "Value"].iloc[0]
        except:
            self.df.loc[len(self.df)] = [name, value]
        return(value)
    
    def Set_setting(self, name, value):
        self.df = self.df.copy()
        mask = self.df["Name"] == name
        self.df.loc[mask, "Value"] = value

    def Save_to_default_file(self):
        self.df.to_csv(os.path.join(self.path, self.name + ".csv"), sep=",", index=False)

    def Read_from_default_file(self):
        self.df = pd.read_csv(os.path.join(self.path, self.name + ".csv"), sep=",", index=False)

    def Save_to_file(self, name, path = here):
        self.df.to_csv(os.path.join(path, name + ".csv"), sep=",", index=False)

    def Read_from_default_file(self, name, path = here):
        self.df = pd.read_csv(os.path.join(path, name + ".csv"), sep=",", index=False)

"""
Setting_1 = Settings("Settings", here, None)
Setting_1.Get_setting("Name_1", "Data_1")
Setting_1.Set_setting("Name_1", "Data_2")
Setting_1.Save_to_default_file()
Setting_1.Get_setting("Name_1", "Data_1")
"""
"""
df = pd.read_csv("data.csv", sep=";")
df.to_csv("output.csv", sep=";", index=False)

# 1. Create a DataFrame from a dictionary
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Budapest", "London", "Paris"]
}

df = pd.DataFrame(data)

df.loc[len(df)] = ["David", 28, "Berlin"]

age = df.loc[df["name"] == "Bob", "age"].iloc[0]


self.T_out = self.Frame.Add_Spin(100, float(self.settings.get_setting(self.Name + "_T Count", "1")), 1, 100000, 1)
    def Update_settings(self):
        self.settings.set_setting(self.Name + "_mytext", self.mytext.get("1.0", "end-1c").replace('\n', '\\n'))
        self.settings.set_setting(self.Name + "_delay_between_lines", str(self.delay_between_lines.get()))
        self.settings.set_setting(self.Name + "_Out_check", str(self.Out_check.get()))
        self.settings.set_setting(self.Name + "_IN_check", str(self.In_check.get()))

"""