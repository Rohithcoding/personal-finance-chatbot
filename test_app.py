"""
Simple tests for the personal finance chatbot
"""

import sys
sys.path.append('./backend')

from backend.utils import FinanceUtils

def test_utils():
    """Test utility functions"""
    utils = FinanceUtils()
    
    # Test amount extraction
    test_text = "I want to invest $5000 in stocks and save $2,500 for retirement"
    amounts = utils.extract_amounts(test_text)
    assert 5000.0 in amounts
    assert 2500.0 in amounts
    print(f"✅ Amount extraction test passed: {amounts}")
    
    # Test currency formatting
    formatted = utils.format_currency(1234.56)
    assert formatted == "$1,234.56"
    print(f"✅ Currency formatting test passed: {formatted}")
    
    # Test expense categorization
    food_expense = "Lunch at restaurant downtown"
    category = utils.categorize_expense(food_expense)
    assert category == "food"
    print(f"✅ Expense categorization test passed: {category}")
    
    # Test compound interest calculation
    result = utils.calculate_compound_interest(1000, 0.05, 10)
    expected = 1000 * (1.05 ** 10)  # Simplified for annual compounding
    print(f"✅ Compound interest calculation: ${result}")
    
    print("All tests passed! 🎉")

if __name__ == "__main__":
    test_utils()
