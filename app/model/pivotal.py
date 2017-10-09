import requests
from .. import app

PIVOTAL_API_V5 = 'https://www.pivotaltracker.com/services/v5'


def _auth_headers(access_token):
    return {'X-TrackerToken': access_token, 'Content-Type': 'application/json'}


def story(project_id, story_id, access_token):
    url = f'{PIVOTAL_API_V5}/projects/{project_id}/stories/{story_id}'
    response = requests.get(url, headers=_auth_headers(access_token))
    response.raise_for_status()
    _story = response.json()

    app.logger.info('Fetched pivotal project:%s story:%s state:%s name:%r',
                    project_id, story_id, _story['current_state'],
                    _story['name'])
    return _story


def stories(project_id, story_ids, access_token):
    for story_id in story_ids:
        yield story(project_id, story_id, access_token)
