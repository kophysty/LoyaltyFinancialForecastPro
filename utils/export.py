import pandas as pd
import json
from datetime import datetime
import plotly
import os
from utils.logging_config import log_info, log_error

def export_financial_data(data, format='csv'):
    """Export financial data to various formats"""
    try:
        # Create export directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'csv':
            df = pd.DataFrame(data)
            filename = f'exports/financial_data_{timestamp}.csv'
            df.to_csv(filename, index=False)
            log_info(f"Financial data exported to CSV: {filename}")
            return filename
            
        elif format == 'json':
            filename = f'exports/financial_data_{timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            log_info(f"Financial data exported to JSON: {filename}")
            return filename
            
    except Exception as e:
        log_error(e, context="Error exporting financial data")
        raise

def export_chart(figure, chart_name):
    """Export Plotly chart as HTML"""
    try:
        # Create export directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'exports/{chart_name}_{timestamp}.html'
        
        plotly.io.write_html(figure, filename)
        log_info(f"Chart exported to HTML: {filename}")
        return filename
        
    except Exception as e:
        log_error(e, context="Error exporting chart")
        raise
