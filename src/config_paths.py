from dataclasses import dataclass
from dataclasses import fields
from pathlib import path
import yaml


#Let's create a function that filters the required fields from the Yaml file
# such that when using across multiple yaml fields and yaml files that contains
# more than required parameteres then this filtered values will help not raise error of more/less paramteres
def create_config(config_class, raw: dict):

    valid_fields = (fields.name for field in fields(config_class))
    filtered = {
        key: value for
        key, value in raw.items()
        if key in valid_fields
    }
    return config_class(**filtered)



class DatasetConfig:

    def __init__(self, root_dir : str, train_subdir : str, test_subdir : str) -> None:
        self.root_dir = root_dir
        self.train_subdir = train_subdir
        self.test_subdir = test_subdir

class LoadData:
    ...

    

