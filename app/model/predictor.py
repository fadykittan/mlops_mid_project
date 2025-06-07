import pandas as pd
import pickle
from typing import List
from transform.data_transformer import DataTransformer
from utils.logger import setup_logger

class Predictor:
    """
    A class to handle model loading and prediction functionality.
    """
    
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.data_transformer = DataTransformer()
        self.model = None
        self.logger.info("Predictor initialized")
    
    def load_model(self, model_path: str):
        """
        Load the trained model from a pickle file.
        
        Args:
            model_path (str): Path to the pickle file containing the model
        """
        try:
            self.logger.info("Loading model from file", extra={"model_path": model_path})
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.logger.info("Model loaded successfully", extra={
                "model_type": type(self.model).__name__,
                "model_path": model_path
            })
        except Exception as e:
            self.logger.error("Error loading model", extra={
                "error": str(e),
                "model_path": model_path
            }, exc_info=True)
            raise
    
    def predict(self, dataset: pd.DataFrame) -> List[int]:
        """
        Make predictions using the loaded model.
        
        Args:
            dataset (pd.DataFrame): Dataset to make predictions on
            
        Returns:
            List[int]: List of predictions
        """
        try:
            if not hasattr(self, 'model'):
                self.logger.error("Model not loaded")
                raise ValueError("Model not loaded. Please load the model first using load_model()")
            
            self.logger.info("Starting prediction process", extra={
                "input_rows": len(dataset),
                "input_columns": list(dataset.columns)
            })
            
            transformed_data = self.data_transformer.transform(dataset)
            features = self.data_transformer.get_features_for_prediction(transformed_data)
            
            predictions = self.model.predict(features)
            
            # Log prediction statistics
            prediction_counts = pd.Series(predictions).value_counts().to_dict()
            self.logger.info("Predictions completed", extra={
                "total_predictions": len(predictions),
                "prediction_distribution": prediction_counts
            })
            
            return predictions
            
        except Exception as e:
            self.logger.error("Error during prediction", extra={
                "error": str(e),
                "input_shape": dataset.shape
            }, exc_info=True)
            raise 