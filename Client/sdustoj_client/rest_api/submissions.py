import requests
from requests.auth import HTTPBasicAuth
from config import CLIENT_SETTINGS


url = CLIENT_SETTINGS['root_url'].rstrip('/') + '/' + CLIENT_SETTINGS['submission_url'].lstrip('/')
username = CLIENT_SETTINGS['username']
password = CLIENT_SETTINGS['password']
auth = HTTPBasicAuth(username, password)


def request_submit(submission_json):
    request_url = '%s/' % (url.rstrip('/'),)
    r = requests.post(url, submission_json, auth=auth)
    if r.status_code == 201:
        return r.json()
    else:
        return None


def submit(submission_json):
    """
    发起一次提交，将submission提交到Server端。该函数会返回Server端的请求回执信息。
    :param submission_json: 
    :return: 
    """
    chance_left = 3
    result = None
    while result is None and chance_left > 0:
        print('submitting submission, tried %s ......' % (3 - chance_left,))
        result = request_submit(submission_json)
        chance_left -= 1
    if result is None:
        print('submitting submission failed')
    return result
