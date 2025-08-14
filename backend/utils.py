"""
Utility functions for personal finance chatbot
"""

import re
from typing import Dict, List, Optional
from datetime import datetime

class FinanceUtils:
    """Utility functions for financial calculations and text processing"""
    
    @staticmethod
    def extract_amounts(text: str) -> List[float]:
        """Extract monetary amounts from text"""
        # Pattern to match currency amounts
        pattern = r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
        matches = re.findall(pattern, text)
        
        amounts = []
        for match in matches:
            try:
                # Remove commas and convert to float
                amount = float(match.replace(',', ''))
                amounts.append(amount)
            except ValueError:
                continue
        
        return amounts
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def calculate_compound_interest(principal: float, rate: float, time: float, 
                                  compound_frequency: int = 12) -> float:
        """Calculate compound interest"""
        amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
        return round(amount, 2)
    
    @staticmethod
    def calculate_monthly_payment(loan_amount: float, annual_rate: float, years: int) -> float:
        """Calculate monthly loan payment using standard formula"""
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                 ((1 + monthly_rate) ** num_payments - 1)
        
        return round(payment, 2)
    
    @staticmethod
    def categorize_expense(text: str) -> str:
        """Categorize expense based on keywords in text"""
        text_lower = text.lower()
        
        categories = {
            'food': ['restaurant', 'grocery', 'food', 'dining', 'coffee', 'lunch', 'dinner'],
            'transportation': ['gas', 'uber', 'taxi', 'bus', 'train', 'parking', 'car'],
            'entertainment': ['movie', 'concert', 'game', 'entertainment', 'streaming'],
            'shopping': ['amazon', 'store', 'mall', 'shopping', 'clothes', 'electronics'],
            'utilities': ['electric', 'water', 'internet', 'phone', 'utility'],
            'healthcare': ['doctor', 'hospital', 'pharmacy', 'medical', 'dentist']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'other'
    
    @staticmethod
    def validate_financial_input(text: str) -> Dict[str, bool]:
        """Validate if text contains financial information"""
        return {
            'has_amount': bool(re.search(r'\$?\d+(?:,\d{3})*(?:\.\d{2})?', text)),
            'has_percentage': bool(re.search(r'\d+(?:\.\d+)?%', text)),
            'has_date': bool(re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)),
        }

# Standalone functions for easier importing
def extract_amounts(text: str) -> List[float]:
    """Extract monetary amounts from text"""
    return FinanceUtils.extract_amounts(text)

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return FinanceUtils.format_currency(amount)

def calculate_compound_interest(principal: float, rate: float, time: float, 
                              compound_frequency: int = 12) -> float:
    """Calculate compound interest"""
    return FinanceUtils.calculate_compound_interest(principal, rate, time, compound_frequency)

def categorize_expense(text: str) -> str:
    """Categorize expense based on keywords in text"""
    return FinanceUtils.categorize_expense(text)

def validate_financial_input(text: str) -> Dict[str, bool]:
    """Validate if text contains financial information"""
    return FinanceUtils.validate_financial_input(text)
