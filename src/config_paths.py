from dataclasses import dataclass
from pathlib import path
import yaml


class DatasetConfig:

    def __init__(self, root_dir : str, train_subdir : str, test_subdir : str) -> None:
        self.root_dir = root_dir
        self.train_subdir = train_subdir
        self.test_subdir = test_subdir

    

