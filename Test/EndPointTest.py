# This file is used to test endpoint connections(for testing) Run locally(python .\test.py)

"""
You also can use 
#  Write test data
curl -X POST http://localhost:8081/health/db/test

#  Read test data
curl http://localhost:8081/health/db/test

# Clear test data
curl -X DELETE http://localhost:8081/health/db/test
"""
import requests
# Write test data
response = requests.post("http://localhost:8081/health/db/test")
print(response.json())

# Read test data  
response = requests.get("http://localhost:8081/health/db/test")
print(response.json())

# Clear test data
response = requests.delete("http://localhost:8081/health/db/test")
print(response.json())