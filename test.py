import requests

BASE_URL = 'http://127.0.0.1:5555/api/jobs'


class CheckException(ValueError):
    ...


try:
    all_response = requests.get(url=BASE_URL)
    if all_response.status_code == 404:
        raise CheckException(1)
    else:
        all_response = all_response.json()['jobs']

    one_response = requests.get(url=f'{BASE_URL}/0')

    if one_response.status_code == 404 and all_response[0] != one_response.json():
        raise CheckException(2)
    
    if requests.get(url=f'{BASE_URL}/-1').status_code != 404:
        raise CheckException(3)
    
    if requests.get(url=f'{BASE_URL}/hello').status_code != 404:
        raise CheckException(4)
except requests.ConnectionError as Err:
    print(Err)
except CheckException as Err:
    print(f'{Err} test failed')
else:
    print('OK')