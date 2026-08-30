#let's setup the config class for the project
from src.config import load_config
config = load_config()

#Let's import the logger function
from src.logger import set_logger
logger = set_logger(__name__)

#Now, let's import the required libraries
import pandas as pd
from pathlib import Path



EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]





def load_data() -> pd.DataFrame:
    """
    This function loads the data from the raw data path and returns a pandas dataframe
    """

    #Raw data path
    path = Path(__file__).resolve().parent.parent
    path = path.joinpath(config.dataPath.root_dir, config.dataPath.raw_data_dir, config.dataPath.datasetName)

    if not path.exists():
        logger.critical(f"DataSet File not found {path}")
        raise FileNotFoundError(f"Could not locate Dataset {path}")

    
    logger.info(f"Loading the data from {path}")
    try:
        df = pd.read_csv(path, encoding='latin-1')

    except Exception as e:
        logger.critical(f"Error occurred while loading data from {path}: {e}")
        raise

    logger.info(f"Data loaded successfully from {path}")
    logger.info(f"Data shape: {df.shape[0]}Rows, {df.shape[1]} Columns")

    return df




def validate_columns(df: pd.DataFrame) -> None:
    """
    This function validates the columns of the dataframe against the expected columns
    """

    logger.info(f"Validating the columns of the dataset")
    actual_columns = set(df.columns)
    expected_columns = set(EXPECTED_COLUMNS)

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    if missing_columns:
        logger.critical(f"Missing required columns in the dataset: {sorted(missing_columns)}")
        raise ValueError(f"Missing required columns in the dataset: {sorted(missing_columns)}")

    if unexpected_columns:
        logger.critical(f"Unexpected columns found in the dataset: {sorted(unexpected_columns)}")
        raise ValueError(f"Unexpected columns found in the dataset: {sorted(unexpected_columns)}")

    
    logger.info(f"Validation Complete - Columns in the dataset are as expected")

    return None


def handle_missing_values(df: pd.DataFrame, missing_columns: pd.Series, missing_values: pd.Series) -> pd.DataFrame:
    """
    This function handles missing values in the dataframe by filling or dropping them as appropriate
    """

    logger.info(f"Handling missing values in the dataset")

    #This handles TotalCharges column
    if "TotalCharges" in missing_columns:
        # Fill missing TotalCharges for new customers with tenure 0
        df.loc[df["tenure"] == 0, "TotalCharges"] = 0
        logger.info(
            "Filled missing TotalCharges for new customers with tenure 0. Remaining missing values: %d",
            df["TotalCharges"].isna().sum()
        )

        # Drop any remaining rows with missing TotalCharges
        df = df.dropna(subset=["TotalCharges"])
        logger.info(
            "Dropped remaining rows with missing TotalCharges. Remaining missing values: %d",
            df["TotalCharges"].isna().sum()
        )

    # Add more statements as you go to handle the missing values

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans the data by removing any leading or trailing spaces from the column names
    and returns a cleaned dataframe
    """

    logger.info(f"Cleaning the data by removing leading and trailing spaces from column names")
    df.columns = df.columns.str.strip()

    # Remove leading/trailing whitespace from string columns
    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].str.strip()    

    # Convert TotalCharges to numeric.
    # Invalid/blank values become NaN.
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # Convert tenure explicitly to numeric
    df["tenure"] = pd.to_numeric(
        df["tenure"],
        errors="coerce"
    )

    # Convert MonthlyCharges explicitly to numeric
    df["MonthlyCharges"] = pd.to_numeric(
        df["MonthlyCharges"],
        errors="coerce"
    )

    # Check duplicates
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        logger.warning(
            "Found %d duplicate rows. Removing them.",
            duplicate_count
        )
        df = df.drop_duplicates()

    # Check missing values
    missing_values = df.isna().sum()
    missing_columns = missing_values[missing_values > 0]

    if not missing_columns.empty:
        logger.warning(
            "Missing values detected: %s",
            missing_columns.to_dict()
        )

        #Let's handle the missing values in the dataset
        df = handle_missing_values(df,missing_columns,missing_values)


    logger.info(
        "Data cleaning completed. Final shape: %s",
        df.shape
    )

    return df


def save_data(
    df: pd.DataFrame,
    output_path: str | Path
) -> None:
    """
    Save cleaned data to the specified path.
    """

    output_path = Path(output_path)

    logger.info("Saving cleaned dataset to: %s", output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(output_path, index=False)

    logger.info(
        "Cleaned dataset saved successfully. Shape: %s",
        df.shape
    )

    return None

def process_data() -> pd.DataFrame:
    """
    Complete data ingestion and cleaning pipeline.
    """
    #let's define output data path
    output_path = Path(__file__).resolve().parent.parent
    output_path = output_path.joinpath(config.dataPath.root_dir, config.dataPath.processed_data_dir, config.dataPath.cleaened_datasetName)
    logger.info("Starting data processing pipeline")

    df = load_data() # type: ignore

    validate_columns(df)

    df = clean_data(df)

    save_data(df, output_path)

    logger.info("Data processing pipeline completed successfully")

    return df


if __name__ == '__main__':

    logger.info("Starting data processing script")
    try:
        process_data()
    except Exception as e:
        logger.critical(f"Data processing failed: {e}")
        raise
    logger.info("Data processing script completed successfully")