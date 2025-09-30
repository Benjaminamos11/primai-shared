"""
Utility functions shared between API and Workers
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))


def validate_swiss_phone(phone: str) -> bool:
    """
    Validate Swiss phone number
    Accepts: +41 XX XXX XX XX, 0XX XXX XX XX, etc.
    """
    clean_phone = re.sub(r'\s+', '', phone)
    swiss_phone_regex = r'^(\+41|0041|0)[1-9]\d{8}$'
    return bool(re.match(swiss_phone_regex, clean_phone))


def validate_swiss_postal_code(postal_code: str) -> bool:
    """Validate Swiss postal code (4 digits, starts with 1-9)"""
    postal_code_regex = r'^[1-9]\d{3}$'
    return bool(re.match(postal_code_regex, postal_code))


def format_currency_chf(amount: float) -> str:
    """Format amount as Swiss Francs"""
    return f"CHF {amount:,.2f}"


def format_swiss_phone(phone: str) -> str:
    """
    Format Swiss phone number
    Returns: +41 XX XXX XX XX or 0XX XXX XX XX
    """
    clean_phone = re.sub(r'\s+', '', phone)
    
    # Format as +41 XX XXX XX XX
    if clean_phone.startswith('+41'):
        number = clean_phone[3:]
        return f"+41 {number[:2]} {number[2:5]} {number[5:7]} {number[7:]}"
    
    # Format as 0XX XXX XX XX
    if clean_phone.startswith('0'):
        return f"{clean_phone[:3]} {clean_phone[3:6]} {clean_phone[6:8]} {clean_phone[8:]}"
    
    return phone


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def calculate_savings_percentage(old_premium: float, new_premium: float) -> float:
    """Calculate savings percentage"""
    if old_premium == 0:
        return 0.0
    savings = ((old_premium - new_premium) / old_premium) * 100
    return round(savings, 2)
