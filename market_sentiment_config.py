"""
Configuration module for Market Sentiment Analysis System
Centralized configuration with environment variable support
"""
import os
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

@dataclass
class SentimentConfig:
    """Centralized configuration for sentiment analysis"""
    
    # Data collection sources
    TWITTER_HANDLES: List[str] = None
    INSTAGRAM_TAGS: List[str] = None
    NEWS_KEYWORDS: List[str] = None
    
    # API configurations (would be loaded from environment variables)
    TWITTER_BEARER_TOKEN: str = None
    INSTAGRAM_ACCESS_TOKEN: str = None
    NEWS_API_KEY: str = None
    
    # Processing parameters
    SENTIMENT_THRESHOLD: float = 0.3
    MIN_CONFIDENCE: float = 0.7
    BATCH_SIZE: int = 100
    UPDATE_INTERVAL_MINUTES: int = 15
    
    # Firebase configuration
    FIREBASE_CREDENTIALS_PATH: str = "firebase_credentials.json"
    FIRESTORE_COLLECTION: str = "market_sentiment"
    
    def __post_init__(self):
        """Initialize with environment variables"""
        self.TWITTER_HANDLES = os.getenv("TWITTER_HANDLES", "elonmusk,cz_binance").split(",")
        self.INSTAGRAM_TAGS = os.getenv("INSTAGRAM_TAGS", "bitcoin,crypto").split(",")
        self.NEWS_KEYWORDS = os.getenv("NEWS_KEYWORDS", "BTC,ETH,stock market").split(",")
        
        # Load API tokens from environment
        self.TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
        self.INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
        
        # Validate critical configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration and log warnings for missing critical data"""
        missing_tokens = []
        if not self.TWITTER_BEARER_TOKEN:
            missing_tokens.append("Twitter")
        if not self.INSTAGRAM_ACCESS_TOKEN:
            missing_tokens.append("Instagram")
        if not self.NEWS_API_KEY:
            missing_tokens.append("NewsAPI")
        
        if missing_tokens:
            logging.warning(f"Missing API tokens for: {', '.join(missing_tokens)}. "
                          f"Corresponding data sources will be