import requests


class ApiException(Exception):
    ...


try:
    # test all users api
    response = requests.get('http://127.0.0.1:5555/api/v2/users')
    if response.status_code != 200:
        raise ApiException(1)

    # test add user
    data = {
        'surname': '1',
        'name': '2',
        'age': '3',
        'position': '4',
        'speciality': '5',
        'address': '6',
        'email': 'test@test.test',
        'hashed_password': '123'
    }
    response = requests.post('http://127.0.0.1:5555/api/v2/users', json=data)
    if response.status_code != 200:
        print(response.json())
        raise ApiException(2)
    _id = response.json()['id']

    # test get user
    response = requests.get(f'http://127.0.0.1:5555/api/v2/users/{_id}')
    if response.status_code != 200 or response.json()['email'] != 'test@test.test':
        raise ApiException(3)

    # test del user
    response = requests.delete(f'http://127.0.0.1:5555/api/v2/users/{_id}')
    if response.status_code != 200:
        raise ApiException(4)

except requests.exceptions.ConnectionError as _:
    print('error url')
except ApiException as e:
    print(e)
else:
    print('OK')