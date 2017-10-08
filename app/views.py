from . import app
from .model import github
from flask import request, jsonify, abort
import requests


def get_story_state(change):
    story_id = change['id']
    next_state = change['new_values']['current_state']
    return story_id, next_state


@app.route(
    "/<string:repo_owner>/<string:repo_name>/<string:access_token>",
    methods=['POST'])
def index(repo_owner, repo_name, access_token):
    for change in request.json['changes']:
        story_id, next_state = get_story_state(change)
        try:
            pull_requests = github.pull_requests(
                repo_owner, repo_name, access_token=access_token)
        except requests.HTTPError as e:
            return abort(e.response.status_code)

        for pull_request in pull_requests:
            if str(story_id) not in pull_request['title']:
                continue

            try:
                github.set_label(
                    pull_request['number'],
                    next_state,
                    access_token=access_token)
            except Exception as e:
                return abort(e.response.status_code)

    return jsonify(response='Ok')
