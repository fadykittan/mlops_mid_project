import pandas as pd
from pathlib import Path
from .base_loader import BaseLoader

class CSVLoader(BaseLoader):
    """
    Loader class for reading data from CSV files.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the CSV loader with the path to the CSV file.
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = Path(file_path)
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the CSV file.
        
        Returns:
            pd.DataFrame: The loaded data from the CSV file
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            pd.errors.EmptyDataError: If the CSV file is empty
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found at {self.file_path}")
            
        return pd.read_csv(self.file_path) 