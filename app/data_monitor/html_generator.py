from typing import Dict
from datetime import datetime

class HTMLReportGenerator:
    """
    A class to generate HTML reports for data drift detection results.
    """
    
    @staticmethod
    def generate_drift_report(drift_metrics: Dict, drift_report: Dict) -> str:
        """
        Generate an HTML report for the drift detection results.
        
        Args:
            drift_metrics (dict): Dictionary containing drift metrics
            drift_report (dict): Dictionary containing detailed drift report
            
        Returns:
            str: HTML content of the report
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Drift Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1, h2 {{
                    color: #333;
                }}
                .summary {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }}
                .drift-detected {{
                    color: #dc3545;
                    font-weight: bold;
                }}
                .no-drift {{
                    color: #28a745;
                    font-weight: bold;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f8f9fa;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .timestamp {{
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Data Drift Report</h1>
                <div class="timestamp">Generated at: {drift_report['timestamp']}</div>
                
                <div class="summary">
                    <h2>Summary</h2>
                    <p>Drift Detected: <span class="{'drift-detected' if drift_metrics['drift_detected'] else 'no-drift'}">
                        {'Yes' if drift_metrics['drift_detected'] else 'No'}
                    </span></p>
                    <p>Overall Drift Score: {drift_metrics['drift_score']:.4f}</p>
                    <p>Number of Features with Drift: {len(drift_metrics['features_drifted'])}</p>
                </div>
                
                <h2>Detailed Results</h2>
                <table>
                    <tr>
                        <th>Feature</th>
                        <th>KL Divergence</th>
                        <th>Drift Detected</th>
                    </tr>
        """
        
        for column in drift_report['columns']:
            dist_metrics = drift_report['columns'][column]['distribution']
            kl_div = dist_metrics['kl_divergence']
            drift_detected = dist_metrics['drift_detected']
            
            html_content += f"""
                    <tr>
                        <td>{column}</td>
                        <td>{kl_div:.4f}</td>
                        <td class="{'drift-detected' if drift_detected else 'no-drift'}">
                            {'Yes' if drift_detected else 'No'}
                        </td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        return html_content 