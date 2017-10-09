from . import app
from .model import github, pivotal
from flask import request, abort
import requests
import re

PIVOTAL_ACCESS_TOKEN = app.config['PIVOTAL_ACCESS_TOKEN']
GITHUB_ACCESS_TOKEN = app.config['GITHUB_ACCESS_TOKEN']
BLACKLISTED_GITHUB_ACTIONS = ('labeled', 'unlabeled')


def log_and_abort(e):
    app.logger.warning('%s. Authorization: %s', e.args[0],
                       e.request.headers.get('Authorization', 'null'))

    return abort(e.response.status_code)


def get_story_ids(title):
    _re_story_ids = re.compile(r'[^#]*#(\d+)(?=[,\]\s])')
    return (match for match in _re_story_ids.findall(title))


def pull_requests_for_story(owner, repo, story_id):
    try:
        pull_requests = github.pull_requests(
            owner, repo, access_token=GITHUB_ACCESS_TOKEN)
    except requests.HTTPError as e:
        return log_and_abort(e)

    for pull_request in pull_requests:
        if story_id not in pull_request['title']:
            continue

        yield pull_request


def set_pull_request_labels(pull_request, project_id):
    story_ids = get_story_ids(pull_request['title'])
    try:
        labels = (
            story['current_state']
            for story in pivotal.stories(
                project_id, story_ids, access_token=PIVOTAL_ACCESS_TOKEN))
        github.set_labels(
            pull_request, labels, access_token=GITHUB_ACCESS_TOKEN)
    except requests.HTTPError as e:
        return log_and_abort(e)


@app.route('/github/<int:project_id>/<string:secret_key>', methods=['POST'])
def github_hook(project_id, secret_key):
    if request.json['action'] in BLACKLISTED_GITHUB_ACTIONS:
        app.logger.info('Ignoring %s event from github',
                        request.json['action'])
        return ('', 200)

    owner = request.json['repository']['owner']['login']
    repo = request.json['repository']['name']
    pull_request_number = request.json['number']

    pull_request = github.pull_request(
        owner, repo, pull_request_number, access_token=GITHUB_ACCESS_TOKEN)

    set_pull_request_labels(pull_request, project_id)

    return ('', 204)


@app.route(
    '/pivotal/<int:project_id>/<string:owner>/<string:repo>/<string:secret_key>',  # noqa E501
    methods=['POST'])
def pivotal_hook(project_id, owner, repo, secret_key):
    for change in request.json['changes']:
        story_id = str(change['id'])

        for pull_request in pull_requests_for_story(owner, repo, story_id):
            set_pull_request_labels(pull_request, project_id)

    return ('', 204)
