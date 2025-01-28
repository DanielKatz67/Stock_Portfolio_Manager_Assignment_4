import pytest
import requests

BASE_URL = "http://localhost:5001"
STOCK_IDS = {}

# Sample stock data
stock1 = {"name": "NVIDIA Corporation", "symbol": "NVDA", "purchase price": 134.66, "purchase date": "18-06-2024", "shares": 7}
stock2 = {"name": "Apple Inc.", "symbol": "AAPL", "purchase price": 183.63, "purchase date": "22-02-2024", "shares": 19}
stock3 = {"name": "Alphabet Inc.", "symbol": "GOOG", "purchase price": 140.12, "purchase date": "24-10-2024", "shares": 14}
stock4 = {"name": "Tesla, Inc.", "symbol": "TSLA", "purchase price": 194.58, "purchase date": "28-11-2022", "shares": 32}
stock5 = {"name": "Microsoft Corporation", "symbol": "MSFT", "purchase price": 420.55, "purchase date": "09-02-2024", "shares": 35}
stock6 = {"name": "Intel Corporation", "symbol": "INTC", "purchase price": 19.15, "purchase date": "13-01-2025", "shares": 10}
stock7 = {"name": "Amazon.com, Inc.", "purchase price": 134.66, "purchase date": "18-06-2024", "shares": 7}
stock8 = {"name": "Amazon.com, Inc.", "symbol": "AMZN", "purchase price": 134.66, "purchase date": "Tuesday, June 18, 2024", "shares": 7}


# Test 1
# Runs once per module and automatically executes before tests
@pytest.fixture(scope="module", autouse=True)
def posted_stocks():
    """Posts all initial stocks and stores their IDs globally."""
    global STOCK_IDS
    for stock in [stock1, stock2, stock3]:
        response = requests.post(f"{BASE_URL}/stocks", json=stock)
        assert response.status_code == 201
        STOCK_IDS[stock["symbol"]] = response.json()["id"]


# Test 2
# Test GET /stocks/{ID}
def test_get_stock():
    response = requests.get(f"{BASE_URL}/stocks/{STOCK_IDS['NVDA']}")
    assert response.status_code == 200
    assert response.json()["symbol"] == "NVDA"


# Test 3
# Test GET /stocks
def test_get_stocks():
    response = requests.get(f"{BASE_URL}/stocks")
    assert response.status_code == 200
    assert len(response.json()) == 3


# Test 4
# Test GET /stock-value/{ID}
def test_get_stock_value():
    for symbol in ["NVDA", "AAPL", "GOOG"]:
        response = requests.get(f"{BASE_URL}/stock-value/{STOCK_IDS[symbol]}")
        assert response.status_code == 200
        assert response.json()["symbol"] == symbol


# # Test 5
# # Test GET /portfolio-value
# def test_get_portfolio_value():
#     response = requests.get(f"{BASE_URL}/portfolio-value")
#     assert response.status_code == 200
#     pv = response.json()["portfolio value"]
#     print("Portfolio Value:", pv)
#     stock1_value = stock1["purchase price"] * stock1["shares"]
#     stock2_value = stock2["purchase price"] * stock2["shares"]
#     stock3_value = stock3["purchase price"] * stock3["shares"]
#     stocks_value = stock1_value + stock2_value + stock3_value
#     print(f"stocks_value {stocks_value}= Stock1 value: {stock1_value}, Stock2 value: {stock2_value}, Stock3 value: {stock3_value}")
#     assert pv * 0.97 <= stocks_value <= pv * 1.03


# Test 6
# Test POST /stocks with missing symbol
def test_post_invalid_stock():
    response = requests.post(f"{BASE_URL}/stocks", json=stock7)
    assert response.status_code == 400


# Test 7
# Test DELETE /stocks/{ID}
def test_delete_stock():
    response = requests.delete(f"{BASE_URL}/stocks/{STOCK_IDS['AAPL']}")
    assert response.status_code == 204


# Test 8
# Test GET /stocks/{ID} after deletion
def test_get_deleted_stock():
    response = requests.get(f"{BASE_URL}/stocks/{STOCK_IDS['AAPL']}")
    assert response.status_code == 404


# Test 9
# Test POST /stocks with invalid purchase date
def test_post_invalid_stock_date():
    response = requests.post(f"{BASE_URL}/stocks", json=stock8)
    assert response.status_code == 400