"""
Utility helper functions
"""
import re
from urllib.parse import urlparse
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_url_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def deduplicate_list(items: list) -> list:
    """
    Remove duplicates from list while preserving order
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def calculate_confidence(score: float, threshold: float = 0.7) -> str:
    """
    Convert similarity score to confidence level
    """
    if score >= threshold + 0.2:
        return "high"
    elif score >= threshold:
        return "medium"
    else:
        return "low"
