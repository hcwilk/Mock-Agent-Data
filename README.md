# Mock Flight API

A mock flight API for testing travel agent applications. This package simulates airline booking systems with realistic delays and random variations in pricing and availability.

## Installation

```bash
pip install mock-flight-api
```

## Usage

```python
from mock_flight_api import MockAirlineAPI, FlightSearchRequest
# Initialize the API
api = MockAirlineAPI()
# Create a search request
request = FlightSearchRequest(
departure_city="JFK",
arrival_city="LAX",
departure_date="2024-11-09",
num_passengers=2,
preferred_class="Business"
)
# Search for flights
results = api.search_flights(request)
# Verify a specific flight
if results:
flight = results[0]
verification = api.verify_flight(flight['flight_id'], flight['price'])
```

