import requests
from .. import app

PIVOTAL_API_V5 = 'https://www.pivotaltracker.com/services/v5'


def _auth_headers(access_token):
    return {'X-TrackerToken': access_token, 'Content-Type': 'application/json'}


def story(story_id, access_token):
    url = f'{PIVOTAL_API_V5}/stories/{story_id}'
    response = requests.get(url, headers=_auth_headers(access_token))
    response.raise_for_status()
    _story = response.json()

    app.logger.info('Fetched pivotal story:%s state:%s name:%r', story_id,
                    _story['current_state'], _story['name'])
    return _story


def stories(story_ids, access_token):
    for story_id in story_ids:
        yield story(story_id, access_token)
