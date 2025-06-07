import pandas as pd
import pickle
from typing import List
from transform.data_transformer import DataTransformer

class Predictor:
    """
    A class to handle model loading and prediction functionality.
    """
    
    def __init__(self):
        self.data_transformer = DataTransformer()
        self.model = None
    
    def load_model(self, model_path: str):
        """
        Load the trained model from a pickle file.
        
        Args:
            model_path (str): Path to the pickle file containing the model
        """
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    def predict(self, dataset: pd.DataFrame) -> List[int]:
        """
        Make predictions using the loaded model.
        
        Args:
            dataset (pd.DataFrame): Dataset to make predictions on
            
        Returns:
            List[int]: List of predictions
        """
        if not hasattr(self, 'model'):
            raise ValueError("Model not loaded. Please load the model first using load_model()")
        
        transformed_data = self.data_transformer.transform(dataset)
        features = self.data_transformer.get_features_for_prediction(transformed_data)
        return self.model.predict(features) 