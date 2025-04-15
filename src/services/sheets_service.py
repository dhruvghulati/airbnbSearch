import csv
from typing import List, Dict, Any
from datetime import datetime
import os

class ResultsExporter:
    def __init__(self):
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

    def export_listings(self, listings: List[Dict[Any, Any]]) -> str:
        """Export listings to a CSV file and return the filepath"""
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/airbnb_results_{timestamp}.csv'
        
        # Define headers
        headers = [
            'Title',
            'Price per Night',
            'Location',
            'Bedrooms',
            'Bathrooms',
            'Relevance Score',
            'Summary',
            'Pros',
            'Cons',
            'Link'
        ]

        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for listing in listings:
                evaluation = listing.get('llm_evaluation', {})
                row = [
                    listing.get('name', 'N/A'),
                    f"${listing.get('price', 'N/A')}",
                    listing.get('location', {}).get('address', 'N/A'),
                    str(listing.get('bedrooms', 'N/A')),
                    str(listing.get('bathrooms', 'N/A')),
                    str(evaluation.get('relevance_score', 'N/A')),
                    evaluation.get('summary', 'N/A'),
                    '\n'.join(evaluation.get('pros', [])),
                    '\n'.join(evaluation.get('cons', [])),
                    f"https://airbnb.com/rooms/{listing.get('id', '')}"
                ]
                writer.writerow(row)
        
        return filename 