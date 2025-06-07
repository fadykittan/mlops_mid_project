import pandas as pd
from sqlalchemy import create_engine
import os

def load_data_to_db():
    # Load environment variables
    # load_dotenv()
    
    # Database connection parameters
    DB_USER = 'mlops'
    DB_PASSWORD = 'mlops'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'mlops_db'
    
    # Create database connection URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        # Read the CSV file
        csv_path = os.path.join('data', 'database_input.csv')
        df = pd.read_csv(csv_path)
        
        # Insert data into the database
        # Replace 'your_table_name' with the actual table name
        df.to_sql('customer_data', engine, if_exists='append', index=False)
        
        print("Data successfully loaded into the database!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    load_data_to_db() 