import requests


class ApiException(Exception):
    ...


try:
    # test add user
    data = {
        'team_leader': 1, 'job': 'test', 'work_size': 15, 'collaborators': '1, 2'
    }
    response = requests.post('http://127.0.0.1:5000/api/v2/jobs', json=data)
    if response.status_code != 200:
        print(response.json())
        raise ApiException(1)
    job_id = response.json()['id']

    # test all users api
    response = requests.get('http://127.0.0.1:5000/api/v2/jobs')
    if response.status_code != 200:
        raise ApiException(2)
    all_jobs = response.json()

    if all_jobs[-1]['id'] != job_id:
        raise ApiException(3)

    # test get user
    response = requests.get(f'http://127.0.0.1:5000/api/v2/jobs/{job_id}')
    if response.status_code != 200 or response.json()['job'] != 'test':
        raise ApiException(4)

    # test del user
    response = requests.delete(f'http://127.0.0.1:5000/api/v2/jobs/{job_id}')
    if response.status_code != 200:
        raise ApiException(5)

except requests.exceptions.ConnectionError as _:
    print('error url')
except ApiException as e:
    print(e)
else:
    print('OK')