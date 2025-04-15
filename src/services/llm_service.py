from typing import List, Dict, Any
import openai
import os
from dotenv import load_dotenv
from models.input_model import TripPreferences

load_dotenv()

class LLMService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

    def evaluate_listing(self, listing: Dict[Any, Any], preferences: TripPreferences) -> Dict[str, Any]:
        """
        Evaluate a single listing against the user's preferences using GPT-4
        """
        # Construct the prompt
        prompt = f"""
        Evaluate this Airbnb listing against the following preferences:
        
        Group Size: {preferences.group_size} people
        Budget per night: ${preferences.max_budget_per_night}
        Dates: {preferences.check_in_date} to {preferences.check_out_date}
        Desired Amenities: {', '.join(preferences.desired_amenities) if preferences.desired_amenities else 'No specific preferences'}
        Preferred Vibes: {', '.join(preferences.preferred_vibes) if preferences.preferred_vibes else 'No specific preferences'}
        Walkability Important: {'Yes' if preferences.walkability_important else 'No'}
        
        Listing Details:
        - Title: {listing.get('name', 'N/A')}
        - Price per night: ${listing.get('price', 'N/A')}
        - Location: {listing.get('location', {}).get('address', 'N/A')}
        - Number of bedrooms: {listing.get('bedrooms', 'N/A')}
        - Number of bathrooms: {listing.get('bathrooms', 'N/A')}
        - Amenities: {', '.join(listing.get('amenities', []))}
        
        Provide a concise evaluation focusing on:
        1. How well it matches the group's needs
        2. Value for money
        3. Location and accessibility
        4. Special features or concerns
        
        Format the response as a JSON with these fields:
        - relevance_score (0-100)
        - summary (2-3 sentences)
        - pros (list)
        - cons (list)
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that evaluates Airbnb listings based on user preferences."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse the response
            evaluation = response.choices[0].message.content
            
            # Add the evaluation to the listing
            listing['llm_evaluation'] = evaluation
            
            return listing
        except Exception as e:
            listing['llm_evaluation'] = {
                "relevance_score": 0,
                "summary": f"Error evaluating listing: {str(e)}",
                "pros": [],
                "cons": ["Failed to evaluate"]
            }
            return listing

    def evaluate_listings(self, listings: List[Dict[Any, Any]], preferences: TripPreferences) -> List[Dict[Any, Any]]:
        """
        Evaluate all listings against the user's preferences
        """
        evaluated_listings = []
        
        for listing in listings:
            evaluated_listing = self.evaluate_listing(listing, preferences)
            evaluated_listings.append(evaluated_listing)
        
        # Sort listings by relevance score
        evaluated_listings.sort(
            key=lambda x: x.get('llm_evaluation', {}).get('relevance_score', 0),
            reverse=True
        )
        
        return evaluated_listings 