from property.reader import PropertiesReader


def load_properties(file):
    pr = PropertiesReader(file + '/modifier', file + '/params')
    return pr.get_parameters()


def load_properties_two_files(modifiers_file, params_file):
    pr = PropertiesReader(modifiers_file, params_file)
    return pr.get_parameters()
