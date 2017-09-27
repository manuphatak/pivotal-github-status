from app import app
from flask import request
import requests
import json

with open("label_and_pull_requests.graphql", "r") as file:
    QUERY = "".join(file.readlines())

access_token = app.config['GITHUB_ACCESS_TOKEN']
GITHUB_HEADERS = {
    'Authorization': f"bearer {access_token}",
    'Content-Type': 'application/json'
}


def get_story_state(change):
    story_id = change['id']
    next_state = change['new_values']['current_state']

    app.logger.info(('story_id', story_id, 'next_state', next_state))
    return story_id, next_state


def get_pull_requests(repo_owner, repo_name):
    url = 'https://api.github.com/graphql'
    data = json.dumps({
        "query": QUERY,
        "variables": {
            "owner": repo_owner,
            "name": repo_name
        }
    })

    response = requests.post(url, data, headers=GITHUB_HEADERS)
    response_json = response.json()
    app.logger.info(('response_json', response_json))
    return [
        edge['node']
        for edge in response_json['data']['repository']['pullRequests'][
            'edges']
    ]


def set_label(next_state, issue_number):
    url = f"https://api.github.com/repos/bionikspoon/test_repo/issues/{issue_number}"
    data = json.dumps({"labels": [next_state]})
    response = requests.post(url, data, headers=GITHUB_HEADERS)

    app.logger.info(('response', response))


@app.route("/<string:repo_owner>/<string:repo_name>", methods=['POST'])
def index(repo_owner, repo_name):

    app.logger.info(('GITHUB_HEADERS', GITHUB_HEADERS))
    app.logger.info(('request.remote_addr', request.remote_addr))
    app.logger.info(('request.headers', request.headers))
    app.logger.info(('repo_owner, repo_name', repo_owner, repo_name))
    app.logger.info(('QUERY', QUERY))

    for change in request.json['changes']:
        story_id, next_state = get_story_state(change)
        pull_requests = filter(lambda opr: str(story_id) in opr['title'],
                               get_pull_requests(repo_owner, repo_name))

        app.logger.info(('pull_requests', pull_requests))
        for pull_request in pull_requests:
            set_label(next_state, pull_request['number'])

    return "{'response': 'Ok'}"
