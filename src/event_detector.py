"""
event_detector.py
=================
Detects, classifies and scores financial events from news text.
  - FinBERT sentiment scoring
  - spaCy Named Entity Recognition (NER)
  - Event type classification (earnings, macro, geopolitical, etc.)

Usage:
    from src.event_detector import EventDetector
    detector = EventDetector()
    df = detector.score_headlines(news_df)
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Event taxonomy
EVENT_TYPES = {
    "earnings": ["earnings", "EPS", "revenue", "beat", "miss", "guidance", "profit", "loss"],
    "macro": ["Fed", "Federal Reserve", "interest rate", "CPI", "inflation", "GDP", "unemployment", "FOMC"],
    "geopolitical": ["war", "conflict", "sanctions", "trade war", "tariff", "election", "coup"],
    "credit": ["default", "downgrade", "upgrade", "rating", "Moody", "S&P", "Fitch"],
    "regulatory": ["SEC", "regulation", "fine", "lawsuit", "antitrust", "ban"],
    "corporate": ["merger", "acquisition", "M&A", "IPO", "spinoff", "buyback", "dividend"],
}


class EventDetector:
    """
    Classifies and scores financial news events using FinBERT.

    Can be instantiated directly with keyword arguments, or via a project
    config dict (config['nlp'] section) using EventDetector.from_config(config).

    Parameters
    ----------
    model_name : str
        HuggingFace model identifier (default: ProsusAI/finbert)
    batch_size : int
        Batch size for inference
    threshold : float
        Minimum confidence to assign a sentiment label
    """

    def __init__(
        self,
        model_name: str = "ProsusAI/finbert",
        batch_size: int = 32,
        threshold: float = 0.7,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.threshold = threshold
        self._pipeline = None

    @classmethod
    def from_config(cls, config: dict) -> "EventDetector":
        """
        Instantiate from project config.yaml (reads config['nlp'] section).

        Usage:
            detector = EventDetector.from_config(config)
        """
        nlp_cfg = config.get("nlp", {})
        return cls(
            model_name=nlp_cfg.get("model", "ProsusAI/finbert"),
            batch_size=nlp_cfg.get("batch_size", 32),
            threshold=nlp_cfg.get("sentiment_threshold", 0.7),
        )

    def _load_pipeline(self):
        """Lazy-load FinBERT pipeline (avoids slow import at module load)."""
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "text-classification",
                    model=self.model_name,
                    tokenizer=self.model_name,
                    top_k=None,
                )
                logger.info(f"Loaded FinBERT: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to load FinBERT: {e}")
                raise

    def score_headlines(self, df: pd.DataFrame, text_col: str = "title") -> pd.DataFrame:
        """
        Run FinBERT sentiment over a DataFrame of headlines.

        Parameters
        ----------
        df : pd.DataFrame
            Must contain text_col (headlines) and 'published_at' column
        text_col : str
            Column containing the text to score

        Returns
        -------
        pd.DataFrame
            Input df with added columns:
              sentiment_label, sentiment_score, event_type, event_score
        """
        self._load_pipeline()
        texts = df[text_col].fillna("").tolist()

        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_results = self._pipeline(batch, truncation=True, max_length=512)
            results.extend(batch_results)

        labels, scores = [], []
        for result in results:
            top = max(result, key=lambda x: x["score"])
            if top["score"] >= self.threshold:
                labels.append(top["label"].lower())
                scores.append(top["score"])
            else:
                labels.append("neutral")
                scores.append(top["score"])

        df = df.copy()
        df["sentiment_label"] = labels
        df["sentiment_score"] = scores

        # Numeric sentiment: positive=+1, negative=-1, neutral=0
        sentiment_map = {"positive": 1, "negative": -1, "neutral": 0}
        df["sentiment_numeric"] = df["sentiment_label"].map(sentiment_map)

        # Event type classification (rule-based on keywords)
        df["event_type"] = df[text_col].apply(self._classify_event_type)

        return df

    def _classify_event_type(self, text: str) -> str:
        """Classify event type based on keyword matching."""
        if not isinstance(text, str):
            return "other"
        text_lower = text.lower()
        for event_type, keywords in EVENT_TYPES.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return event_type
        return "other"

    def aggregate_daily_sentiment(
        self, df: pd.DataFrame, date_col: str = "published_at"
    ) -> pd.DataFrame:
        """
        Aggregate headline-level sentiment to daily scores per event type.

        Returns
        -------
        pd.DataFrame
            Daily sentiment with columns: date, event_type, mean_sentiment,
            article_count, net_sentiment
        """
        df = df.copy()
        df["date"] = pd.to_datetime(df[date_col]).dt.date

        daily = (
            df.groupby(["date", "event_type"])
            .agg(
                mean_sentiment=("sentiment_numeric", "mean"),
                article_count=("sentiment_numeric", "count"),
                net_sentiment=("sentiment_numeric", "sum"),
            )
            .reset_index()
        )
        daily["date"] = pd.to_datetime(daily["date"])
        return daily
