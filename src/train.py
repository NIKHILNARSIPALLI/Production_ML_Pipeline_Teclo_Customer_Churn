"""
This script is used to train the model using the training data and save the trained model to a file.
The script performs the following steps:
1. Load the configuration from the config.yaml file.
2. Load the training data from the specified path.
3. Preprocess the training data using the preprocessing pipeline.  
 Also does MLFlow logging of the training process.
4. Train the model using the preprocessed training data.
5. Save the trained model to a file."""


from src.config import load_config
from src.logger import set_logger
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path
from datetime import datetime


config = load_config()
logger = set_logger(__name__)



def train_model( X_train, y_train):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_name = "LogisticRegression"

    model_path = Path(__file__).resolve().parent.parent
    model_path = model_path.joinpath(config.model.model_path_parent, config.model.model_path_main, f"{model_name}_{timestamp}.joblib")

    logger.info("started model training process")


    # Let's create a model
    model = LogisticRegression(
        max_iter = 1000,
        random_state= 42
    )

    # Train the model
    model.fit(X = X_train, y = y_train)

    logger.info("Model training completed")


    # Let's create the parent directory if not existing
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Let's save the model
    joblib.dump(model, model_path)

    logger.info(f"Model {model_name}, saved to {model_path}")

    return model




if __name__ == "__main__":

    print("This is a module for feature engineering and preprocessing. It is not meant to be run directly.")
    logger.warning("This is a module for feature engineering and preprocessing. It is not meant to be run directly.")
