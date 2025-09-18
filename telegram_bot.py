import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import json
from typing import Dict, Any
from database import Database
from agents import FlightAgents, FlightTasks
from crewai import Crew, Process
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlightBot:
    """Main Telegram bot class"""
    
    def __init__(self):
        self.db = Database()
        self.agents = FlightAgents()
        self.tasks = FlightTasks()
        self.user_sessions: Dict[str, Dict] = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        self.db.get_or_create_user(
            str(user.id), 
            user.username, 
            user.first_name
        )
        
        keyboard = [
            [InlineKeyboardButton("✈️ Search Flights", callback_data='search')],
            [InlineKeyboardButton("📍 Track Route", callback_data='track')],
            [InlineKeyboardButton("📊 Price Predictions", callback_data='predict')],
            [InlineKeyboardButton("🔔 My Alerts", callback_data='alerts')],
            [InlineKeyboardButton("💰 Expense Tracking", callback_data='expenses')],
            [InlineKeyboardButton("📈 Analytics", callback_data='analytics')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🤖 <b>Welcome to Flight AI Assistant!</b>

Hello {user.first_name}! I'm your intelligent flight assistant powered by AI agents.

<b>What I can do:</b>
• Search flights with smart recommendations
• Track routes and alert you on price drops
• Predict future prices using ML
• Auto-book flights (when enabled)
• Track travel expenses
• Provide analytics and insights

Choose an action below or type your request!
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def handle_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle flight search request"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        
        # Store session
        self.user_sessions[user_id] = {
            'action': 'search',
            'step': 'origin'
        }
        
        await query.edit_message_text(
            "🛫 <b>Flight Search</b>\n\n"
            "Please enter the <b>departure city</b> or airport code:\n"
            "Example: LAX or Los Angeles",
            parse_mode='HTML'
        )
    
    async def handle_track(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle route tracking setup"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        
        self.user_sessions[user_id] = {
            'action': 'track',
            'step': 'route'
        }
        
        await query.edit_message_text(
            "📍 <b>Route Tracking</b>\n\n"
            "I'll monitor this route and alert you on price drops!\n\n"
            "Enter route in format: <code>origin-destination</code>\n"
            "Example: <code>LAX-JFK</code>",
            parse_mode='HTML'
        )
    
    async def handle_predict(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle price prediction request"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        
        # Run prediction crew
        await query.edit_message_text(
            "🤖 <b>AI agents are analyzing prices...</b>\n\n"
            "Please enter the route to analyze:\n"
            "Format: <code>origin-destination</code>\n"
            "Example: <code>NYC-LON</code>",
            parse_mode='HTML'
        )
        
        self.user_sessions[user_id] = {
            'action': 'predict',
            'step': 'route'
        }
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages based on context"""
        user_id = str(update.effective_user.id)
        text = update.message.text
        
        if user_id not in self.user_sessions:
            await update.message.reply_text(
                "Please use /start to begin or choose an action from the menu."
            )
            return
        
        session = self.user_sessions[user_id]
        action = session.get('action')
        
        if action == 'search':
            await self._handle_search_flow(update, context, session, text)
        elif action == 'track':
            await self._handle_track_flow(update, context, session, text)
        elif action == 'predict':
            await self._handle_predict_flow(update, context, session, text)
    
    async def _handle_search_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                  session: Dict, text: str):
        """Handle multi-step search flow"""
        step = session.get('step')
        user_id = str(update.effective_user.id)
        
        if step == 'origin':
            session['origin'] = text.upper()[:3]  # Airport code
            session['step'] = 'destination'
            await update.message.reply_text(
                f"✅ Origin: <b>{session['origin']}</b>\n\n"
                "Now enter the <b>destination</b>:",
                parse_mode='HTML'
            )
            
        elif step == 'destination':
            session['destination'] = text.upper()[:3]
            session['step'] = 'date'
            
            # Quick date options
            keyboard = [
                [InlineKeyboardButton("Today", callback_data='date_today')],
                [InlineKeyboardButton("Tomorrow", callback_data='date_tomorrow')],
                [InlineKeyboardButton("Next Week", callback_data='date_next_week')],
                [InlineKeyboardButton("Flexible Dates", callback_data='date_flexible')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ Route: <b>{session['origin']} → {session['destination']}</b>\n\n"
                "Select travel date or enter specific date (YYYY-MM-DD):",
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
        elif step == 'date':
            session['date'] = text
            
            # Run the search crew
            await update.message.reply_text(
                "🔍 <b>Searching flights...</b>\n"
                "AI agents are finding the best options for you.",
                parse_mode='HTML'
            )
            
            # Execute crew
            results = await self._execute_search_crew(
                session['origin'],
                session['destination'],
                session['date']
            )
            
            # Send results
            await self._send_flight_results(update, results)
            
            # Clear session
            del self.user_sessions[user_id]
    
    async def _handle_predict_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                   session: Dict, text: str):
        """Handle prediction flow"""
        user_id = str(update.effective_user.id)
        
        if session.get('step') == 'route':
            route = text.upper()
            
            await update.message.reply_text(
                "📊 <b>Running price prediction analysis...</b>\n"
                "This may take a moment.",
                parse_mode='HTML'
            )
            
            # Execute prediction crew
            predictions = await self._execute_prediction_crew(route)
            
            # Send formatted predictions
            await self._send_predictions(update, predictions)
            
            # Clear session
            del self.user_sessions[user_id]
    
    async def _execute_search_crew(self, origin: str, destination: str, date: str) -> Dict:
        """Execute search crew and return results"""
        search_agent = self.agents.search_specialist()
        analyst_agent = self.agents.price_analyst()
        notifier_agent = self.agents.notification_specialist()
        
        search_task = self.tasks.search_flights_task(search_agent, origin, destination, date)
        analysis_task = Task(
            description="Analyze the search results and identify best options",
            agent=analyst_agent,
            expected_output="Analysis of best flights"
        )
        notification_task = Task(
            description="Create a Telegram-formatted message with results",
            agent=notifier_agent,
            expected_output="Formatted message"
        )
        
        crew = Crew(
            agents=[search_agent, analyst_agent, notifier_agent],
            tasks=[search_task, analysis_task, notification_task],
            process=Process.sequential
        )
        
        result = crew.kickoff()
        return {"raw": result, "formatted": self._format_search_results(result)}
    
    async def _execute_prediction_crew(self, route: str) -> Dict:
        """Execute prediction crew"""
        analyst_agent = self.agents.price_analyst()
        
        predict_task = self.tasks.predict_prices_task(analyst_agent, route)
        
        crew = Crew(
            agents=[analyst_agent],
            tasks=[predict_task],
            process=Process.sequential
        )
        
        result = crew.kickoff()
        return {"raw": result, "formatted": self._format_predictions(result)}
    
    def _format_search_results(self, results: str) -> str:
        """Format search results for Telegram"""
        # This would parse the crew output and format nicely
        return f"""
✈️ <b>Flight Search Results</b>

🏆 <b>Best Options:</b>

1️⃣ <b>Cheapest:</b>
   AA 101 | $425
   08:00 → 16:30 (8h 30m)
   
2️⃣ <b>Fastest:</b>
   DL 205 | $520
   09:15 → 16:45 (7h 30m)
   
3️⃣ <b>Best Value:</b>
   UA 333 | $445
   10:00 → 17:45 (7h 45m)

💡 <b>AI Recommendation:</b>
Book the UA 333 flight - best balance of price and convenience.

<i>Prices may change. Book soon for best rates!</i>
        """
    
    def _format_predictions(self, predictions: str) -> str:
        """Format predictions for Telegram"""
        return f"""
📊 <b>Price Prediction Analysis</b>

📈 <b>Price Forecast:</b>
• 7 days: $450 (↑ 5%)
• 14 days: $425 (↓ 2%) 
• 30 days: $480 (↑ 10%)

📉 <b>Trend:</b> Rising
⚡ <b>Confidence:</b> 78%

💡 <b>AI Recommendation:</b>
Book within the next 3-5 days before prices increase.

🎯 <b>Best Booking Window:</b>
Tuesday-Wednesday next week

<i>Based on historical data and ML predictions</i>
        """
    
    async def _send_flight_results(self, update: Update, results: Dict):
        """Send formatted flight results with action buttons"""
        keyboard = [
            [InlineKeyboardButton("📍 Track This Route", callback_data='track_route')],
            [InlineKeyboardButton("🔔 Set Price Alert", callback_data='set_alert')],
            [InlineKeyboardButton("📊 View Predictions", callback_data='view_predict')],
            [InlineKeyboardButton("🔍 New Search", callback_data='search')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            results['formatted'],
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def _send_predictions(self, update: Update, predictions: Dict):
        """Send formatted predictions with actions"""
        keyboard = [
            [InlineKeyboardButton("🔔 Alert When Price Drops", callback_data='alert_drop')],
            [InlineKeyboardButton("📍 Track This Route", callback_data='track_route')],
            [InlineKeyboardButton("🔍 Search Flights Now", callback_data='search')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            predictions['formatted'],
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def send_alert(self, chat_id: str, message: str, 
                         buttons: List[Dict[str, str]] = None):
        """Send alert to user via Telegram"""
        # This would be called by the monitoring system
        keyboard = []
        if buttons:
            for btn in buttons:
                keyboard.append([InlineKeyboardButton(btn['text'], 
                                                     callback_data=btn['data'])])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        # Send via bot (would need bot instance)
        # await bot.send_message(chat_id, message, reply_markup=reply_markup, parse_mode='HTML')

def run_bot():
    """Run the Telegram bot"""
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    bot = FlightBot()
    
    # Command handlers
    application.add_handler(CommandHandler("start", bot.start))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(bot.handle_search, pattern='^search$'))
    application.add_handler(CallbackQueryHandler(bot.handle_track, pattern='^track$'))
    application.add_handler(CallbackQueryHandler(bot.handle_predict, pattern='^predict$'))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Start bot
    application.run_polling()