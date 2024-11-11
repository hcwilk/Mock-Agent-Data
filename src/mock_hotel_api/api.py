import random
from datetime import datetime, timedelta
from typing import List, Dict
import time
import json
from pathlib import Path
from .models import HotelSearchRequest

class MockHotelAPI:
    def __init__(self):
        # Load sample data
        data_file = Path(__file__).parent / 'hotel_data.json'
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.cities = data['cities']
        self.hotel_chains = data['hotel_chains']
        self.room_types = data['room_types']
        self.amenities = data['amenities']

    def search_hotels(self, request: HotelSearchRequest) -> List[Dict]:
        """
        Generate dynamic hotel results based on search criteria.
        Sometimes returns empty list to simulate no availability.
        """
        print(f"Searching for hotels in {request.city}...")
        # Simulate API latency
        time.sleep(random.uniform(0.5, 2))
        
        # Random chance (5%) of no hotels available
        if random.random() < 0.05:
            return []
            
        # Random number of hotels to return (3-8)
        num_hotels = random.randint(3, 8)
        
        hotels = []
        used_hotel_ids = set()
        
        for _ in range(num_hotels):
            # Generate hotel details
            chain_name, chain_code = random.choice(self.hotel_chains)
            
            # Generate unique hotel ID
            while True:
                hotel_id = f"{chain_code}{random.randint(1000, 9999)}"
                if hotel_id not in used_hotel_ids:
                    used_hotel_ids.add(hotel_id)
                    break
            
            # Generate base price with location factor
            base_price = random.randint(80, 400)
            location_multiplier = random.uniform(0.8, 1.5)
            
            # Calculate total nights
            check_in = datetime.strptime(request.check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(request.check_out_date, "%Y-%m-%d")
            num_nights = (check_out - check_in).days
            
            # Generate room details
            room_type = (request.room_type if request.room_type 
                        else random.choice(self.room_types))
            
            # Adjust price based on room type
            room_type_multipliers = {
                "Standard": 1.0,
                "Deluxe": 1.5,
                "Suite": 2.5,
                "Executive": 3.0,
                "Presidential": 5.0
            }
            
            final_price = (base_price * location_multiplier * 
                         room_type_multipliers[room_type])
            
            # Random amenities
            selected_amenities = random.sample(
                self.amenities, 
                random.randint(5, len(self.amenities))
            )
            
            # Generate rating
            rating = round(random.uniform(3.0, 5.0), 1)
            
            # Distance to city center
            distance_to_center = round(random.uniform(0.1, 15.0), 1)
            
            hotel = {
                "hotel_id": hotel_id,
                "name": f"{chain_name} {self.cities[request.city]}",
                "chain": chain_name,
                "address": f"{random.randint(1, 999)} {random.choice(['Main', 'First', 'Park', 'Lake', 'River'])} St, {self.cities[request.city]}",
                "city": request.city,
                "city_name": self.cities[request.city],
                "rating": rating,
                "room_type": room_type,
                "price_per_night": round(final_price, 2),
                "total_price": round(final_price * num_nights, 2),
                "num_nights": num_nights,
                "distance_to_center": distance_to_center,
                "amenities": selected_amenities,
                "breakfast_included": random.choice([True, False]),
                "free_cancellation": random.choice([True, False]),
                "rooms_available": random.randint(1, 10)
            }
            
            if self._passes_filters(hotel, request):
                hotels.append(hotel)
        
        print(f"Found {len(hotels)} hotels")
        for hotel in hotels:
            print(f"Hotel ID: {hotel['hotel_id']}")
            print(f"Name: {hotel['name']}")
            print(f"Rating: {hotel['rating']} stars")
            print(f"Room Type: {hotel['room_type']}")
            print(f"Price per night: ${hotel['price_per_night']:.2f}")
            print(f"Total price: ${hotel['total_price']:.2f}")
            print(f"Distance to center: {hotel['distance_to_center']}km")
            print("---")
        
        return hotels

    def _passes_filters(self, hotel: Dict, request: HotelSearchRequest) -> bool:
        """Helper method to check if a hotel passes all specified filters."""
        # Check max price
        if (request.max_price_per_night and 
            hotel["price_per_night"] > request.max_price_per_night):
            return False

        # Check minimum rating
        if request.min_rating and hotel["rating"] < request.min_rating:
            return False

        # Check preferred chains
        if (request.preferred_chains and 
            hotel["chain"] not in request.preferred_chains):
            return False

        # Check distance to center
        if (request.max_distance_to_center and 
            hotel["distance_to_center"] > request.max_distance_to_center):
            return False

        # Check breakfast included
        if (request.breakfast_included and 
            not hotel["breakfast_included"]):
            return False

        # Check free cancellation
        if (request.free_cancellation and 
            not hotel["free_cancellation"]):
            return False

        # Check required amenities
        if request.amenities:
            if not all(amenity in hotel["amenities"] 
                      for amenity in request.amenities):
                return False

        # Check room availability
        if hotel["rooms_available"] < request.num_rooms:
            return False

        return True

    def verify_hotel(self, hotel_id: str, expected_price: float) -> Dict:
        """
        Verify if hotel is still available at the expected price.
        Simulates price and availability changes.
        """
        time.sleep(random.uniform(0.2, 1.0))  # Simulate API latency
        
        # 15% chance hotel is no longer available
        if random.random() < 0.15:
            return {
                "hotel_id": hotel_id,
                "available": False,
                "reason": "No rooms available for selected dates"
            }
        
        # 25% chance of price change
        if random.random() < 0.25:
            price_change = expected_price * random.uniform(-0.15, 0.25)
            new_price = round(expected_price + price_change, 2)
            return {
                "hotel_id": hotel_id,
                "available": True,
                "price_changed": True,
                "original_price": expected_price,
                "new_price": new_price
            }
        
        # Hotel available at expected price
        return {
            "hotel_id": hotel_id,
            "available": True,
            "price_changed": False,
            "price": expected_price
        } 