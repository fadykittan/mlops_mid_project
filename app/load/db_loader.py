import pandas as pd
from sqlalchemy import create_engine
from .base_loader import BaseLoader

class PostgresLoader(BaseLoader):
    """
    Loader class for reading data from PostgreSQL database.
    """
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        """
        Initialize the PostgreSQL loader with database connection parameters.
        
        Args:
            host (str): Database host
            port (int): Database port
            database (str): Database name
            user (str): Database user
            password (str): Database password
        """
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection_string)
        
    def load_data(self, query: str) -> pd.DataFrame:
        """
        Load data from PostgreSQL database using the provided query.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: The loaded data from the database
            
        Raises:
            Exception: If there's an error connecting to the database or executing the query
        """
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            raise Exception(f"Error loading data from PostgreSQL: {str(e)}") 