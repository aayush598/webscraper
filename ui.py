import streamlit as st
import requests

# Flask API Base URL
BASE_URL = "http://127.0.0.1:5000"

# Function to fetch colleges from the Flask API
def get_colleges(state, mode, college_type, course):
    params = {}
    if state and state != "All States":
        params["state"] = state
    if mode and mode != "All Modes":
        params["mode"] = mode
    if college_type and college_type != "All Types":
        params["type"] = college_type
    if course and course != "All Courses":
        params["course"] = course
    
    response = requests.get(f"{BASE_URL}/get_colleges", params=params)
    if response.status_code == 200:
        return response.json()
    return []

# Streamlit UI
st.title("College Search Portal")
st.sidebar.header("Filters")

# Filters
states = ["All States", "Andaman & Nicobar", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra & Nagar Haveli", "Daman & Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Pondicherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Telangana", "Ladakh"]
selected_state = st.sidebar.selectbox("Select State", states)

modes = ["All Modes", "Full Time", "Part Time", "Correspondence"]
selected_mode = st.sidebar.selectbox("Select Mode", modes)

college_types = ["All Types", "Private", "Public", "Public Private Partnership"]
selected_type = st.sidebar.selectbox("Select College Type", college_types)

courses = ["All Courses", "UG Courses", "PG Courses", "Courses after 10th", "Fellowship / Doctoral", "Diploma", "Courses After 12th", "Certificate", "Pursuing Doctorate/Fellowship"]
selected_course = st.sidebar.selectbox("Select Course", courses)

if st.sidebar.button("Search"):
    results = get_colleges(selected_state, selected_mode, selected_type, selected_course)
    if results:
        st.write(f"### {len(results)} College(s) Found")
        for row in results:
            st.write(f"**{row['name']}** - {row['city']}, {row['state']} ({row['type']}, {row['mode']})")
            st.write(f"Courses: {row['courses']}")
            st.write("---")
    else:
        st.write("### No colleges found matching your criteria.")
