import json
import os

import pytest
import requests

BASE_URL = "http://localhost:5001"
STOCK_IDS = {}
STOCK_VALUES = {}
STOCK_DATA = []


# Load stock data from JSON file at the beginning
@pytest.fixture(scope="session", autouse=True)
def load_stock_data():
    global STOCK_DATA
    json_path = os.path.join(os.path.dirname(__file__), "stocks.json")
    with open(json_path, "r") as file:
        STOCK_DATA = json.load(file)


# Test 1
def test_posted_stocks():
    """Posts all initial stocks and stores their IDs globally."""
    global STOCK_IDS
    ids = set()
    for stock in STOCK_DATA[:3]:  # Posting only first 3 stocks
        response = requests.post(f"{BASE_URL}/stocks", json=stock)
        assert response.status_code == 201
        stock_id = response.json()["id"]
        assert stock_id not in ids  # Ensure the ID is unique
        ids.add(stock_id)
        STOCK_IDS[stock["symbol"]] = stock_id


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
    global STOCK_VALUES
    for symbol in ["NVDA", "AAPL", "GOOG"]:
        response = requests.get(f"{BASE_URL}/stock-value/{STOCK_IDS[symbol]}")
        STOCK_VALUES[symbol] = response.json()["stock_value"]
        assert response.status_code == 200
        assert response.json()["symbol"] == symbol


# Test 5
# Test GET /portfolio-value
def test_get_portfolio_value():
    response = requests.get(f"{BASE_URL}/portfolio-value")
    assert response.status_code == 200
    pv = response.json()["portfolio value"]
    stocks_value = sum(STOCK_VALUES[symbol] for symbol in ["NVDA", "AAPL", "GOOG"])
    assert pv * 0.97 <= stocks_value <= pv * 1.03


# Test 6
# Test POST /stocks with missing symbol
def test_post_invalid_stock():
    invalid_stock = STOCK_DATA[6]  # Stock missing "symbol"
    response = requests.post(f"{BASE_URL}/stocks", json=invalid_stock)
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
    invalid_stock_date = STOCK_DATA[7]  # Invalid purchase date format
    response = requests.post(f"{BASE_URL}/stocks", json=invalid_stock_date)
    assert response.status_code == 400