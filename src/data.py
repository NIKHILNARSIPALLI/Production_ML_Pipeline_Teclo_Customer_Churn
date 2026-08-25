import pandas as pd
import yaml


def import_data():
    with open("config/paths.yaml", "r") as file:
        file_paths = yaml.safe_load(file)




if __name__ == '__main__':
    None