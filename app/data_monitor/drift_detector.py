import pandas as pd
import whylogs as why
from whylogs.core import DatasetProfile
from whylogs.core.metrics import DistributionMetric
from typing import Optional, Union
import logging
import os
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriftDetector:
    """
    A class to detect data drift using WhyLogs.
    This class compares new data against reference data loaded from a CSV file.
    """
    
    def __init__(self, reference_data_path: str = "data_monitor/data/database_input2.csv"):
        """
        Initialize the DriftDetector with reference data from a CSV file.
        
        Args:
            reference_data_path (str): Path to the CSV file containing reference data
        """
        try:
            self.reference_data = pd.read_csv(reference_data_path)
            # Create reference profile
            self.reference_profile = why.log(self.reference_data).profile()
            logger.info(f"Successfully loaded reference data from {reference_data_path}")
        except Exception as e:
            logger.error(f"Error loading reference data: {str(e)}")
            raise
            
    def detect_drift(self, 
                    current_data: Union[pd.DataFrame, str],
                    drift_threshold: float = 0.05,
                    output_dir: str = "data_monitor/drift_reports") -> str:
        """
        Detect data drift between reference data and current data and save results as JSON.
        
        Args:
            current_data (Union[pd.DataFrame, str]): Current data as DataFrame or path to CSV file
            drift_threshold (float): Threshold for drift detection (default: 0.05)
            output_dir (str): Directory to save the drift report (default: "drift_reports")
            
        Returns:
            str: Path to the generated drift report
        """
        try:
            # Load current data if it's a file path
            if isinstance(current_data, str):
                current_data = pd.read_csv(current_data)
                
            # Create current profile
            current_profile = why.log(current_data).profile()
            
            # Get profile views
            reference_view = self.reference_profile.view()
            current_view = current_profile.view()
            
            # Create drift report
            drift_report = {
                'columns': {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Compare distributions for each column
            for column in reference_view.get_columns():
                if column in current_view.get_columns():
                    ref_col = reference_view.get_column(column)
                    curr_col = current_view.get_column(column)
                    
                    # Get distribution metrics
                    ref_dist = ref_col.get_metric("distribution")
                    curr_dist = curr_col.get_metric("distribution")
                    
                    if ref_dist and curr_dist:
                        # Calculate KL divergence using the to_summary_dict method
                        ref_summary = ref_dist.to_summary_dict()
                        curr_summary = curr_dist.to_summary_dict()
                        
                        # Get KL divergence from summary
                        kl_div = ref_summary.get('kl_divergence', 0.0)
                        
                        drift_report['columns'][column] = {
                            'distribution': {
                                'kl_divergence': kl_div,
                                'drift_detected': kl_div > drift_threshold
                            }
                        }
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"drift_report_{timestamp}.json")
            
            # Save the report as JSON
            with open(output_path, 'w') as f:
                json.dump(drift_report, f, indent=2)
            
            # Log drift metrics
            drift_metrics = {
                'drift_detected': False,
                'drift_score': 0.0,
                'features_drifted': []
            }
            
            # Check for drift in each feature
            for column in drift_report['columns']:
                if 'distribution' in drift_report['columns'][column]:
                    dist_metrics = drift_report['columns'][column]['distribution']
                    if 'kl_divergence' in dist_metrics:
                        kl_div = dist_metrics['kl_divergence']
                        if kl_div > drift_threshold:
                            drift_metrics['drift_detected'] = True
                            drift_metrics['features_drifted'].append(column)
                            drift_metrics['drift_score'] = max(drift_metrics['drift_score'], kl_div)
            
            logger.info(f"Drift report saved to: {output_path}")
            logger.info(f"Drift metrics: {drift_metrics}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error detecting drift: {str(e)}")
            raise 
