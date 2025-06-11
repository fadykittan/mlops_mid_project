from load.db_loader import PostgresLoader
from model.predictor import Predictor
from writer.db_writer import DBWriter
from data_monitor.drift_detector import DriftDetector
import pandas as pd
from utils.logger import setup_logger
import os

# Initialize logger
logger = setup_logger(__name__)

def main():

    # Get database connection parameters from environment variables
    DB_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DB_PORT = '5432'
    DB_NAME = 'mlops_db'
    DB_USER = 'mlops'
    DB_PASS = 'mlops'
    
    print(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
    
    # SQL query to fetch the data
    QUERY = """
select * FROM customer_data
    """

    try:
        logger.info("Starting database prediction process")
        
        # Initialize the database loader
        loader = PostgresLoader(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

        # Load data from database
        print("Loading data from database...")
        logger.info("Loading data from database")
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
        
        logger.info("Data loaded successfully", extra={
            "rows": len(df),
            "columns": len(df.columns)
        })

        # Check for data drift
        print("\nChecking for data drift...")
        logger.info("Checking for data drift")
        drift_detector = DriftDetector()
        drift_report_path = drift_detector.detect_drift(df)
        logger.info(f"Drift report generated at: {drift_report_path}")

        # Initialize the predictor
        predictor = Predictor()

        # Load the model
        model_path = 'model/new_churn_model.pickle'
        print("\nLoading model...")
        logger.info("Loading prediction model")
        predictor.load_model(model_path)

        # Make predictions
        print("\nMaking predictions...")
        logger.info("Making predictions on loaded data")
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
        
        logger.info("Predictions completed", extra={
            "total_customers": total_customers,
            "churn_count": churn_count,
            "churn_rate": f"{churn_rate:.2f}%"
        })

        # Write predictions to database
        write_predictions_to_db(predictions, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
        print("\nPredictions written to database successfully.")
        logger.info("Process completed successfully")

    except Exception as e:
        logger.error("Error in main process", extra={"error": str(e)}, exc_info=True)
        print(f"An error occurred: {str(e)}")

def write_predictions_to_db(predictions: list, DB_HOST: str, DB_PORT: str, DB_NAME: str, DB_USER: str, DB_PASS: str):
    logger.info("Writing predictions to database")
    
    # Initialize the writer
    writer = DBWriter(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

    # Create a DataFrame with predictions
    predictions_df = pd.DataFrame({
        'id': range(len(predictions)),
        'predict_result': predictions
    })

    # Write predictions to database
    writer.write_predictions(predictions_df)
    logger.info("Predictions written to database successfully")

if __name__ == "__main__":
    main() 