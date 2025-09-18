"""
Background monitoring system for tracked routes and alerts
"""
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict
from database import Database
from agents import FlightAgents, FlightTasks
from crewai import Crew, Process
from telegram import Bot
from config import config
import logging

logger = logging.getLogger(__name__)

class FlightMonitor:
    """Background monitoring system"""
    
    def __init__(self):
        self.db = Database()
        self.agents = FlightAgents()
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        
    async def check_tracked_routes(self):
        """Check all tracked routes for price changes"""
        routes = self.db.get_active_routes()
        
        for route in routes:
            try:
                await self._check_route(route)
            except Exception as e:
                logger.error(f"Error checking route {route['id']}: {e}")
    
    async def _check_route(self, route: Dict):
        """Check single route for price changes"""
        # Execute search crew
        search_agent = self.agents.search_specialist()
        analyst_agent = self.agents.price_analyst()
        
        search_task = Task(
            description=f"Search flights for {route['origin']} to {route['destination']}",
            agent=search_agent
        )
        
        crew = Crew(
            agents=[search_agent, analyst_agent],
            tasks=[search_task],
            process=Process.sequential
        )
        
        results = crew.kickoff()
        
        # Parse results and check for price drops
        current_best_price = self._extract_best_price(results)
        
        if route.get('best_price'):
            if current_best_price < route['best_price'] * 0.95:  # 5% drop
                await self._send_price_alert(route, current_best_price)
        
        # Update database
        self._update_route_price(route['id'], current_best_price)
    
    async def _send_price_alert(self, route: Dict, new_price: float):
        """Send price drop alert to user"""
        message = f"""
🚨 <b>PRICE DROP ALERT!</b>

Route: {route['origin']} → {route['destination']}
Previous best: ${route.get('best_price', 0):.2f}
Current best: ${new_price:.2f}
Savings: ${(route.get('best_price', 0) - new_price):.2f}

<i>Book now before prices go back up!</i>
        """
        
        await self.bot.send_message(
            chat_id=route['user_id'],
            text=message,
            parse_mode='HTML'
        )
    
    def _extract_best_price(self, results: str) -> float:
        """Extract best price from crew results"""
        # Parse crew output for price
        # This is simplified - would need proper parsing
        return 425.0
    
    def _update_route_price(self, route_id: str, price: float):
        """Update route with new price"""
        session = self.db.Session()
        try:
            route = session.query(TrackedRoute).filter_by(id=route_id).first()
            if route:
                route.best_price = price
                route.last_check = datetime.utcnow()
                
                # Update price history
                history = route.price_history or []
                history.append({
                    "price": price,
                    "timestamp": datetime.utcnow().isoformat()
                })
                route.price_history = history[-100:]  # Keep last 100
                
                session.commit()
        finally:
            session.close()
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        logger.info("Starting flight monitoring system...")
        
        # Schedule checks
        schedule.every(config.CHECK_INTERVAL).minutes.do(
            lambda: asyncio.run(self.check_tracked_routes())
        )
        
        # Initial check
        asyncio.run(self.check_tracked_routes())
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)