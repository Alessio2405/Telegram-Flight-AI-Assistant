\# ✈️ Advanced Telegram Flight AI Assistant



\*\*An 'intelligent' multi-agent system that monitors flight prices, predicts trends, and sends notifications via Telegram\*\*



---



\## 🌟 Overview



The Advanced Telegram Flight AI Assistant is a sophisticated autonomous system that uses AI agents to monitor flight prices, predict trends, and take intelligent actions on your behalf. Built with Crew.ai and integrated with Telegram, it provides a seamless conversational interface for all your flight tracking needs.



\### 🎯 Key Highlights



\- \*\*🤖 AI-Powered\*\*: Multiple specialized agents working together using Crew.ai

\- \*\*💬 Telegram Native\*\*: Full-featured Telegram bot with rich interactions

\- \*\*📊 ML Predictions\*\*: Advanced price forecasting using machine learning

\- \*\*🔄 Autonomous\*\*: 24/7 monitoring with intelligent decision-making

\- \*\*⚡ Real-time\*\*: Instant notifications for price drops and opportunities

\- \*\*🎨 User-Friendly\*\*: Intuitive conversational interface with inline buttons



\## 🚀 Features



\### AI Agent Capabilities



```mermaid

graph LR

&nbsp;   A\[User Request] --> B\[Search Specialist]

&nbsp;   B --> C\[Price Analyst]

&nbsp;   C --> D\[Booking Assistant]

&nbsp;   D --> E\[Notification Specialist]

&nbsp;   E --> F\[Telegram Message]

```



\### Telegram Bot Features



\- \*\*Interactive Menus\*\*: Rich inline keyboards for easy navigation

\- \*\*Multi-step Flows\*\*: Guided conversations for complex actions

\- \*\*Real-time Updates\*\*: Live notifications with action buttons

\- \*\*Group Support\*\*: Works in personal and group chats

\- \*\*Voice Alerts\*\*: Optional voice message notifications

\- \*\*Persistent Sessions\*\*: Remembers context across conversations



\## 📋 Prerequisites



\- Python 3.9 or higher

\- Telegram account and bot token

\- OpenAI API key (for Crew.ai agents)

\- At least one flight API key (Amadeus, RapidAPI, etc.)

\- PostgreSQL or SQLite database



\## 🔧 Installation



\### 1. Clone the Repository



```bash

git clone https://github.com/yourusername/telegram-flight-assistant.git

cd telegram-flight-assistant

```



\### 2. Set Up Virtual Environment



```bash

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate

```



\### 3. Install Dependencies



```bash

pip install -r requirements.txt

```



\### 4. Create Telegram Bot



1\. Open Telegram and search for `@BotFather`

2\. Send `/newbot` and follow the prompts

3\. Save the bot token provided

4\. Get your chat ID:

&nbsp;  - Message your new bot

&nbsp;  - Visit: `https://api.telegram.org/bot<YOUR\_TOKEN>/getUpdates`

&nbsp;  - Find your `chat\_id` in the response



\### 5. Configure Environment



```bash

cp .env.example .env

```



Edit `.env` with your credentials:



```env

\# Required

TELEGRAM\_BOT\_TOKEN=your\_bot\_token\_from\_botfather

TELEGRAM\_CHAT\_ID=your\_chat\_id

OPENAI\_API\_KEY=your\_openai\_api\_key



\# Flight APIs (at least one required)

AMADEUS\_API\_KEY=your\_amadeus\_key

AMADEUS\_API\_SECRET=your\_amadeus\_secret

\# OR

RAPIDAPI\_KEY=your\_rapidapi\_key



\# Optional

DATABASE\_URL=postgresql://user:pass@localhost/flightbot

ENABLE\_AUTO\_BOOKING=false

MAX\_AUTO\_BOOKING\_AMOUNT=1500

```



\### 6. Initialize Database



```bash

python -c "from database import Database; Database()"

```



\## 🎮 Usage



\### Starting the Bot



```bash

\# Run full system (bot + monitoring)

python main.py



\# Run bot only

python main.py --bot-only



\# Run monitoring only

python main.py --monitor-only

```



\### Telegram Commands



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



\### Example Interactions



\#### 🔍 Flight Search

```

You: /search

Bot: 🛫 Enter departure city:

You: Los Angeles

Bot: 🛬 Enter destination:

You: New York

Bot: 📅 Select travel date:

&nbsp;    \[Today] \[Tomorrow] \[Next Week] \[Custom]

You: \[Tomorrow]

Bot: 🔍 AI agents searching...



Bot: ✈️ BEST FLIGHTS FOUND:

&nbsp;    

&nbsp;    1️⃣ CHEAPEST: AA 101 - $399

&nbsp;       08:00 → 16:30 (5h 30m)

&nbsp;    

&nbsp;    2️⃣ FASTEST: DL 205 - $520

&nbsp;       09:15 → 16:45 (4h 30m)

&nbsp;    

&nbsp;    3️⃣ BEST VALUE: UA 333 - $445

&nbsp;       10:00 → 17:45 (4h 45m)

&nbsp;    

&nbsp;    💡 AI Recommendation: Book UA 333

&nbsp;    

&nbsp;    \[Track Route] \[Set Alert] \[Book Now]

```



\#### 📊 Price Predictions

```

You: /predict LAX-NYC

Bot: 📊 Analyzing price trends...



Bot: 🔮 PRICE FORECAST:

&nbsp;    

&nbsp;    Current Price: $425

&nbsp;    

&nbsp;    📈 Predictions:

&nbsp;    • 7 days: $480 (+12.9%) ⬆️

&nbsp;    • 14 days: $390 (-8.2%) ⬇️

&nbsp;    • 30 days: $510 (+20.0%) ⬆️

&nbsp;    

&nbsp;    🎯 AI RECOMMENDATION:

&nbsp;    Wait 10-14 days for best prices

&nbsp;    Set alert at $400

&nbsp;    

&nbsp;    📊 Confidence: 78%

&nbsp;    

&nbsp;    \[Set Alert at $400] \[Track Route]

```



\#### 🚨 Automatic Alerts

```

Bot: 🚨 PRICE DROP ALERT!

&nbsp;    

&nbsp;    Route: LAX → NYC

&nbsp;    Previous: $520

&nbsp;    Current: $385 💰

&nbsp;    

&nbsp;    SAVINGS: $135 (26% OFF!)

&nbsp;    

&nbsp;    ⚡ Only 3 seats remaining

&nbsp;    🔥 Price likely to increase soon

&nbsp;    

&nbsp;    \[Book Now] \[View Details] \[Snooze 24h]

```



\## 🏗️ Architecture



\### System Overview



```

┌──────────────────────────────────────────────────────┐

│                   User Interface                     │

│                  (Telegram Bot)                      │

└────────────────────┬─────────────────────────────────┘

&nbsp;                    │

┌────────────────────▼─────────────────────────────────┐

│                Orchestration Layer                   │

│               (Crew.ai Coordinator)                  │

└────────────────────┬─────────────────────────────────┘

&nbsp;                    │

&nbsp;    ┌───────────────┼───────────────┐

&nbsp;    │               │               │

┌────▼────┐    ┌────▼────┐    ┌────▼────┐

│ Search  │    │ Price   │    │ Booking │

│ Agent   │    │ Analyst │    │ Agent   │

└─────────┘    └─────────┘    └─────────┘

&nbsp;    │               │               │

&nbsp;    └───────────────┼───────────────┘

&nbsp;                    │

┌────────────────────▼─────────────────────────────────┐

│                  Data Layer                          │

│         (Database, APIs, Cache)                      │

└──────────────────────────────────────────────────────┘

```



\### Agent Roles



| Agent | Role | Responsibilities |

|-------|------|------------------|

| \*\*Search Specialist\*\* | Find best flights | Query multiple APIs, compare options, identify deals |

| \*\*Price Analyst\*\* | Analyze and predict | ML predictions, trend analysis, timing recommendations |

| \*\*Booking Assistant\*\* | Manage bookings | Handle reservations, seat selection, payment processing |

| \*\*Notification Specialist\*\* | Communicate with users | Format messages, create alerts, manage Telegram interactions |



\### Database Schema



```sql

-- Users table

users (

&nbsp;   telegram\_id PRIMARY KEY,

&nbsp;   username,

&nbsp;   preferences JSON,

&nbsp;   created\_at,

&nbsp;   last\_active

)



-- Tracked routes

tracked\_routes (

&nbsp;   id PRIMARY KEY,

&nbsp;   user\_id REFERENCES users,

&nbsp;   origin,

&nbsp;   destination,

&nbsp;   max\_price,

&nbsp;   active,

&nbsp;   best\_price,

&nbsp;   price\_history JSON

)



-- Action logs

action\_logs (

&nbsp;   id PRIMARY KEY,

&nbsp;   user\_id,

&nbsp;   action\_type,

&nbsp;   parameters JSON,

&nbsp;   result JSON,

&nbsp;   timestamp

)

```



\## 🔬 Advanced Features



\### Machine Learning Price Predictions



The system uses multiple ML models for price forecasting:



\- \*\*Linear Regression\*\*: Basic trend analysis

\- \*\*LSTM Networks\*\*: Time series prediction

\- \*\*Random Forest\*\*: Pattern recognition

\- \*\*Ensemble Methods\*\*: Combined predictions for accuracy



\### Intelligent Monitoring



\- \*\*Adaptive Checking\*\*: Frequency adjusts based on volatility

\- \*\*Pattern Recognition\*\*: Identifies booking patterns

\- \*\*Event Correlation\*\*: Considers holidays, events, seasons

\- \*\*Competition Analysis\*\*: Monitors airline pricing strategies



\### Auto-Booking Rules



Configure automatic purchasing with rules:



```python

rules = {

&nbsp;   "max\_price": 500,

&nbsp;   "preferred\_times": \["morning", "evening"],

&nbsp;   "min\_savings": 100,

&nbsp;   "airlines": \["AA", "UA", "DL"],

&nbsp;   "class": "economy",

&nbsp;   "auto\_confirm": False

}

```



\## 📊 Performance



\- \*\*Response Time\*\*: < 2 seconds for searches

\- \*\*Monitoring Frequency\*\*: Configurable (default: 30 min)

\- \*\*Concurrent Users\*\*: Supports 1000+ active users

\- \*\*API Calls\*\*: Optimized with caching and batching

\- \*\*Database\*\*: Indexed for fast queries



\## 🔒 Security



\- \*\*API Keys\*\*: Stored securely in environment variables

\- \*\*User Data\*\*: Encrypted in database

\- \*\*Payment Info\*\*: Never stored (uses Stripe tokenization)

\- \*\*Rate Limiting\*\*: Prevents abuse and API overuse

\- \*\*Input Validation\*\*: Sanitizes all user inputs



\## 🧪 Testing



```bash

\# Run all tests

pytest



\# Run specific test suite

pytest tests/test\_agents.py



\# Run with coverage

pytest --cov=. --cov-report=html



\# Test Telegram bot

python -m pytest tests/test\_telegram.py -v

```



\### Development Setup



```bash

\# Install development dependencies

pip install -r requirements-dev.txt



\# Run linter

flake8 .



\# Run formatter

black .



\# Run type checker

mypy .

```



\## 📈 Roadmap



\- \[ ] Multi-language support

\- \[ ] Voice command integration

\- \[ ] Hotel and car rental tracking

\- \[ ] API marketplace integration



\## 🐛 Troubleshooting



\### Common Issues



| Issue | Solution |

|-------|----------|

| Bot not responding | Check `TELEGRAM\_BOT\_TOKEN` is correct |

| No flight results | Verify flight API credentials |

| Database errors | Run database initialization script |

| Prediction failures | Ensure sufficient historical data |

| High API costs | Adjust `CHECK\_INTERVAL` and enable caching |



\### Debug Mode



```bash

\# Enable debug logging

export LOG\_LEVEL=DEBUG

python main.py

```



\## 📄 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



\## 🙏 Acknowledgments



\- \[Crew.ai](https://crewai.io/) for the amazing agent framework

\- \[python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration

\- \[Amadeus](https://developers.amadeus.com/) for flight data API



