from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import date

@dataclass
class HotelSearchRequest:
    city: str
    check_in_date: str  # YYYY-MM-DD format
    check_out_date: str  # YYYY-MM-DD format
    num_rooms: int = 1
    num_guests: int = 2
    room_type: Optional[str] = None
    max_price_per_night: Optional[float] = None
    min_rating: Optional[float] = None
    preferred_chains: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    max_distance_to_center: Optional[float] = None  # in kilometers
    breakfast_included: Optional[bool] = None
    free_cancellation: Optional[bool] = None 