from dataclasses import dataclass
from dataclasses import fields, is_dataclass
from pathlib import Path
import yaml


#Let's set up the logger
import data
from src.logger import set_logger

logger = set_logger(__name__)




"""
Let's create a function that filters the required fields from one of the Yaml file key:values pair
such that when using across multiple yaml fields and yaml files that contains
more than required parameteres then this filtered values will help not raise error of more/less paramteres
So, ideally input would be a yaml_file["Key"], and output would be the value pairs inside the key sent to the specfici object
"""
def create_config(config_class: type, raw: dict, strict=True):

     # We want to make sure the config_class is an actual data class before moving further
     if not is_dataclass(config_class):
          logger.critical(f"Provided config_class must be a dataclass {config_class.__name__}")
          raise TypeError(f"{config_class.__name__} must be a dataclass")


     # Let's get all fields from the dataclass and filter the fields that we need to pass to the config_class
     valid_fields = {field.name for field in fields(config_class)}

     #Before moving futher let's make sure all the value's mentioned in the yaml file
     # for that specific field have been used up or if we are missing any key parameters
     unknown = set(raw) - valid_fields
     if strict and unknown:
         logger.critical(f"Unkown parameters found in {config_class.__name__} class: {unknown}")
         raise ValueError(
              f"Unknown paramters for "
              f"{config_class.__name__} : {unknown}"
         )


     filtered = {
        key: value for
        key, value in raw.items()
        if key in valid_fields
    }

     if not filtered:
         logger.warning(f"Filtered configs for {config_class.__name__} class is empty")

     logger.info(f"Created config class for {config_class.__name__}")

     return config_class(**filtered)






# This class is created to make objects for each of the config parameters
@dataclass
class DatasetConfig:
        root_dir : str
        train_subdir : str
        test_subdir :str

@dataclass
class ModelConfig:
     model_name :str # type: ignore
     model_type :str # type: ignore


@dataclass
class TrainingConfig:
     batch_size : int # type: ignore



@dataclass
class UnitTest:
     parameter1 : str
     parameter2 : str
     parameter3 : str


@dataclass
class DataPath:
     root_dir: str
     raw_data_dir: str
     datasetName : str
     processed_data_dir: str
     cleaened_datasetName : str


# This contains the configs of all the dataclasses and defines which class object each name contains
@dataclass
class Configs:
     dataset : DatasetConfig # type: ignore
     model : ModelConfig # type: ignore
     training: TrainingConfig # type: ignore
     unitTest : UnitTest # type: ignore
     dataPath : DataPath





#This function defines the object
def load_config() -> Configs:

    #Main project file oath and relative yaml file path
     main_dir = Path(__file__).resolve().parent.parent
     yaml_path = main_dir.joinpath("configs","config.yaml")

     try:
          raw = yaml.safe_load(open(yaml_path))
          logger.info(f"Loaded the yaml file from {yaml_path}")
     except:
          logger.critical(f"File not found {yaml_path}")
          raise FileNotFoundError(f"Could not locate {yaml_path}")
          

     return Configs(
          dataset = create_config(
               DatasetConfig, raw["dataset"]
          ),# type: ignore

          model = create_config(
               ModelConfig, raw["model"]
          ),# type: ignore

          training = create_config(
               TrainingConfig, raw["train"]
          ),# type: ignore

          unitTest = create_config(
               UnitTest, raw["UnitTest"]
          ),# type: ignore

          dataPath= create_config(
               DataPath, raw["DataPath"]
          )# type: ignore


     )

"""
So, now in other python files we can simply call the function load_congig
and then get its parameters ex: 
from src.config import load_config

config = load_config()

print(config.dataset.root_dir)

"""

    

