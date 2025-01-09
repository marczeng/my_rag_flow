import configparser

def read_ini(file):
    config = configparser.ConfigParser()
    config.read(file, encoding="utf-8")
    return config

