"""
Tools for Crew.ai agents to perform actions
"""
from langchain.tools import Tool
from typing import Dict, List, Any
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from models import Flight, PricePrediction

class FlightTools:
    """Collection of tools for flight operations"""
    
    @staticmethod
    def search_flights_tool() -> Tool:
        """Tool to search for flights"""
        def search(query: str) -> str:
            """
            Search for flights. Format: origin,destination,date
            Example: 'LAX,JFK,2024-03-15'
            """
            try:
                parts = query.split(',')
                # Implement actual flight search here
                # This is a mock implementation
                flights = [
                    {
                        "flight_number": "AA101",
                        "price": 450.00,
                        "departure": "08:00",
                        "arrival": "16:30"
                    },
                    {
                        "flight_number": "UA202", 
                        "price": 425.00,
                        "departure": "10:30",
                        "arrival": "18:45"
                    }
                ]
                return json.dumps(flights)
            except Exception as e:
                return f"Error: {str(e)}"
        
        return Tool(
            name="search_flights",
            func=search,
            description="Search for flights between airports on specific date"
        )
    
    @staticmethod
    def predict_prices_tool() -> Tool:
        """Tool to predict future prices"""
        def predict(route_data: str) -> str:
            """
            Predict future prices using ML.
            Input: JSON with route and historical prices
            """
            try:
                data = json.loads(route_data)
                
                # Simple prediction using linear regression
                # In production, use more sophisticated models
                prices = data.get("historical_prices", [])
                if len(prices) < 3:
                    return json.dumps({"error": "Insufficient data"})
                
                # Create time series
                X = np.array(range(len(prices))).reshape(-1, 1)
                y = np.array(prices)
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 7, 14, 30 days
                future_days = [7, 14, 30]
                predictions = {}
                
                for days in future_days:
                    future_x = len(prices) + days
                    pred_price = model.predict([[future_x]])[0]
                    predictions[f"{days}d"] = round(pred_price, 2)
                
                # Determine trend
                slope = model.coef_[0]
                if slope > 1:
                    trend = "rising"
                elif slope < -1:
                    trend = "falling"
                else:
                    trend = "stable"
                
                result = PricePrediction(
                    route=data.get("route", ""),
                    current_price=prices[-1] if prices else 0,
                    predictions=predictions,
                    confidence=0.75,
                    trend=trend,
                    recommendation="Buy now" if trend == "rising" else "Wait",
                    best_booking_window="Next 7 days" if trend == "rising" else "In 2 weeks"
                )
                
                return json.dumps(result.dict(), default=str)
                
            except Exception as e:
                return f"Error predicting: {str(e)}"
        
        return Tool(
            name="predict_prices",
            func=predict,
            description="Predict future flight prices using ML"
        )
    
    @staticmethod
    def analyze_route_tool() -> Tool:
        """Tool to analyze route patterns"""
        def analyze(route: str) -> str:
            """
            Analyze route for patterns, best times, airlines
            Input: 'origin-destination'
            """
            try:
                # Mock analysis - in production, use real data
                analysis = {
                    "route": route,
                    "best_booking_day": "Tuesday",
                    "best_travel_day": "Wednesday", 
                    "cheapest_month": "February",
                    "average_price": 520,
                    "price_range": {"min": 380, "max": 750},
                    "best_airlines": ["Delta", "United"],
                    "typical_discount_percentage": 15,
                    "recommendation": "Book 6-8 weeks in advance for best prices"
                }
                return json.dumps(analysis)
            except Exception as e:
                return f"Error analyzing: {str(e)}"
        
        return Tool(
            name="analyze_route",
            func=analyze,
            description="Analyze route for patterns and best booking strategies"
        )