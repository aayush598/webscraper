# College Database API

This project is a Flask-based REST API for managing a college database using SQLite. It allows users to add, update, and retrieve college details while preventing duplicate entries.

## 📌 Features

- Add new colleges (ensures no duplicates)
- Update existing college details
- Retrieve all colleges based on filters (state, mode, type, and courses)
- Uses SQLite for persistent storage

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/aayush598/webscraper
cd webscraper
```

### 2️⃣ Create a Virtual Environment

```sh
python -m venv venv
```

Activate the virtual environment:

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App

```sh
python app.py
```

### 4️⃣ Run the streamlit ui

```sh
streamlit run ui.py
```

The server will start at **http://127.0.0.1:5000/**.

---

## 📡 API Endpoints

### **1️⃣ Add a College**

#### `POST /add_college`

**Request Body (JSON):**

```json
{
  "name": "Test College",
  "city": "Test City",
  "state": "Test State",
  "type": "Private",
  "mode": "Full Time",
  "courses": "UG Courses, PG Courses"
}
```

**Response:**

- `201 Created`: Successfully added
- `409 Conflict`: College already exists

---

### **2️⃣ Update College**

#### `PUT /update_college`

**Request Body (JSON):**

```json
{
  "name": "Test College",
  "city": "Updated City",
  "state": "Updated State",
  "type": "Public",
  "mode": "Part Time",
  "courses": "Diploma, PhD"
}
```

**Response:**

- `200 OK`: Successfully updated
- `404 Not Found`: College does not exist

---

### **3️⃣ Get Colleges (With Filters)**

#### `GET /get_colleges`

**Query Parameters:**

- `state` (optional) - Filter by state
- `mode` (optional) - Filter by study mode (Full Time, Part Time, Correspondence)
- `type` (optional) - Filter by college type (Private, Public, Public Private Partnership)
- `course` (optional) - Filter by courses offered

**Example Request:**

```sh
GET /get_colleges?state=Test%20State&type=Private&mode=Full%20Time&course=Engineering
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Test College",
    "city": "Test City",
    "state": "Test State",
    "type": "Private",
    "mode": "Full Time",
    "courses": "UG Courses, PG Courses"
  }
]
```

---

## 🖥️ Example React Frontend Code

```jsx
import React, { useState, useEffect } from "react";

function CollegeList() {
  const [colleges, setColleges] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_colleges")
      .then((response) => response.json())
      .then((data) => setColleges(data));
  }, []);

  return (
    <div>
      <h2>Colleges</h2>
      <ul>
        {colleges.map((college) => (
          <li key={college.id}>
            {college.name} - {college.state}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CollegeList;
```

---

## 🐍 Example Python API Code

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

def add_college():
    data = {
        "name": "New College",
        "city": "New City",
        "state": "Maharashtra",
        "type": "Public",
        "mode": "Full Time",
        "courses": "UG Courses, PhD"
    }
    response = requests.post(f"{BASE_URL}/add_college", json=data)
    print(response.json())

def get_colleges():
    response = requests.get(f"{BASE_URL}/get_colleges")
    print(response.json())

if __name__ == "__main__":
    add_college()
    get_colleges()
```

---

## 🛠 Running Tests

### **1️⃣ Unit Tests (`test_api.py`)**

Run unit tests using:

```sh
python -m unittest test_api.py
```

### **2️⃣ Manual API Testing (`test_requests.py`)**

Run API tests using requests:

```sh
python test_requests.py
```

---

## 🔥 Notes

- Ensure your **Flask server is running** before making API requests.
- If using a different port, update `BASE_URL` in `test_requests.py` accordingly.

---

## 📜 License

This project is open-source and available under the MIT License.
