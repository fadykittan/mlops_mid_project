import pandas as pd
from model.predictor import Predictor

def main():
    # Create sample data that matches the expected format
    sample_data = pd.DataFrame({
        'TotalCharges': [2000, 3000, 1500],
        'Contract': ['Month-to-month', 'One year', 'Two year'],
        'PhoneService': ['Yes', 'No', 'Yes'],
        'tenure': [12, 24, 6]
    })

    # Initialize the predictor
    predictor = Predictor()

    try:
        # Load the model (replace with your actual model path)
        model_path = 'model/new_churn_model.pickle'
        predictor.load_model(model_path)

        # Make predictions
        predictions = predictor.predict(sample_data)

        # Print results
        print("\nSample Data:")
        print(sample_data)
        print("\nPredictions:")
        for i, pred in enumerate(predictions):
            print(f"Customer {i+1}: {'Churn' if pred == 1 else 'No Churn'}")

    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        print("Please ensure the model file exists at the specified path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 