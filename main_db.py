from load.db_loader import PostgresLoader
from model.predictor import Predictor
import pandas as pd

def main():
    # Database connection parameters
    DB_HOST = "localhost"  # Replace with your database host
    DB_PORT = 5432        # Replace with your database port
    DB_NAME = "your_db"   # Replace with your database name
    DB_USER = "your_user" # Replace with your database user
    DB_PASS = "your_pass" # Replace with your database password

    # SQL query to fetch the data
    QUERY = """
select * FROM customer_data
    """

    try:
        # Initialize the database loader
        loader = PostgresLoader(
            host='localhost',
            port='5432',
            database='mlops_db',
            user='mlops',
            password='mlops'
        )

        # Load data from database
        print("Loading data from database...")
        df = loader.load_data(QUERY)
        
        # Display basic information about the loaded data
        print("\nDataset Information:")
        print("-" * 50)
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print("\nColumn names:")
        for col in df.columns:
            print(f"- {col}")
            
        print("\nFirst 5 rows of the data:")
        print("-" * 50)
        print(df.head())

        # Initialize the predictor
        predictor = Predictor()

        # Load the model
        model_path = 'model/new_churn_model.pickle'
        print("\nLoading model...")
        predictor.load_model(model_path)

        # Make predictions
        print("\nMaking predictions...")
        predictions = predictor.predict(df)

        # Print results
        print("\nPredictions:")
        print("-" * 50)
        for i, pred in enumerate(predictions):
            print(f"Customer {i+1}: {'Churn' if pred == 1 else 'No Churn'}")

        # Print summary statistics
        churn_count = sum(predictions)
        total_customers = len(predictions)
        churn_rate = (churn_count / total_customers) * 100
        
        print("\nSummary Statistics:")
        print("-" * 50)
        print(f"Total Customers: {total_customers}")
        print(f"Predicted Churns: {churn_count}")
        print(f"Churn Rate: {churn_rate:.2f}%")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 