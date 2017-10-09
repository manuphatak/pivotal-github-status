from . import app
from .model import github, pivotal
from flask import request, jsonify, abort
import requests
import re

_re_story_ids = re.compile(r'[^#]*#(\d+)(?=[,\]\s])')

PIVOTAL_ACCESS_TOKEN = app.config['PIVOTAL_ACCESS_TOKEN']
GITHUB_ACCESS_TOKEN = app.config['GITHUB_ACCESS_TOKEN']


def log_and_abort(e):
    app.logger.warning('%s. Authorization: %s', e.args[0],
                       e.request.headers.get('Authorization', 'null'))

    return abort(e.response.status_code)


def get_story_state(change):
    story_id = change['id']
    next_state = change['new_values']['current_state']
    return story_id, next_state


def get_story_ids(title):
    return (match for match in _re_story_ids.findall(title))


@app.route('/github/<int:project_id>/<string:secret_key>', methods=['POST'])
def github_hook(project_id, secret_key):
    repo_owner = request.json['repository']['owner']['login']
    repo_name = request.json['repository']['name']
    pull_request_number = request.json['number']
    pull_request = github.pull_request(
        repo_owner,
        repo_name,
        pull_request_number,
        access_token=GITHUB_ACCESS_TOKEN)
    story_ids = get_story_ids(pull_request['title'])
    for story_id in story_ids:
        try:
            story = pivotal.story(
                project_id, story_id, access_token=PIVOTAL_ACCESS_TOKEN)
            next_label = story['current_state']
            github.set_label(
                pull_request, next_label, access_token=GITHUB_ACCESS_TOKEN)
        except requests.HTTPError as e:
            return log_and_abort(e)

        break

    return jsonify(response='Ok')


@app.route(
    '/pivotal/<string:repo_owner>/<string:repo_name>/<string:secret_key>',
    methods=['POST'])
def pivotal_hook(repo_owner, repo_name, secret_key):
    for change in request.json['changes']:
        story_id, next_label = get_story_state(change)
        try:
            pull_requests = github.pull_requests(
                repo_owner, repo_name, access_token=GITHUB_ACCESS_TOKEN)
        except requests.HTTPError as e:
            return log_and_abort(e)

        for pull_request in pull_requests:
            if str(story_id) not in pull_request['title']:
                continue

            try:
                github.set_label(
                    pull_request, next_label, access_token=GITHUB_ACCESS_TOKEN)
            except requests.HTTPError as e:
                return log_and_abort(e)

    return jsonify(response='Ok')
