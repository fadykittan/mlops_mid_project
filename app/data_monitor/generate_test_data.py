import pandas as pd
import numpy as np
from datetime import datetime

def generate_test_data(n_samples=1000, drift_factor=0.5):
    """
    Generate test data with intentional drift in some features.
    
    Args:
        n_samples (int): Number of samples to generate
        drift_factor (float): Factor to control the amount of drift (0-1)
    
    Returns:
        pd.DataFrame: Generated test data
    """
    np.random.seed(42)
    
    # Generate base data
    data = {
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice(['0', '1'], n_samples),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'tenure': np.random.normal(32, 24, n_samples).clip(0, 72),  # Months
        'MonthlyCharges': np.random.normal(65, 30, n_samples).clip(20, 120),
        'TotalCharges': np.random.normal(2280, 2266, n_samples).clip(0, 8684),
        'PhoneService': np.random.choice(['Yes', 'No'], n_samples),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples)
    }
    
    # Create drift in some features
    drift_mask = np.random.random(n_samples) < drift_factor
    
    # Drift in Contract (more long-term contracts)
    data['Contract'] = np.where(drift_mask, 
                               np.random.choice(['One year', 'Two year'], n_samples),
                               data['Contract'])
    
    # Drift in MonthlyCharges (higher charges)
    data['MonthlyCharges'] = np.where(drift_mask,
                                     np.random.normal(85, 30, n_samples).clip(20, 120),
                                     data['MonthlyCharges'])
    
    # Drift in tenure (longer tenure)
    data['tenure'] = np.where(drift_mask,
                             np.random.normal(45, 20, n_samples).clip(0, 72),
                             data['tenure'])
    
    # Drift in StreamingTV (more streaming)
    data['StreamingTV'] = np.where(drift_mask,
                                  np.random.choice(['Yes', 'Yes', 'No'], n_samples),
                                  data['StreamingTV'])
    
    # Drift in PhoneService (more phone service)
    data['PhoneService'] = np.where(drift_mask,
                                   np.random.choice(['Yes', 'Yes', 'Yes', 'No'], n_samples),
                                   data['PhoneService'])
    
    # Drift in gender (more female customers)
    data['gender'] = np.where(drift_mask,
                             np.random.choice(['Female', 'Female', 'Male'], n_samples),
                             data['gender'])
    
    # Drift in PaperlessBilling (more paperless)
    data['PaperlessBilling'] = np.where(drift_mask,
                                       np.random.choice(['Yes', 'Yes', 'No'], n_samples),
                                       data['PaperlessBilling'])
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data_monitor/data/test_data_{timestamp}.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Generated test data with drift saved to: {output_path}")
    print("\nSample of generated data:")
    print(df.head())
    print("\nData distribution summary:")
    print(df.describe())
    
    return df

if __name__ == "__main__":
    generate_test_data() 