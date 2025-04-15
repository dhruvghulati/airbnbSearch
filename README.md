# Airbnb Search Tool

A TypeScript-based tool for searching Airbnb listings using the official MCP server.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory (if needed for any API keys)

3. Create a `preferences.json` file with your search preferences (see example below)

## Usage

Run the search:
```bash
npm start
```

Results will be saved to `results.json`.

## Preferences Format

Example `preferences.json`:
```json
{
  "group_size": 14,
  "locations": [
    {
      "city": "Split",
      "state": "",
      "country": "Croatia"
    }
  ],
  "check_in_date": "2024-09-10",
  "check_out_date": "2024-09-14",
  "max_budget_per_night": 2000,
  "min_bedrooms": 8,
  "min_bathrooms": 4,
  "desired_amenities": [
    "Pool",
    "Garden",
    "Air Conditioning"
  ],
  "preferred_vibes": [
    "Luxury",
    "Historic"
  ],
  "walkability_important": false
}
```

## Development

- Build: `npm run build`
- Test: `npm test`
