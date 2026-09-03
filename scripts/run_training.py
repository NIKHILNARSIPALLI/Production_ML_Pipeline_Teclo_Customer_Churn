"""
let's run the training script
"""

from src.data import process_data
from src.features import prepare_features
from src.train import train_model

from src.logger import set_logger
logger = set_logger(__name__)


logger.info("Initializing training process")


# Let's get the dataframe from the dataset
try:
    df = process_data()
    logger.info("read and processed data csv file")
except Exception as e:
    logger.critical(f"Data processing has failed with exception: \n{e}")
    raise


# Let's preprocess the data and split into train and test sets
try:
    X_train, X_test, y_train, y_test, preprocessor = prepare_features(df)
    logger.info("completed train test split and preprocessor")
except Exception as e:
    logger.critical(f"Train.py has failed with exception: \n {e}")
    raise

# Let's complete model training and obtained the trained model
try:
    model = train_model(X_train, y_train)
    logger.info("Completed model training")

except Exception as e:
    logger.critical(f"Model.py has failed with exception: \n {e}")
    raise









