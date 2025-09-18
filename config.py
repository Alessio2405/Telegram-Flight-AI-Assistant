import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    # AI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    
    # Telegram (Required)
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
    
    # Flight APIs
    AMADEUS_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_SECRET = os.getenv("AMADEUS_API_SECRET")
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    
    # Features
    ENABLE_AUTO_BOOKING = os.getenv("ENABLE_AUTO_BOOKING", "false").lower() == "true"
    ENABLE_PREDICTIONS = os.getenv("ENABLE_PRICE_PREDICTIONS", "true").lower() == "true"
    ENABLE_EXPENSES = os.getenv("ENABLE_EXPENSE_TRACKING", "true").lower() == "true"
    ENABLE_WEATHER = os.getenv("ENABLE_WEATHER_ALERTS", "true").lower() == "true"
    
    # Limits
    MAX_BOOKING = float(os.getenv("MAX_AUTO_BOOKING_AMOUNT", "1500"))
    CHECK_INTERVAL = int(os.getenv("DEFAULT_CHECK_INTERVAL", "30"))
    PRICE_THRESHOLD = float(os.getenv("PRICE_DROP_THRESHOLD", "5"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///flightbot.db")
    REDIS_URL = os.getenv("REDIS_URL")

config = Config()