import requests


data = {
    'name': '123',
    'surname': '456',
    'age': 21,
    'position': 'test',
    'speciality': 'test',
    'address': 'tam',
    'email': 'test@test.test',
    'hashed_password': '1234',
}

response = requests.post('http://127.0.0.1:5000/api/users', json=data)
print(response.json())