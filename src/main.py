import logging
from datetime import datetime
from typing import Dict, Any
import json
from models.input_model import TripPreferences, Location
from services.airbnb_service import AirbnbService
from services.llm_service import LLMService
from services.sheets_service import ResultsExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_preferences(preferences_file: str) -> TripPreferences:
    """Load preferences from a JSON file"""
    with open(preferences_file, 'r') as f:
        data = json.load(f)
        
        # Convert dates from string to date objects
        data['check_in_date'] = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
        data['check_out_date'] = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        
        # Convert locations to Location objects
        data['locations'] = [Location(**loc) for loc in data['locations']]
        
        return TripPreferences(**data)

def main(preferences_file: str) -> Dict[str, Any]:
    """Main function to orchestrate the Airbnb search and evaluation process"""
    try:
        # Load preferences
        logger.info("Loading preferences...")
        preferences = load_preferences(preferences_file)
        
        # Initialize services
        airbnb_service = AirbnbService()
        llm_service = LLMService()
        exporter = ResultsExporter()
        
        # Search for listings
        logger.info("Searching for Airbnb listings...")
        listings = airbnb_service.search_listings(preferences)
        logger.info(f"Found {len(listings)} listings")
        
        if not listings:
            logger.warning("No listings found matching the criteria")
            return {"status": "error", "message": "No listings found"}
        
        # Evaluate listings using LLM
        logger.info("Evaluating listings...")
        evaluated_listings = llm_service.evaluate_listings(listings, preferences)
        
        # Export to CSV
        logger.info("Exporting results to CSV...")
        output_file = exporter.export_listings(evaluated_listings)
        logger.info(f"Results exported to: {output_file}")
        
        return {
            "status": "success",
            "message": "Search completed successfully",
            "output_file": output_file,
            "total_listings": len(evaluated_listings)
        }
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <preferences_file>")
        sys.exit(1)
    
    result = main(sys.argv[1])
    print(json.dumps(result, indent=2)) 