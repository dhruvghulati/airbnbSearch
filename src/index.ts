import dotenv from 'dotenv';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { AirbnbService } from './services/airbnb';

// Load environment variables
dotenv.config();

// Types
interface TripPreferences {
  groupSize: number;
  location: string;
  checkIn: string;
  checkOut: string;
  budget: {
    min: number;
    max: number;
  };
  bedrooms: number;
  bathrooms: number;
  amenities: string[];
  vibes: string[];
  walkabilityImportance: number;
}

interface Listing {
  id: string;
  name: string;
  price: number;
  amenities: string[];
  walkScore?: number;
  location: {
    lat: number;
    lng: number;
    address: string;
  };
}

interface EvaluatedListing extends Listing {
  score: number;
}

// Load preferences from JSON file
function loadPreferences(): TripPreferences {
  const preferencesPath = join(__dirname, '..', 'preferences.json');
  const rawData = readFileSync(preferencesPath, 'utf-8');
  return JSON.parse(rawData);
}

async function main() {
  try {
    console.log('Loading preferences...');
    const preferences = loadPreferences();

    console.log('Initializing Airbnb service...');
    const airbnbService = new AirbnbService();

    console.log('Searching for listings...');
    const listings = await airbnbService.search({
      location: preferences.location,
      checkIn: new Date(preferences.checkIn),
      checkOut: new Date(preferences.checkOut),
      guests: preferences.groupSize,
      priceMin: preferences.budget.min,
      priceMax: preferences.budget.max,
      bedrooms: preferences.bedrooms,
      bathrooms: preferences.bathrooms,
      amenities: preferences.amenities
    });

    console.log(`Found ${listings.length} listings`);
    
    // Process and evaluate listings based on preferences
    const evaluatedListings = listings.map((listing: Listing): EvaluatedListing => ({
      ...listing,
      score: calculateListingScore(listing, preferences)
    }));

    // Sort by score
    evaluatedListings.sort((a: EvaluatedListing, b: EvaluatedListing) => b.score - a.score);

    // Save results
    const resultsPath = join(__dirname, '..', 'results.json');
    writeFileSync(resultsPath, JSON.stringify(evaluatedListings, null, 2));
    console.log(`Results saved to ${resultsPath}`);

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

function calculateListingScore(listing: Listing, preferences: TripPreferences): number {
  // Implement scoring logic based on preferences
  // This is a simple example - you can make it more sophisticated
  let score = 100;

  // Price score
  const priceRange = preferences.budget.max - preferences.budget.min;
  const priceDiff = listing.price - preferences.budget.min;
  score -= (priceDiff / priceRange) * 20; // Price affects up to 20 points

  // Location/walkability score
  if (listing.walkScore) {
    score += (listing.walkScore / 100) * preferences.walkabilityImportance;
  }

  // Amenities score
  const matchingAmenities = preferences.amenities.filter(amenity => 
    listing.amenities.includes(amenity)
  );
  score += (matchingAmenities.length / preferences.amenities.length) * 30;

  return Math.max(0, Math.min(100, score));
}

// Run the main function
main().catch(console.error); 