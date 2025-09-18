from crewai import Agent, Task, Crew, Process
from langchain.llms import OpenAI
from tools import FlightTools
from typing import List, Dict, Any
from config import config

class FlightAgents:
    """Collection of specialized agents"""
    
    def __init__(self):
        self.llm = OpenAI(api_key=config.OPENAI_API_KEY, model=config.MODEL_NAME)
        self.tools = FlightTools()
    
    def search_specialist(self) -> Agent:
        """Agent specialized in flight searches"""
        return Agent(
            role="Flight Search Specialist",
            goal="Find the best flight options based on user requirements",
            backstory="""You are an expert at searching for flights. You know all 
            the tricks to find the best deals, hidden city ticketing, optimal 
            connection times, and which airlines offer the best service.""",
            tools=[self.tools.search_flights_tool()],
            llm=self.llm,
            verbose=True
        )
    
    def price_analyst(self) -> Agent:
        """Agent specialized in price analysis and predictions"""
        return Agent(
            role="Aviation Price Analyst",
            goal="Analyze and predict flight prices to find optimal booking times",
            backstory="""You are a data scientist specializing in airline pricing. 
            You understand seasonal patterns, demand curves, and can predict when 
            prices will drop or rise. You use advanced analytics to help users 
            save money.""",
            tools=[self.tools.predict_prices_tool(), self.tools.analyze_route_tool()],
            llm=self.llm,
            verbose=True
        )
    
    def booking_assistant(self) -> Agent:
        """Agent specialized in booking and travel planning"""
        return Agent(
            role="Travel Booking Assistant",
            goal="Help users make booking decisions and manage their travel plans",
            backstory="""You are a professional travel agent with years of experience. 
            You help users understand fare rules, choose the best flights for their 
            needs, and ensure smooth travel experiences.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )
    
    def notification_specialist(self) -> Agent:
        """Agent specialized in creating notifications"""
        return Agent(
            role="Communication Specialist",
            goal="Create clear, actionable notifications for users via Telegram",
            backstory="""You excel at crafting concise, informative messages that 
            help users make quick decisions. You know how to use emojis effectively 
            and format messages for maximum clarity on Telegram.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )

class FlightTasks:
    """Collection of tasks for agents"""
    
    @staticmethod
    def search_flights_task(agent: Agent, origin: str, destination: str, 
                           date: str) -> Task:
        return Task(
            description=f"""Search for flights from {origin} to {destination} 
            on {date}. Find at least 5 options and rank them by:
            1. Price
            2. Duration
            3. Departure time convenience
            4. Airline quality
            
            Provide detailed information for each flight.""",
            agent=agent,
            expected_output="List of flights with rankings"
        )
    
    @staticmethod
    def predict_prices_task(agent: Agent, route: str) -> Task:
        return Task(
            description=f"""Analyze price trends for route {route} and predict:
            1. Expected prices for next 7, 14, and 30 days
            2. Whether prices will rise or fall
            3. Best time to book
            4. Confidence level in predictions
            
            Provide clear reasoning for your predictions.""",
            agent=agent,
            expected_output="Price predictions with recommendations"
        )
    
    @staticmethod
    def create_alert_task(agent: Agent, flights: List[Dict], 
                         user_preferences: Dict) -> Task:
        return Task(
            description=f"""Based on the flight search results and user preferences, 
            create a Telegram notification that:
            1. Highlights the best options
            2. Shows price comparisons
            3. Includes actionable buttons
            4. Uses emojis for clarity
            5. Is concise but informative
            
            Format for Telegram with proper markdown.""",
            agent=agent,
            expected_output="Formatted Telegram message"
        )
