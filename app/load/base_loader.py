from abc import ABC, abstractmethod
import pandas as pd

class BaseLoader(ABC):
    """
    Abstract base class for data loaders.
    All specific loader implementations should inherit from this class.
    """
    
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """
        Load data from a source and return it as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: The loaded data
        """
        pass 