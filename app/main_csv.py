from load import CSVLoader
import pandas as pd
from model.predictor import Predictor

def main():
    # Initialize the CSV loader with the path to the CSV file
    loader = CSVLoader("data_base/database_input.csv")
    
    try:
        # Load the data
        df = loader.load_data()
        
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
        
        print("\nData types:")
        print("-" * 50)
        print(df.dtypes)

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    # Print a separator
    print("\n")
    print("=" * 50)
    print("=" * 50)

    # Initialize the predictor
    predictor = Predictor()

    try:
        # Load the model (replace with your actual model path)
        model_path = 'app/model/new_churn_model.pickle'
        predictor.load_model(model_path)

        # Make predictions
        predictions = predictor.predict(df)

        # Print results
        print("\nPredictions:")
        for i, pred in enumerate(predictions):
            print(f"Customer {i+1}: {'Churn' if pred == 1 else 'No Churn'}")

        print("\nRun on CSV file finished successfully!!!")

    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        print("Please ensure the model file exists at the specified path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 