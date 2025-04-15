import { searchListings, getListingDetails } from '@openbnb/mcp-server-airbnb';

export interface AirbnbSearchParams {
  location: string;
  checkIn: Date;
  checkOut: Date;
  guests: number;
  priceMin: number;
  priceMax: number;
  bedrooms: number;
  bathrooms: number;
  amenities: string[];
}

export interface AirbnbListing {
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

export class AirbnbService {
  async search(params: AirbnbSearchParams): Promise<AirbnbListing[]> {
    try {
      // Search for listings using MCP server
      const searchResults = await searchListings({
        location: params.location,
        checkin: params.checkIn.toISOString().split('T')[0],
        checkout: params.checkOut.toISOString().split('T')[0],
        adults: params.guests,
        min_price: params.priceMin,
        max_price: params.priceMax,
        min_bedrooms: params.bedrooms,
        min_bathrooms: params.bathrooms,
        amenities: params.amenities,
        ignore_robots_txt: true
      });

      // Get detailed information for each listing
      const listings = await Promise.all(
        searchResults.listings.map(async (listing: any) => {
          const details = await getListingDetails({
            id: listing.id,
            checkin: params.checkIn.toISOString().split('T')[0],
            checkout: params.checkOut.toISOString().split('T')[0],
            adults: params.guests,
            ignore_robots_txt: true
          });

          return {
            id: listing.id,
            name: listing.name,
            price: listing.price,
            amenities: listing.amenities,
            walkScore: listing.neighborhood_info?.walk_score,
            location: {
              lat: listing.lat,
              lng: listing.lng,
              address: listing.public_address
            }
          };
        })
      );

      return listings;
    } catch (error) {
      console.error('Error searching Airbnb listings:', error);
      throw error;
    }
  }
} 