import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_add_college():
    data = {
        "name": "Test College Assam2",
        "city": "Test City",
        "state": "Assam",
        "type": "Private",
        "mode": "Full Time",
        "courses": "Diploma, Certificate"
    }
    response = requests.post(f"{BASE_URL}/add_college", json=data)
    print("Add College Response:", response.status_code, response.json())
    print("-"*50)

def test_add_duplicate_college():
    data = {
        "name": "Test College",
        "city": "Another City",
        "state": "Another State",
        "type": "Public",
        "mode": "Part Time",
        "courses": "Science, Arts"
    }
    response = requests.post(f"{BASE_URL}/add_college", json=data)
    print("Duplicate College Response:", response.status_code, response.json())
    print("-"*50)

def test_update_college():
    data = {
        "name": "Test College",
        "city": "Updated City",
        "state": "Updated State",
        "type": "Public",
        "mode": "Part Time",
        "courses": "Science, Arts"
    }
    response = requests.put(f"{BASE_URL}/update_college", json=data)
    print("Update College Response:", response.status_code, response.json())
    print("-"*50)

def test_update_nonexistent_college():
    data = {
        "name": "Nonexistent College",
        "city": "New City",
        "state": "New State",
        "type": "Public",
        "mode": "Full Time",
        "courses": "Law, Commerce"
    }
    response = requests.put(f"{BASE_URL}/update_college", json=data)
    print("Update Nonexistent College Response:", response.status_code, response.json())
    print("-"*50)

def test_get_colleges():
    response = requests.get(f"{BASE_URL}/get_colleges")
    print("Get Colleges Response:", response.status_code, response.json())
    print("-"*50)


if __name__ == "__main__":
    test_add_college()
    test_add_duplicate_college()
    test_update_college()
    test_update_nonexistent_college()
    test_get_colleges()