import requests

PIVOTAL_API_V5 = 'https://www.pivotaltracker.com/services/v5'


def _auth_headers(access_token):
    return {'X-TrackerToken': access_token, 'Content-Type': 'application/json'}


def story(project_id, story_id, access_token):
    url = f'{PIVOTAL_API_V5}/projects/{project_id}/stories/{story_id}'
    response = requests.get(url, headers=_auth_headers(access_token))
    response.raise_for_status()

    return response.json()
