from typing import List, Dict, Any, Optional
from datetime import date
from decimal import Decimal
import logging
from models.input_model import TripPreferences, Location

logger = logging.getLogger(__name__)

class AirbnbService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _search_location(self, location: Location, preferences: TripPreferences) -> List[Dict[Any, Any]]:
        """
        Search for listings in a specific location using the Airbnb MCP server
        """
        try:
            from mcp_server_openbnb import search_listings
            
            # Convert location to search string
            location_str = f"{location.city}"
            if location.state:
                location_str += f", {location.state}"
            if location.country:
                location_str += f", {location.country}"
            
            # Perform the search
            results = search_listings(
                location=location_str,
                checkin=preferences.check_in_date.isoformat(),
                checkout=preferences.check_out_date.isoformat(),
                adults=preferences.group_size,
                max_price=float(preferences.max_budget_per_night),
                min_price=0,  # We'll filter results later based on other criteria
                min_bedrooms=preferences.min_bedrooms,
                ignore_robots_txt=True  # Since we're doing automated search
            )
            
            return results.get('listings', [])
        except Exception as e:
            self.logger.error(f"Error searching Airbnb for location {location}: {str(e)}")
            return []

    def _get_listing_details(self, listing_id: str, preferences: TripPreferences) -> Optional[Dict[Any, Any]]:
        """
        Get detailed information about a specific listing
        """
        try:
            from mcp_server_openbnb import get_listing_details
            
            details = get_listing_details(
                id=listing_id,
                checkin=preferences.check_in_date.isoformat(),
                checkout=preferences.check_out_date.isoformat(),
                adults=preferences.group_size,
                ignore_robots_txt=True
            )
            
            return details
        except Exception as e:
            self.logger.error(f"Error getting details for listing {listing_id}: {str(e)}")
            return None

    def search_listings(self, preferences: TripPreferences) -> List[Dict[Any, Any]]:
        """
        Search for listings across all preferred locations
        """
        all_listings = []
        
        for location in preferences.locations:
            listings = self._search_location(location, preferences)
            all_listings.extend(listings)
            
            # Get detailed information for each listing
            for listing in listings:
                if details := self._get_listing_details(listing['id'], preferences):
                    listing.update(details)
        
        return all_listings 