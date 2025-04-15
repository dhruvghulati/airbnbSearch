from datetime import date
from typing import List, Optional
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Location:
    city: str
    state: Optional[str] = None
    country: Optional[str] = None

@dataclass
class TripPreferences:
    group_size: int
    locations: List[Location]
    check_in_date: date
    check_out_date: date
    max_budget_per_night: Decimal
    min_bedrooms: Optional[int] = None
    min_bathrooms: Optional[float] = None
    desired_amenities: List[str] = None
    preferred_vibes: List[str] = None
    walkability_important: bool = False

    def __post_init__(self):
        if self.group_size > 16:
            raise ValueError('group_size must be 16 or less')
        if self.check_out_date <= self.check_in_date:
            raise ValueError('check_out_date must be after check_in_date')
        if self.group_size <= 0:
            raise ValueError('group_size must be greater than 0')
        if self.max_budget_per_night <= 0:
            raise ValueError('max_budget_per_night must be greater than 0')
        if self.min_bedrooms is not None and self.min_bedrooms <= 0:
            raise ValueError('min_bedrooms must be greater than 0')
        if self.min_bathrooms is not None and self.min_bathrooms <= 0:
            raise ValueError('min_bathrooms must be greater than 0')
        
        # Initialize empty lists if None
        if self.desired_amenities is None:
            self.desired_amenities = []
        if self.preferred_vibes is None:
            self.preferred_vibes = [] 