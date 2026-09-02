1. Validate the cleaned dataset

Before transforming anything, verify things such as:
Required columns exist
Expected data types
Target column exists (Churn)
No unexpected nulls
No duplicate customer IDs
Valid ranges for numerical columns
Expected categories for categorical columns
Target contains both classes
For example:
customerID     → unique
SeniorCitizen  → 0/1
tenure         → >= 0
MonthlyCharges → >= 0
TotalCharges   → >= 0
Churn          → Yes/No
This is data validation, not preprocessing.