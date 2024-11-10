import random
from datetime import datetime, timedelta
from typing import List, Dict
import time
import json
from pathlib import Path
from .models import FlightSearchRequest

class MockAirlineAPI:
    def __init__(self):
        # Sample Data
        data_file = Path(__file__).parent / 'airline_data.json'
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.airports = data['airports']
        self.airlines = [tuple(airline) for airline in data['airlines']]
        self.aircraft_types = data['aircraft_types']
        self.flight_classes = data['flight_classes']
        

    def search_flights(self, request: FlightSearchRequest) -> List[Dict]:
        """
        Generate dynamic flight results based on search criteria.
        Sometimes returns empty list to simulate no availability.
        """
        print(f"Searching for flights...")
        # Simulate API latency
        time.sleep(random.uniform(0.5, 2))
        
        # Random chance (5%) of no flights available
        if random.random() < 0.05:
            return []
            
        # Random number of flights to return (2-5)
        num_flights = random.randint(2, 5)

        route_info = {
            "base_price": random.randint(200, 600),
            "duration": random.randint(120, 480)
        }


        flights = []
        used_flight_numbers = set()
        
        for _ in range(num_flights):
            # Randomly select airline
            airline_name, airline_code = random.choice(self.airlines)
            
            # Generate unique flight number
            while True:
                flight_number = f"{airline_code}{random.randint(1000, 9999)}"
                if flight_number not in used_flight_numbers:
                    used_flight_numbers.add(flight_number)
                    break
            
            # Generate departure time
            base_date = datetime.strptime(request.departure_date, "%Y-%m-%d")
            departure_hour = random.randint(6, 22)  # Flights between 6 AM and 10 PM
            departure_time = base_date.replace(hour=departure_hour, 
                                            minute=random.choice([0, 15, 30, 45]))
            
            # Calculate arrival time
            duration = route_info["duration"] + random.randint(-30, 30)  # Add some variance
            arrival_time = departure_time + timedelta(minutes=duration)
            
            # Generate price with various factors
            base_price = route_info["base_price"]
            price_multiplier = random.uniform(0.8, 1.4)  # Price variance
            time_multiplier = 1 + (abs(departure_hour - 14) / 20)  # Higher prices for peak times
            demand_multiplier = random.uniform(0.9, 1.3)  # Random demand factor
            
            final_price = base_price * price_multiplier * time_multiplier * demand_multiplier
            
            # Determine available seats
            if random.random() < 0.2:  # 20% chance of very limited seats
                available_seats = random.randint(1, 3)
            else:
                available_seats = random.randint(4, 50)
            
            # Randomly select travel class if not specified
            travel_class = (request.preferred_class if request.preferred_class 
                          else random.choice(self.flight_classes))
            
            # Adjust price based on class
            if travel_class == "Business":
                final_price *= 2.5
            elif travel_class == "First":
                final_price *= 4.0
            
            flight = {
                "flight_id": f"{flight_number}-{request.departure_date}",
                "airline": airline_name,
                "flight_number": flight_number,
                "origin": request.departure_city,
                "origin_city": self.airports.get(request.departure_city, "Unknown"),
                "destination": request.arrival_city,
                "destination_city": self.airports.get(request.arrival_city, "Unknown"),
                "departure_time": departure_time.strftime("%Y-%m-%d %H:%M"),
                "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M"),
                "duration_minutes": duration,
                "price": round(final_price, 2),
                "seats_available": available_seats,
                "aircraft_type": random.choice(self.aircraft_types),
                "class": travel_class,
                "refundable": random.choice([True, False])
            }
            
            # Only add flight if it passes all filters
            if (flight["seats_available"] >= request.num_passengers and
                self._passes_filters(flight, request)):
                flights.append(flight)
        
        print(f"Found {len(flights)} flights")
        for flight in flights:
            print(f"Flight ID: {flight['flight_id']}")
            print(f"Airline: {flight['airline']}")
            print(f"Flight Number: {flight['flight_number']}")
            print(f"Origin: {flight['origin']} ({flight['origin_city']})")
            print(f"Destination: {flight['destination']} ({flight['destination_city']})")
            print(f"Departure Time: {flight['departure_time']}")
            print(f"Arrival Time: {flight['arrival_time']}")
            print(f"Duration (minutes): {flight['duration_minutes']}")
            print(f"Price: ${flight['price']:.2f}")
            print(f"Seats Available: {flight['seats_available']}")
            print(f"Aircraft Type: {flight['aircraft_type']}")
            print(f"Class: {flight['class']}")
            print(f"Refundable: {'Yes' if flight['refundable'] else 'No'}")
            print("---")  # Separator for each flight

        return flights

    def _passes_filters(self, flight: Dict, request: FlightSearchRequest) -> bool:
        """Helper method to check if a flight passes all specified filters."""
        # Check max price
        if request.max_price and flight["price"] > request.max_price:
            return False

        # Check max duration
        if request.max_duration and flight["duration_minutes"] > request.max_duration:
            return False

        # Check preferred airlines
        if (request.preferred_airlines and 
            flight["airline"] not in request.preferred_airlines):
            return False

        # Check nonstop/max stops (for future implementation of multi-leg flights)
        if request.nonstop_only:
            # Currently all flights are nonstop, but prepared for future expansion
            pass

        # Check departure time range
        if request.departure_time_range:
            dept_time = datetime.strptime(flight["departure_time"], "%Y-%m-%d %H:%M")
            start_time = datetime.strptime(f"{dept_time.date()} {request.departure_time_range[0]}", 
                                         "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(f"{dept_time.date()} {request.departure_time_range[1]}", 
                                       "%Y-%m-%d %H:%M")
            if not (start_time <= dept_time <= end_time):
                return False

        # Check arrival time range
        if request.arrival_time_range:
            arr_time = datetime.strptime(flight["arrival_time"], "%Y-%m-%d %H:%M")
            start_time = datetime.strptime(f"{arr_time.date()} {request.arrival_time_range[0]}", 
                                         "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(f"{arr_time.date()} {request.arrival_time_range[1]}", 
                                       "%Y-%m-%d %H:%M")
            if not (start_time <= arr_time <= end_time):
                return False

        # Check refundable only
        if request.refundable_only and not flight["refundable"]:
            return False

        return True

    def verify_flight(self, flight_id: str, expected_price: float) -> Dict:
        """
        Verify if flight is still available at the expected price.
        Simulates price and availability changes.
        """
        time.sleep(random.uniform(0.2, 1.0))  # Simulate API latency
        
        # 15% chance flight is no longer available
        if random.random() < 0.2:
            return {
                "flight_id": flight_id,
                "available": False,
                "reason": "Flight no longer available"
            }
        
        # 20% chance of price change
        if random.random() < 0.2:
            price_change = expected_price * random.uniform(-0.2, 0.3)
            new_price = round(expected_price + price_change, 2)
            return {
                "flight_id": flight_id,
                "available": True,
                "price_changed": True,
                "original_price": expected_price,
                "new_price": new_price
            }
        
        # Flight available at expected price
        return {
            "flight_id": flight_id,
            "available": True,
            "price_changed": False,
            "price": expected_price
        }
