from mock_hotel_api import MockHotelAPI, HotelSearchRequest

def main():
    api = MockHotelAPI()
    
    # Test different scenarios
    requests = [
        HotelSearchRequest(
            city="NYC",
            check_in_date="2024-07-15",
            check_out_date="2024-07-20",
            num_guests=2
        ),
        HotelSearchRequest(
            city="SFO",
            check_in_date="2024-08-01",
            check_out_date="2024-08-05",
            room_type="Suite",
            max_price_per_night=500,
            min_rating=4.0,
            amenities=["Pool", "Spa"]
        )
    ]
    
    for request in requests:
        print(f"\nSearching hotels in {request.city}")
        results = api.search_hotels(request)
        print(f"Found {len(results)} hotels")

if __name__ == "__main__":
    main() 