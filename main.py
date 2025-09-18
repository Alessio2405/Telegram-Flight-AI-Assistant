"""
Advanced Telegram Flight Bot with AI Agents

This system uses Crew.ai agents to intelligently monitor flights,
predict prices, and send notifications via Telegram.
"""

import asyncio
import threading
import argparse
from telegram_bot import run_bot
from monitoring import FlightMonitor
from config import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_monitor_thread():
    """Run monitoring in separate thread"""
    monitor = FlightMonitor()
    monitor.start_monitoring()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Advanced Telegram Flight Bot with AI Agents"
    )
    
    parser.add_argument(
        "--bot-only",
        action="store_true",
        help="Run only the Telegram bot without monitoring"
    )
    
    parser.add_argument(
        "--monitor-only", 
        action="store_true",
        help="Run only the monitoring system"
    )
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║  
    ║       ✈️  TELEGRAM FLIGHT AI ASSISTANT v2.0 ✈️            ║
    ║                                                          ║
    ║         Powered by Crew.ai Intelligent Agents           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not configured!")
        return
    
    if args.monitor_only:
        logger.info("Starting monitoring system only...")
        monitor = FlightMonitor()
        monitor.start_monitoring()
        
    elif args.bot_only:
        logger.info("Starting Telegram bot only...")
        run_bot()
        
    else:
        logger.info("Starting full system (bot + monitoring)...")
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=run_monitor_thread, daemon=True)
        monitor_thread.start()
        
        # Run bot in main thread
        run_bot()

if __name__ == "__main__":
    main()
