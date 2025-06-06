from flask import Flask, request, jsonify
import pandas as pd
from model.predictor import Predictor
from transform.data_transformer import DataTransformer
from api.models import CustomerData

app = Flask(__name__)

# Initialize the predictor and transformer
predictor = Predictor()
model_path = 'model/new_churn_model.pickle'
predictor.load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Create CustomerData instance
        customer = CustomerData(
            TotalCharges=float(data.get('TotalCharges', 0)),
            Contract=data.get('Contract', ''),
            PhoneService=data.get('PhoneService', ''),
            tenure=float(data.get('tenure', 0))
        )
        
        # Validate data
        is_valid, error_message = customer.validate()
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'TotalCharges': customer.TotalCharges,
            'Contract': customer.Contract,
            'PhoneService': customer.PhoneService,
            'tenure': customer.tenure
        }])
        
        # Make prediction using the predictor (which uses DataTransformer internally)
        prediction = predictor.predict(df)
        
        # Return result
        return jsonify({
            'prediction': int(prediction[0]),
            'churn_status': 'Churn' if prediction[0] == 1 else 'No Churn'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 
