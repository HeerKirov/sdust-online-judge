import requests
from requests.auth import HTTPBasicAuth
from config import CLIENT_SETTINGS
from json.decoder import JSONDecodeError


url = CLIENT_SETTINGS['root_url'].rstrip('/') + '/' + CLIENT_SETTINGS['submission_url'].lstrip('/')
username = CLIENT_SETTINGS['username']
password = CLIENT_SETTINGS['password']
auth = HTTPBasicAuth(username, password)


def request_submit(submission_json):
    request_url = '%s/' % (url.rstrip('/'),)
    r = requests.post(url, json=submission_json, auth=auth)
    try:
        result = r.status_code == 201, r.json()
    except JSONDecodeError:
        result = False, {'error': 'Internal Server Error.'}
    return result


def submit(submission_json):
    """
    发起一次提交，将submission提交到Server端。该函数会返回Server端的请求回执信息。
    :param submission_json: 
    :return: 
    """
    chance_left = 3
    result = False
    json = None
    while result is False and chance_left > 0:
        print('submitting submission, tried %s ......' % (3 - chance_left,))
        result, json = request_submit(submission_json)
        chance_left -= 1
    if result is False:
        print('submitting submission failed')
    return result, json
