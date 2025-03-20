import requests

job = {
    'job': '12',
}

print(requests.post('http://127.0.0.1:5555/api/jobs', json=job).status_code)