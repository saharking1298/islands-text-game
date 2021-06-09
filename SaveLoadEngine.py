# For licencing, check LICENCE file.
import os.path
import ast


class SaveLoadEngine:
    def __init__(self, general_directory, filename):
        self.directory = general_directory
        self.save_location = general_directory + "\\" + filename + ".txt"
        if not os.path.exists(general_directory):
            os.makedirs(general_directory)
        if not os.path.isfile(self.save_location):
            open(self.save_location, "x")

    def clear_save(self):
        w = open(self.save_location, "w")
        w.write("")
        w.close()

    def get_serial_names(self):
        file = open(self.save_location, 'r')
        content = file.read()
        file.close()
        lines = content.split("#Serial Name#:")
        del lines[0]
        serial_names = []
        for variable in lines:
            x = variable.split("#Type#:")
            serial_names.append(x[0].strip())
        return serial_names

    def get_types(self):
        file = open(self.save_location, 'r')
        content = file.read()
        file.close()
        lines = content.split("#Serial Name#:")
        del lines[0]
        types = []
        for variable in lines:
            x = variable.split("#Type#:")
            y = x[1].split("#End#")
            types.append(y[0].strip())
        return types

    def get_vars(self):
        file = open(self.save_location, 'r')
        content = file.read()
        file.close()
        lines = content.split("#Serial Name#:")
        del lines[0]
        variables = []
        for variable in lines:
            x = variable.split("#Type#:")
            y = x[1].split("#End#")
            variables.append(y[1].replace("\n", ""))
        return variables

    def get_type(self, variable):
        vtype = ""
        if type(variable) == str:
            vtype = "str"
        elif type(variable) == int:
            vtype = "int"
        elif type(variable) == dict:
            vtype = "dict"
        elif type(variable) == set:
            vtype = "set"
        elif type(variable) == list:
            vtype = "list"
        elif type(variable) == float:
            vtype = "float"
        elif type(variable) == tuple:
            vtype = "tuple"
        return vtype

    def update_save(self, serial_names, variables, types):
        file = open(self.save_location, 'w')
        for i in range(len(serial_names)):
            file.write("#Serial Name#: " + serial_names[i] + " #Type#: " + types[i] + "#End#")
            file.write("\n" + str(variables[i]) + "\n")
        file.close()

    def delete_var(self, serial_name):
        serial_names = self.get_serial_names()
        types = self.get_types()
        variables = self.get_vars()
        for i in range(len(serial_names)):
            if serial_name == serial_names[i]:
                del serial_names[i]
                del types[i]
                del variables[i]
                self.update_save(serial_names, variables, types)
                break

    def save(self, variable, serial_name):
        vtype = self.get_type(variable)
        serial_names = self.get_serial_names()
        if serial_name not in serial_names:
            file = open(self.save_location, 'a+')
            file.write("#Serial Name#: " + serial_name + " #Type#: " + vtype + "#End#")
            file.write("\n" + str(variable) + "\n")
            file.close()
        else:
            types = self.get_types()
            variables = self.get_vars()
            for i in range(len(serial_names)):
                if serial_name == serial_names[i]:
                    types[i] = vtype
                    variables[i] = variable
                    self.update_save(serial_names,variables, types)
                    break





    def load(self, serial_name):
        try:
            result = None
            serial_names = self.get_serial_names()
            variables = self.get_vars()
            types = self.get_types()
            if serial_name in serial_names:
                for i in range(len(serial_names)):
                    if serial_name == serial_names[i]:
                        if types[i] == "str":
                            result = str(variables[i].strip())
                        elif types[i] == "int":
                            result = int(variables[i].strip())
                        elif types[i] == "dict":
                            result = ast.literal_eval(variables[i].strip())
                        elif types[i] == "set":
                            result = ast.literal_eval(variables[i].strip())
                        elif types[i] == "list":
                            result = ast.literal_eval(variables[i].strip())
                        elif types[i] == "float":
                            result = float(variables[i].strip())
                        elif types[i] == "tuple":
                            result = ast.literal_eval(variables[i].strip())
                        break
            return result
        except:
            self.clear_save()

    def safe_load(self, serial_name, default_var):
        x = self.load(serial_name)
        if x != None:
            return x
        else:
            self.save(default_var, serial_name)
            return default_var

    def get_all(self):
        serial_names = self.get_serial_names()
        x = {}
        for name in serial_names:
            x[name] = self.load(name)
        return x
