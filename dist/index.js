"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dotenv_1 = __importDefault(require("dotenv"));
const fs_1 = require("fs");
const path_1 = require("path");
// Load environment variables
dotenv_1.default.config();
// Mock AirbnbService since we don't have access to the actual package
class AirbnbService {
    async search(params) {
        // This is a mock implementation
        console.log('Searching with params:', params);
        return [];
    }
}
// Load preferences from JSON file
function loadPreferences() {
    const preferencesPath = (0, path_1.join)(__dirname, '..', 'preferences.json');
    const rawData = (0, fs_1.readFileSync)(preferencesPath, 'utf-8');
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
        const evaluatedListings = listings.map((listing) => ({
            ...listing,
            score: calculateListingScore(listing, preferences)
        }));
        // Sort by score
        evaluatedListings.sort((a, b) => b.score - a.score);
        // Save results
        const resultsPath = (0, path_1.join)(__dirname, '..', 'results.json');
        (0, fs_1.writeFileSync)(resultsPath, JSON.stringify(evaluatedListings, null, 2));
        console.log(`Results saved to ${resultsPath}`);
    }
    catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}
function calculateListingScore(listing, preferences) {
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
    const matchingAmenities = preferences.amenities.filter(amenity => listing.amenities.includes(amenity));
    score += (matchingAmenities.length / preferences.amenities.length) * 30;
    return Math.max(0, Math.min(100, score));
}
// Run the main function
main().catch(console.error);
