from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum

class ActionType(str, Enum):
    SEARCH_FLIGHTS = "search_flights"
    TRACK_ROUTE = "track_route"
    SET_PRICE_ALERT = "set_price_alert"
    PREDICT_PRICES = "predict_prices"
    BOOK_FLIGHT = "book_flight"
    COMPARE_DATES = "compare_dates"
    ANALYZE_TRENDS = "analyze_trends"
    FIND_ALTERNATIVES = "find_alternatives"
    CHECK_SEAT_MAP = "check_seat_map"
    ADD_TO_CALENDAR = "add_to_calendar"
    TRACK_EXPENSE = "track_expense"
    GET_WEATHER = "get_weather"
    GENERATE_REPORT = "generate_report"
    CREATE_VISUALIZATION = "create_visualization"

class UserCommand(str, Enum):
    START = "/start"
    SEARCH = "/search"
    TRACK = "/track"
    ALERTS = "/alerts"
    PREDICT = "/predict"
    BOOK = "/book"
    EXPENSES = "/expenses"
    SETTINGS = "/settings"
    HELP = "/help"
    CANCEL = "/cancel"
    REPORT = "/report"

class Flight(BaseModel):
    flight_number: str
    airline: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    currency: str = "USD"
    available_seats: Optional[int] = None
    booking_class: str = "economy"
    stops: int = 0
    duration_minutes: int
    booking_url: Optional[str] = None

class RouteTracking(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    user_id: str
    origin: str
    destination: str
    departure_date: Optional[datetime] = None
    flexible_dates: bool = True
    max_price: Optional[float] = None
    preferred_airlines: List[str] = []
    active: bool = True
    check_frequency: int = 30  # minutes
    last_check: Optional[datetime] = None
    best_price_found: Optional[float] = None

class PriceAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    user_id: str
    route: str
    target_price: float
    current_price: Optional[float] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    triggered_at: Optional[datetime] = None

class PricePrediction(BaseModel):
    route: str
    current_price: float
    predictions: Dict[str, float]  # {"7d": price, "14d": price, "30d": price}
    confidence: float
    trend: Literal["rising", "falling", "stable"]
    recommendation: str
    best_booking_window: str

class TelegramContext(BaseModel):
    chat_id: str
    user_id: str
    username: Optional[str]
    current_action: Optional[ActionType] = None
    context_data: Dict[str, Any] = {}
    last_interaction: datetime = Field(default_factory=datetime.now)