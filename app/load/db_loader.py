import pandas as pd
from sqlalchemy import create_engine
from .base_loader import BaseLoader
from utils.logger import setup_logger

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
        self.logger = setup_logger(__name__)
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection_string)
        self.logger.info("PostgreSQL loader initialized", extra={
            "host": host,
            "port": port,
            "database": database,
            "user": user
        })
        
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
            self.logger.info("Executing database query", extra={"query": query})
            df = pd.read_sql(query, self.engine)
            self.logger.info("Data loaded successfully", extra={
                "rows": len(df),
                "columns": list(df.columns)
            })
            return df
        except Exception as e:
            self.logger.error("Error loading data from PostgreSQL", extra={
                "error": str(e),
                "query": query
            }, exc_info=True)
            raise Exception(f"Error loading data from PostgreSQL: {str(e)}") 