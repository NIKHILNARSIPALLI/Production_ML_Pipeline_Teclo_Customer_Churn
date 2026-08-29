import logging
from datetime import datetime
from pathlib import Path


#Let's create a log folder
log_dir = Path()
log_dir.mkdir(exist_ok=True)

#Let's name the log file for this run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = log_dir.joinpath(f"run_{timestamp}.log")

#Let's configuring logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)


#Let's create a callable function from other python codes
def set_logger(name):
    return logging.getLogger(name)