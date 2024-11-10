import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import time

@dataclass
class FlightSearchRequest:
    departure_city: str
    arrival_city: str
    departure_date: str  # YYYY-MM-DD format
    num_passengers: int = 1
    preferred_class: Optional[str] = None
    max_price: Optional[float] = None
    max_duration: Optional[int] = None  # in minutes
    preferred_airlines: Optional[List[str]] = None
    nonstop_only: bool = False
    max_stops: Optional[int] = None
    departure_time_range: Optional[tuple[str, str]] = None  # ("HH:MM", "HH:MM")
    arrival_time_range: Optional[tuple[str, str]] = None    # ("HH:MM", "HH:MM")
    refundable_only: bool = False
