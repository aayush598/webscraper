import unittest
import json
from app import app

class TestCollegeAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_add_college(self):
        response = self.app.post("/add_college", 
                                 data=json.dumps({
                                     "name": "Test College",
                                     "city": "Test City",
                                     "state": "Test State",
                                     "type": "Private",
                                     "mode": "Full Time",
                                     "courses": "Engineering, Management"
                                 }), 
                                 content_type="application/json")
        self.assertIn(response.status_code, [201, 409])
    
    def test_add_duplicate_college(self):
        self.app.post("/add_college", data=json.dumps({
            "name": "Test College",
            "city": "Test City",
            "state": "Test State",
            "type": "Private",
            "mode": "Full Time",
            "courses": "Engineering, Management"
        }), content_type="application/json")
        
        response = self.app.post("/add_college", data=json.dumps({
            "name": "Test College",
            "city": "Another City",
            "state": "Another State",
            "type": "Public",
            "mode": "Part Time",
            "courses": "Science, Arts"
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 409)
        self.assertIn("College already exists", response.get_data(as_text=True))
    
    def test_update_college(self):
        self.app.post("/add_college", data=json.dumps({
            "name": "Test College",
            "city": "Test City",
            "state": "Test State",
            "type": "Private",
            "mode": "Full Time",
            "courses": "Engineering, Management"
        }), content_type="application/json")
        
        response = self.app.put("/update_college", data=json.dumps({
            "name": "Test College",
            "city": "Updated City",
            "state": "Updated State",
            "type": "Public",
            "mode": "Part Time",
            "courses": "Science, Arts"
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("College details updated successfully", response.get_data(as_text=True))
    
    def test_update_nonexistent_college(self):
        response = self.app.put("/update_college", data=json.dumps({
            "name": "Nonexistent College",
            "city": "New City",
            "state": "New State",
            "type": "Public",
            "mode": "Full Time",
            "courses": "Law, Commerce"
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("College not found", response.get_data(as_text=True))
    
    def test_get_colleges(self):
        response = self.app.get("/get_colleges")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)
    
if __name__ == "__main__":
    unittest.main()
