import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional
from datetime import datetime

class DBWriter:
    """
    Writer class for writing prediction results to PostgreSQL database.
    """
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        """
        Initialize the PostgreSQL writer with database connection parameters.
        
        Args:
            host (str): Database host
            port (int): Database port
            database (str): Database name
            user (str): Database user
            password (str): Database password
        """
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection_string)
        
    def write_predictions(self, df: pd.DataFrame, table_name: str = 'prediction_results') -> None:
        """
        Write prediction results to the database.
        
        Args:
            df (pd.DataFrame): DataFrame containing prediction results with columns ['id', 'predict_result']
            table_name (str): Name of the table to write to (default: 'prediction_results')
            
        Raises:
            Exception: If there's an error connecting to the database or writing the data
        """
        try:
            # Ensure the DataFrame has the required columns
            required_columns = ['id', 'predict_result']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"DataFrame must contain columns: {required_columns}")
            
            # Create table if it doesn't exist
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                predict_result INTEGER,
                prediction_date DATE
            )
            """
            
            with self.engine.connect() as connection:
                connection.execute(text(create_table_query))
                connection.commit()
            
            # Add today's date to the DataFrame
            df['prediction_date'] = datetime.now().date()
            
            # Write the DataFrame to the database
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists='append',
                index=False
            )
            
        except Exception as e:
            raise Exception(f"Error writing predictions to PostgreSQL: {str(e)}") 