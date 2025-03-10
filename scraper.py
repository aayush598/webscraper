import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import json

def get_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        
        # Apply filtering logic
        filtered_lines = []
        for line in text.split('\n'):
            if line.strip() and "No Options Found" not in line:
                filtered_lines.append(line.strip())
        
        return '\n'.join(filtered_lines)
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

def save_text_to_file(url, content):
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".txt"
    output_dir = "scraped_data"
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved content from {url} to {filename}")
    
    return filename, filepath

def store_in_database(filename, url, content, json_data):
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            url TEXT,
            content TEXT,
            json_data TEXT
        )
    """)
    
    cursor.execute("""
        INSERT INTO scraped_info (filename, url, content, json_data) 
        VALUES (?, ?, ?, ?)""", (filename, url, content, json.dumps(json_data)))
    
    conn.commit()
    conn.close()
    print(f"Stored {filename} in the database.")

def send_to_gemini_api(text_content, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    prompt = {
        "contents": [{
            "parts": [{
                "text": """
                Extract and structure the data from the following content into a structured JSON format. 
                The required fields are:
                - college_name: Name of the college/institution.
                - available_courses: List of courses offered.
                - sub_stream: Specialization or sub-category of the courses.
                - state: The state where the college is located.
                - city: The city where the college is located.
                - type: Whether the institution is Private, Public, or a Public-Private Partnership.
                - level: Education level (e.g., UG Courses, PG Courses, Diploma, PhD, etc.).
                Return the output as a JSON array.
                """
            }]
        }]
    }
    
    response = requests.post(url, json=prompt, headers=headers)
    return response.json()

def main():
    input_file = "urls.txt"
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    
    with open(input_file, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]
        
    for url in urls:
        print(f"Scraping: {url}")
        content = get_text_from_url(url)
        filename, filepath = save_text_to_file(url, content)
        
        # Sending scraped content to Gemini API
        gemini_response = send_to_gemini_api(content[:3000], api_key)  # Truncate if needed
        
        if "candidates" in gemini_response:
            json_data = gemini_response["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
            try:
                structured_data = json.loads(json_data)
            except json.JSONDecodeError:
                structured_data = []
        else:
            structured_data = []
        
        store_in_database(filename, url, content, structured_data)
        
        # Save structured JSON to a file
        json_filename = filename.replace(".txt", ".json")
        json_filepath = os.path.join("scraped_data", json_filename)
        with open(json_filepath, "w", encoding="utf-8") as json_file:
            json.dump(structured_data, json_file, indent=4)
        print(f"Saved structured data to {json_filename}")

if __name__ == "__main__":
    main()