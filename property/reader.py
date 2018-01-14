import configparser
from os import walk

from fuzzy.domain.simple_domain import SimpleDomain
from property.mods import ModifierProperty
from property.param import ParameterProperty
from property.read_err import ReaderException
from property.variable import VariableProperty


class PropertiesReader:
    def __init__(self, modifiers_path, params_path):
        modifiers = self.parse_modifiers(modifiers_path)
        self.parameters = self.parse_parameters(modifiers, params_path)

    def parse_modifiers(self, modifiers_path):
        modifiers = {}
        modifiers['None'] = []
        for mod_file in self.get_next_ini_file(modifiers_path):
            with open(modifiers_path + "/" + mod_file) as fp:
                config = configparser.ConfigParser()
                config.read_file(fp)
                mod_values = [ModifierProperty(config['Tx'][key], config['Mx'][key]) for key in config['Tx']]
                modifiers[config['X']['Name']] = mod_values

        return modifiers

    def parse_parameters(self, modifiers, variables_path):
        parameters = {}
        for var_file in self.get_next_ini_file(variables_path):
            with open(variables_path + "/" + var_file) as fp:
                config = configparser.ConfigParser()
                config.read_file(fp)
                try :
                    domain = SimpleDomain(int(config['U']['start']), int(config['U']['end']))
                    variables = [VariableProperty(config['Tx'][key], config['Mx'][key],
                                                  domain) for key in config['Tx']]

                    if config['X']['Size'] == 'SCALAR':
                        p = ParameterProperty(config['X']['Name'], modifiers[config['X']['Modifiers']], config['X']['Type']
                                              , variables, domain)
                        parameters[p.name] = p
                    else:
                        for i in range(int(config['X']['Size'])):
                            p = ParameterProperty(config['X']['Name'] + str(i), modifiers[config['X']['Modifiers']],
                                                  config['X']['Type']
                                                  , variables, domain)
                            parameters[p.name] = p
                except Exception as exc:
                    try:
                        name = config['X']['Name']
                    except KeyError:
                        name = "UNK"
                    raise ReaderException("Error while reading parameter " + name) from exc


        return parameters

    @staticmethod
    def get_next_ini_file(path):
        for (dirpath, dirnames, filenames) in walk(path):
            for f in filenames:
                fsp = f.split(".")
                if fsp[-1] == 'ini':
                    yield f

    def get_parameters(self) -> dict:
        return self.parameters


if __name__ == "__main__":
    pr = PropertiesReader('modifier', 'new_params')
    pass