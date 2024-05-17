import requests
import time
import json
from bs4 import BeautifulSoup

URL = "http://127.0.0.1:8000/recommendation/"
LOGIN_URL = "http://127.0.0.1:8000/login/"
USERNAME = "shreyas"
PASSWORD = "FirstPatient!"

TEST_CASES = [
    {"age": "30", "symptoms": "headache, dizziness", "medical_conditions": "hypertension", "exercise": "Moderate"},
    {"age": "45", "symptoms": "cough, fever", "medical_conditions": "diabetes", "exercise": "Low"},
    {"age": "60", "symptoms": "chest pain, shortness of breath", "medical_conditions": "coronary artery disease", "exercise": "Low"},
    {"age": "25", "symptoms": "abdominal pain, nausea", "medical_conditions": "irritable bowel syndrome", "exercise": "Moderate"},
    {"age": "50", "symptoms": "joint pain, swelling", "medical_conditions": "rheumatoid arthritis", "exercise": "Low"},
    {"age": "35", "symptoms": "skin rash, itching", "medical_conditions": "eczema", "exercise": "High"},
    {"age": "70", "symptoms": "memory loss, confusion", "medical_conditions": "Alzheimer's disease", "exercise": "Low"},
    {"age": "55", "symptoms": "frequent urination, thirst", "medical_conditions": "type 2 diabetes", "exercise": "Moderate"},
    {"age": "40", "symptoms": "back pain, stiffness", "medical_conditions": "degenerative disc disease", "exercise": "Moderate"},
    {"age": "20", "symptoms": "headache, sensitivity to light", "medical_conditions": "migraine", "exercise": "High"},
]
NUMBER_OF_REQUESTS = 30

session = requests.Session()

def get_login_csrf_token():
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
    return csrf_token

login_csrf_token = get_login_csrf_token()
login_data = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrfmiddlewaretoken': login_csrf_token
}
login_response = session.post(LOGIN_URL, data=login_data)
login_response.raise_for_status()

def get_recommendation_csrf_token():
    response = session.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
    return csrf_token

results = []

for i in range(NUMBER_OF_REQUESTS):
    test_case = TEST_CASES[i % len(TEST_CASES)]
    csrf_token = get_recommendation_csrf_token()
    test_case['csrfmiddlewaretoken'] = csrf_token

    start_time = time.time()
    response = session.post(URL, data=test_case)
    end_time = time.time()
    response_time = end_time - start_time
    result = {
        "request_number": i + 1,
        "scenario": "common" if i < NUMBER_OF_REQUESTS / 2 else "specific",
        "response_time": response_time
    }
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        recommendation = soup.find('p').text if soup.find('p') else 'No recommendation found'
        result["response_content"] = recommendation[:200] 
    else:
        result["response_content"] = f"Error: {response.status_code}"
    results.append(result)
    print(f"Request {i+1}/{NUMBER_OF_REQUESTS} completed in {response_time:.2f} seconds")

with open('performance_metrics.json', 'w') as f:
    json.dump(results, f, indent=4)

