"""
This consists of feature engineering and preprocessing

This would handle the following:
    - Separate X and y
    - Remove identifiers such as customerID
    - Convert target Churn → 0/1
    - Identify numerical/categorical columns
    - Build ColumnTransformer
    - Numerical imputation/scaling
    - Categorical encoding 
    - Feature engineering if you decide to add any
    - Save/load the fitted preprocessing pipeline

    
Conceptually:

            Clean DataFrame
                ↓
            features.py
                ↓
            X, y
                ↓
            Train/Test Split
                ↓
            Preprocessing Pipeline
                ↓
            Processed X_train / X_test

Important: the preprocessing transformer should be fit only on training data.


features.py
│
├── 1. Receive cleaned DataFrame
│
├── 2. Separate target (`Churn`)
│
├── 3. Remove `customerID`
│
├── 4. Convert target Yes/No → 1/0
│
├── 5. Train/test split
│
├── 6. Identify numerical columns
│
├── 7. Identify categorical columns
│
├── 8. Build ColumnTransformer
│
├── 9. Fit transformer ONLY on X_train
│
├── 10. Transform X_train and X_test
│
└── 11. Return/save the results

"""

from src.logger import set_logger
from src.config import load_config

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder  



config = load_config()
logger = set_logger(__name__)


# Let's prepare the features
def prepare_features(df : pd.DataFrame):
    logger.info("Preparing features for modeling")


    # Let's separate the target and features
    X = df.drop(columns = ["Churn", "customerID"])
    y = df["Churn"].map({"Yes": 1, "No": 0}) # This is basically one-hot encoding i.e., converting the variable to 0/1 for modeling

    #Let's identify the numerical and categorical columns
    # These help in building the ColumnTransformer for preprocessing
    numerical_cols = X.select_dtypes(include=np.number).columns.tolist()   # type: ignore
    categorical_cols = X.select_dtypes(exclude=np.number).columns.tolist() # type:ignore

    # Let's log the results
    logger.info(f"Numerical columns: {numerical_cols}")
    logger.info(f"Categorical columns: {categorical_cols}")



    #Let's do test/train split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= config.features.train_test_split_test_size, # That is 0.2
        random_state= config.features.train_test_split_random_state, # That is 42
        stratify=y # Stratified sampling to ensure the same proportion of classes in train and test sets
    )
    logger.info(f"Train/Test split done with test size {config.features.train_test_split_test_size} and random state {config.features.train_test_split_random_state}")
    logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")


    # Now let's do the preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", StandardScaler(), numerical_cols),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )


    # Fit the preprocessor on the training data
    # This is essestially telling the preprocessor to learn the parameters from the training data
    # This basically is letting is learn the numerical and categorical columns and their respective transformations
    preprocessor.fit(X_train)
    logger.info("Preprocessor fitted on training data")

    # Let's transform the training and test data
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    logger.info("Training and test data transformed using the fitted preprocessor")

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor



if __name__ == "__main__":

    print("This is a module for feature engineering and preprocessing. It is not meant to be run directly.")
    logger.warning("This is a module for feature engineering and preprocessing. It is not meant to be run directly.")

"""
from src.data import load_data
from src.features import prepare_features
from src.train import train_model


df = load_data()

X_train, X_test, y_train, y_test, preprocessor = prepare_features(df)

model = train_model(
    X_train,
    y_train
)"""

       

