# ✈️ Advanced Telegram Flight AI Assistant

**An 'intelligent' multi-agent system that monitors flight prices, predicts trends, and sends notifications via Telegram**

---

## 🌟 Overview

The Advanced Telegram Flight AI Assistant is a sophisticated autonomous system that uses AI agents to monitor flight prices, predict trends, and take intelligent actions on your behalf. Built with Crew.ai and integrated with Telegram, it provides a seamless conversational interface for all your flight tracking needs.

### 🎯 Key Highlights

- **🤖 AI-Powered**: Multiple specialized agents working together using Crew.ai
- **💬 Telegram Native**: Full-featured Telegram bot with rich interactions
- **📊 ML Predictions**: Advanced price forecasting using machine learning
- **🔄 Autonomous**: 24/7 monitoring with intelligent decision-making
- **⚡ Real-time**: Instant notifications for price drops and opportunities
- **🎨 User-Friendly**: Intuitive conversational interface with inline buttons

## 🚀 Features

### AI Agent Capabilities

```mermaid
graph LR
    A[User Request] --> B[Search Specialist]
    B --> C[Price Analyst]
    C --> D[Booking Assistant]
    D --> E[Notification Specialist]
    E --> F[Telegram Message]
```

### Telegram Bot Features

- **Interactive Menus**: Rich inline keyboards for easy navigation
- **Multi-step Flows**: Guided conversations for complex actions
- **Real-time Updates**: Live notifications with action buttons
- **Group Support**: Works in personal and group chats
- **Voice Alerts**: Optional voice message notifications
- **Persistent Sessions**: Remembers context across conversations

## 📋 Prerequisites

- Python 3.9 or higher
- Telegram account and bot token
- OpenAI API key (for Crew.ai agents)
- At least one flight API key (Amadeus, RapidAPI, etc.)
- PostgreSQL or SQLite database

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-flight-assistant.git
cd telegram-flight-assistant
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Save the bot token provided
4. Get your chat ID:
   - Message your new bot
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your `chat_id` in the response

### 5. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id
OPENAI_API_KEY=your_openai_api_key

# Flight APIs (at least one required)
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
# OR
RAPIDAPI_KEY=your_rapidapi_key

# Optional
DATABASE_URL=postgresql://user:pass@localhost/flightbot
ENABLE_AUTO_BOOKING=false
MAX_AUTO_BOOKING_AMOUNT=1500
```

### 6. Initialize Database

```bash
python -c "from database import Database; Database()"
```

## 🎮 Usage

### Starting the Bot

```bash
# Run full system (bot + monitoring)
python main.py

# Run bot only
python main.py --bot-only

# Run monitoring only
python main.py --monitor-only
```

### Telegram Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and show menu | `/start` |
| `/search` | Search for flights | `/search` → Interactive flow |
| `/track` | Track a route for changes | `/track LAX-NYC` |
| `/predict` | Get price predictions | `/predict LAX-NYC` |
| `/alerts` | Manage price alerts | `/alerts` |
| `/expenses` | Track travel expenses | `/expenses` |
| `/report` | Generate analytics report | `/report monthly` |
| `/help` | Show help information | `/help` |

### Example Interactions

#### 🔍 Flight Search

```
You: /search
Bot: 🛫 Enter departure city:
You: Los Angeles
Bot: 🛬 Enter destination:
You: New York
Bot: 📅 Select travel date:
     [Today] [Tomorrow] [Next Week] [Custom]
You: [Tomorrow]
Bot: 🔍 AI agents searching...

Bot: ✈️ BEST FLIGHTS FOUND:
     
     1️⃣ CHEAPEST: AA 101 - $399
        08:00 → 16:30 (5h 30m)
     
     2️⃣ FASTEST: DL 205 - $520
        09:15 → 16:45 (4h 30m)
     
     3️⃣ BEST VALUE: UA 333 - $445
        10:00 → 17:45 (4h 45m)
     
     💡 AI Recommendation: Book UA 333
     
     [Track Route] [Set Alert] [Book Now]
```

#### 📊 Price Predictions

```
You: /predict LAX-NYC
Bot: 📊 Analyzing price trends...

Bot: 🔮 PRICE FORECAST:
     
     Current Price: $425
     
     📈 Predictions:
     • 7 days: $480 (+12.9%) ⬆️
     • 14 days: $390 (-8.2%) ⬇️
     • 30 days: $510 (+20.0%) ⬆️
     
     🎯 AI RECOMMENDATION:
     Wait 10-14 days for best prices
     Set alert at $400
     
     📊 Confidence: 78%
     
     [Set Alert at $400] [Track Route]
```

#### 🚨 Automatic Alerts

```
Bot: 🚨 PRICE DROP ALERT!
     
     Route: LAX → NYC
     Previous: $520
     Current: $385 💰
     
     SAVINGS: $135 (26% OFF!)
     
     ⚡ Only 3 seats remaining
     🔥 Price likely to increase soon
     
     [Book Now] [View Details] [Snooze 24h]
```

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────┐
│                   User Interface                     │
│                  (Telegram Bot)                      │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│                Orchestration Layer                   │
│               (Crew.ai Coordinator)                  │
└────────────────────┬─────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼────┐    ┌────▼────┐    ┌────▼────┐
│ Search  │    │ Price   │    │ Booking │
│ Agent   │    │ Analyst │    │ Agent   │
└─────────┘    └─────────┘    └─────────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│                  Data Layer                          │
│         (Database, APIs, Cache)                      │
└──────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Search Specialist** | Find best flights | Query multiple APIs, compare options, identify deals |
| **Price Analyst** | Analyze and predict | ML predictions, trend analysis, timing recommendations |
| **Booking Assistant** | Manage bookings | Handle reservations, seat selection, payment processing |
| **Notification Specialist** | Communicate with users | Format messages, create alerts, manage Telegram interactions |

### Database Schema

```sql
-- Users table
users (
    telegram_id PRIMARY KEY,
    username,
    preferences JSON,
    created_at,
    last_active
)

-- Tracked routes
tracked_routes (
    id PRIMARY KEY,
    user_id REFERENCES users,
    origin,
    destination,
    max_price,
    active,
    best_price,
    price_history JSON
)

-- Action logs
action_logs (
    id PRIMARY KEY,
    user_id,
    action_type,
    parameters JSON,
    result JSON,
    timestamp
)
```

## 🔬 Advanced Features

### Machine Learning Price Predictions

The system uses multiple ML models for price forecasting:

- **Linear Regression**: Basic trend analysis
- **LSTM Networks**: Time series prediction
- **Random Forest**: Pattern recognition
- **Ensemble Methods**: Combined predictions for accuracy

### Intelligent Monitoring

- **Adaptive Checking**: Frequency adjusts based on volatility
- **Pattern Recognition**: Identifies booking patterns
- **Event Correlation**: Considers holidays, events, seasons
- **Competition Analysis**: Monitors airline pricing strategies

### Auto-Booking Rules

Configure automatic purchasing with rules:

```python
rules = {
    "max_price": 500,
    "preferred_times": ["morning", "evening"],
    "min_savings": 100,
    "airlines": ["AA", "UA", "DL"],
    "class": "economy",
    "auto_confirm": False
}
```

## 📊 Performance

- **Response Time**: < 2 seconds for searches
- **Monitoring Frequency**: Configurable (default: 30 min)
- **Concurrent Users**: Supports 1000+ active users
- **API Calls**: Optimized with caching and batching
- **Database**: Indexed for fast queries

## 🔒 Security

- **API Keys**: Stored securely in environment variables
- **User Data**: Encrypted in database
- **Payment Info**: Never stored (uses Stripe tokenization)
- **Rate Limiting**: Prevents abuse and API overuse
- **Input Validation**: Sanitizes all user inputs

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_agents.py

# Run with coverage
pytest --cov=. --cov-report=html

# Test Telegram bot
python -m pytest tests/test_telegram.py -v
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linter
flake8 .

# Run formatter
black .

# Run type checker
mypy .
```

## 📈 Roadmap

- [ ] Multi-language support
- [ ] Voice command integration
- [ ] Hotel and car rental tracking
- [ ] API marketplace integration

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Bot not responding | Check `TELEGRAM_BOT_TOKEN` is correct |
| No flight results | Verify flight API credentials |
| Database errors | Run database initialization script |
| Prediction failures | Ensure sufficient historical data |
| High API costs | Adjust `CHECK_INTERVAL` and enable caching |

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Crew.ai](https://crewai.io/) for the amazing agent framework
- [python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration
- [Amadeus](https://developers.amadeus.com/) for flight data API
