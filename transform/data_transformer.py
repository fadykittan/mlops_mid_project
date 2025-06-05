import pandas as pd
from typing import List, Optional

class DataTransformer:
    """
    A class to handle data preprocessing for the churn prediction model.
    This class implements the preprocessing steps from the Data_preparation notebook.
    """
    
    def __init__(self):
        self.result_columns = [
            'TotalCharges',
            'Month-to-month',
            'One year',
            'Two year',
            'PhoneService',
            'tenure'
        ]
    
    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input dataset according to the preprocessing steps.
        
        Args:
            dataset (pd.DataFrame): Input dataset to transform
            
        Returns:
            pd.DataFrame: Transformed dataset ready for model prediction
        """
        # Handle missing values
        dataset['TotalCharges'] = dataset['TotalCharges'].fillna(2279)  # 2279 is mean value in data
        dataset['TotalCharges'] = dataset['TotalCharges'].astype(str).str.replace(' ', '2279')
        dataset['TotalCharges'] = dataset['TotalCharges'].astype(float)
        
        # Drop nulls in Contract as it's an important feature
        dataset['Contract'] = dataset['Contract'].dropna()
        
        # Fill missing values in PhoneService
        dataset['PhoneService'] = dataset['PhoneService'].fillna('No')
        
        # Fill missing values in tenure with mean
        dataset['tenure'] = dataset['tenure'].fillna(dataset['tenure'].mean())
        
        # Feature handling
        dataset['PhoneService'] = dataset['PhoneService'].map({'Yes': 1, 'No': 0})
        
        # Create dummy variables for Contract
        contract_dummies = pd.get_dummies(dataset['Contract']).astype(int)
        dataset = dataset.join(contract_dummies)
        
        return dataset
    
    def get_features_for_prediction(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Get the specific features needed for model prediction.
        
        Args:
            dataset (pd.DataFrame): Transformed dataset
            
        Returns:
            pd.DataFrame: Dataset with only the required features for prediction
        """
        return dataset[self.result_columns] 