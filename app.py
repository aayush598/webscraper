from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("colleges.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS colleges (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE,
                            city TEXT,
                            state TEXT,
                            type TEXT,
                            mode TEXT,
                            courses TEXT)''')
        conn.commit()

@app.route('/')
def hello():
    return 'Hello World!'


@app.route("/add_college", methods=["POST"])
def add_college():
    data = request.get_json()
    name = data.get("name")
    city = data.get("city", "")
    state = data.get("state")
    college_type = data.get("type", "")
    mode = data.get("mode", "")
    courses = data.get("courses", "")
    
    if not name or not state:
        return jsonify({"error": "Name and State are required"}), 400
    
    with sqlite3.connect("colleges.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colleges WHERE name = ?", (name,))
        existing_college = cursor.fetchone()
        if existing_college:
            return jsonify({"message": "College already exists in the database"}), 409
        cursor.execute("INSERT INTO colleges (name, city, state, type, mode, courses) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, city, state, college_type, mode, courses))
        conn.commit()
    return jsonify({"message": "College added successfully"}), 201

@app.route("/update_college", methods=["PUT"])
def update_college():
    data = request.get_json()
    name = data.get("name")
    city = data.get("city")
    state = data.get("state")
    college_type = data.get("type")
    mode = data.get("mode")
    courses = data.get("courses")
    
    if not name:
        return jsonify({"error": "College name is required for updating"}), 400
    
    with sqlite3.connect("colleges.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colleges WHERE name = ?", (name,))
        existing_college = cursor.fetchone()
        if not existing_college:
            return jsonify({"error": "College not found"}), 404
        cursor.execute("""
            UPDATE colleges SET city = ?, state = ?, type = ?, mode = ?, courses = ?
            WHERE name = ?
        """, (city, state, college_type, mode, courses, name))
        conn.commit()
    return jsonify({"message": "College details updated successfully"}), 200

@app.route("/get_colleges", methods=["GET"])
def get_colleges():
    with sqlite3.connect("colleges.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colleges")
        colleges = [dict(id=row[0], name=row[1], city=row[2], state=row[3], type=row[4], mode=row[5], courses=row[6]) for row in cursor.fetchall()]
    return jsonify(colleges)

@app.route("/get_colleges_by_state", methods=["GET"])
def get_colleges_by_state():
    state = request.args.get("state")
    if not state:
        return jsonify({"error": "State parameter is required"}), 400
    with sqlite3.connect("colleges.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colleges WHERE state = ?", (state,))
        colleges = [dict(id=row[0], name=row[1], city=row[2], state=row[3], type=row[4], mode=row[5], courses=row[6]) for row in cursor.fetchall()]
    return jsonify(colleges)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)