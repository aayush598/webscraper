# College Database API

This project is a Flask-based REST API for managing a college database using SQLite. It allows users to add, update, and retrieve college details while preventing duplicate entries.

## 📌 Features

- Add new colleges (ensures no duplicates)
- Update existing college details
- Retrieve all colleges
- Get colleges by state
- Uses SQLite for persistent storage

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone <repo-url>
cd <repo-folder>
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
  "courses": "Engineering, Management"
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
  "courses": "Science, Arts"
}
```

**Response:**

- `200 OK`: Successfully updated
- `404 Not Found`: College does not exist

---

### **3️⃣ Get All Colleges**

#### `GET /get_colleges`

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
    "courses": "Engineering, Management"
  }
]
```

---

### **4️⃣ Get Colleges by State**

#### `GET /get_colleges_by_state?state=Test State`

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
    "courses": "Engineering, Management"
  }
]
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
