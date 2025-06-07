import pandas as pd
from typing import List, Optional
from utils.logger import setup_logger

class DataTransformer:
    """
    A class to handle data preprocessing for the churn prediction model.
    This class implements the preprocessing steps from the Data_preparation notebook.
    """
    
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.result_columns = [
            'TotalCharges',
            'Month-to-month',
            'One year',
            'Two year',
            'PhoneService',
            'tenure'
        ]
        self.logger.info("DataTransformer initialized", extra={
            "result_columns": self.result_columns
        })
    
    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input dataset according to the preprocessing steps.
        
        Args:
            dataset (pd.DataFrame): Input dataset to transform
            
        Returns:
            pd.DataFrame: Transformed dataset ready for model prediction
        """
        try:
            self.logger.info("Starting data transformation", extra={
                "input_shape": dataset.shape,
                "input_columns": list(dataset.columns)
            })
            
            # Handle missing values
            self.logger.info("Handling missing values in TotalCharges")
            dataset['TotalCharges'] = dataset['TotalCharges'].fillna(2279)  # 2279 is mean value in data
            dataset['TotalCharges'] = dataset['TotalCharges'].astype(str).str.replace(' ', '2279')
            dataset['TotalCharges'] = dataset['TotalCharges'].astype(float)
            
            # Drop nulls in Contract as it's an important feature
            self.logger.info("Handling Contract column")
            dataset['Contract'] = dataset['Contract'].dropna()
            
            # Fill missing values in PhoneService
            self.logger.info("Handling PhoneService column")
            dataset['PhoneService'] = dataset['PhoneService'].fillna('No')
            
            # Fill missing values in tenure with mean
            self.logger.info("Handling tenure column")
            dataset['tenure'] = dataset['tenure'].fillna(dataset['tenure'].mean())
            
            # Feature handling
            self.logger.info("Converting PhoneService to binary")
            dataset['PhoneService'] = dataset['PhoneService'].map({'Yes': 1, 'No': 0})
            
            # Create dummy variables for Contract
            self.logger.info("Creating dummy variables for Contract")
            contract_dummies = pd.get_dummies(dataset['Contract']).astype(int)
            
            # Ensure all required contract columns exist
            required_contracts = ['Month-to-month', 'One year', 'Two year']
            for contract in required_contracts:
                if contract not in contract_dummies.columns:
                    self.logger.info(f"Adding missing contract column: {contract}")
                    contract_dummies[contract] = 0
            
            # Join with the original dataset
            dataset = dataset.join(contract_dummies)
            
            self.logger.info("Data transformation completed", extra={
                "output_shape": dataset.shape,
                "output_columns": list(dataset.columns)
            })
            
            return dataset
            
        except Exception as e:
            self.logger.error("Error during data transformation", extra={
                "error": str(e),
                "input_shape": dataset.shape
            }, exc_info=True)
            raise
    
    def get_features_for_prediction(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Get the specific features needed for model prediction.
        
        Args:
            dataset (pd.DataFrame): Transformed dataset
            
        Returns:
            pd.DataFrame: Dataset with only the required features for prediction
        """
        try:
            self.logger.info("Selecting features for prediction", extra={
                "input_shape": dataset.shape,
                "required_features": self.result_columns
            })
            
            result = dataset[self.result_columns]
            
            self.logger.info("Features selected successfully", extra={
                "output_shape": result.shape,
                "selected_columns": list(result.columns)
            })
            
            return result
            
        except Exception as e:
            self.logger.error("Error selecting features for prediction", extra={
                "error": str(e),
                "input_shape": dataset.shape,
                "required_features": self.result_columns
            }, exc_info=True)
            raise 