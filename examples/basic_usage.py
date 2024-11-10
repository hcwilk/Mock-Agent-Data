from mock_flight_api import MockAirlineAPI, FlightSearchRequest

def main():
    api = MockAirlineAPI()
    
    # Test different scenarios
    requests = [
        FlightSearchRequest(
            departure_city="JFK",
            arrival_city="LAX",
            departure_date="2024-11-09"
        ),
        FlightSearchRequest(
            departure_city="SFO",
            arrival_city="JFK",
            departure_date="2024-11-09",
            preferred_class="Business",
            max_price=1000
        )
    ]
    
    for request in requests:
        print(f"\nSearching flights from {request.departure_city} to {request.arrival_city}")
        results = api.search_flights(request)
        print(f"Found {len(results)} flights")

if __name__ == "__main__":
    main()
