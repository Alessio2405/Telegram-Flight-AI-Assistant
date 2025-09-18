from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from config import config

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    telegram_id = Column(String, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_searches = Column(Integer, default=0)
    total_bookings = Column(Integer, default=0)

class ActionLog(Base):
    __tablename__ = "action_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    action_type = Column(String)
    parameters = Column(JSON)
    result = Column(JSON)
    success = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FlightSearch(Base):
    __tablename__ = "flight_searches"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    departure_date = Column(DateTime)
    lowest_price = Column(Float)
    results = Column(JSON)
    searched_at = Column(DateTime, default=datetime.utcnow)

class TrackedRoute(Base):
    __tablename__ = "tracked_routes"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    max_price = Column(Float, nullable=True)
    check_frequency = Column(Integer, default=30)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_check = Column(DateTime, nullable=True)
    best_price = Column(Float, nullable=True)
    price_history = Column(JSON, default=list)

class ExpenseRecord(Base):
    __tablename__ = "expense_records"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    category = Column(String)
    description = Column(String)
    flight_reference = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_or_create_user(self, telegram_id: str, username: str = None, 
                           first_name: str = None):
        session = self.Session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    preferences={}
                )
                session.add(user)
            else:
                user.last_active = datetime.utcnow()
            session.commit()
            return user
        finally:
            session.close()
    
    def log_action(self, user_id: str, action_type: str, 
                   parameters: Dict, result: Dict = None, success: bool = True):
        session = self.Session()
        try:
            log = ActionLog(
                user_id=user_id,
                action_type=action_type,
                parameters=parameters,
                result=result,
                success=success
            )
            session.add(log)
            session.commit()
        finally:
            session.close()
    
    def add_tracked_route(self, user_id: str, origin: str, destination: str, 
                         max_price: float = None) -> str:
        session = self.Session()
        try:
            route_id = f"{user_id}_{origin}_{destination}_{datetime.now().timestamp()}"
            route = TrackedRoute(
                id=route_id,
                user_id=user_id,
                origin=origin,
                destination=destination,
                max_price=max_price
            )
            session.add(route)
            session.commit()
            return route_id
        finally:
            session.close()
    
    def get_active_routes(self, user_id: str = None) -> List[Dict]:
        session = self.Session()
        try:
            query = session.query(TrackedRoute).filter_by(active=True)
            if user_id:
                query = query.filter_by(user_id=user_id)
            return [r.__dict__ for r in query.all()]
        finally:
            session.close()