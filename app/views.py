from app import app
from flask import request
import requests
import json


@app.route("/", methods=['POST'])
def index():

    access_token = app.config['GITHUB_ACCESS_TOKEN']
    headers = {
        'Authorization': f"bearer {access_token}",
        'Content-Type': 'application/json'
    }
    app.logger.info(('headers', headers))

    def set_label(change_id, change_status, pull_request):

        issue_number = pull_request['number']
        url = f"https://api.github.com/repos/bionikspoon/test_repo/issues/{issue_number}"
        response = requests.post(
            url, json.dumps({
                "labels": [change_status]
            }), headers=headers)

        app.logger.info(('response', response))

    def do(change):
        change_id = change['id']
        change_status = change['new_values']['current_state']

        app.logger.info(('change_id', change_id, 'change_status',
                         change_status))
        with open("label_and_pull_requests.graphql", "r") as query:
            query = "".join(query.readlines())

        app.logger.info(('query', query))
        url = 'https://api.github.com/graphql'
        response = requests.post(
            url, json.dumps({
                "query": query
            }), headers=headers)
        response_json = response.json()
        app.logger.info(('response_json', response_json))
        open_pull_requests = [
            edge['node']
            for edge in response_json['data']['repository']['pullRequests'][
                'edges']
        ]

        app.logger.info(('open_pull_requests', open_pull_requests))

        pull_requests = list(
            filter(lambda opr: str(change_id) in opr['title'],
                   open_pull_requests))

        app.logger.info(('pull_requests', pull_requests))

        [
            set_label(change_id, change_status, pull_request)
            for pull_request in pull_requests
        ]

    [do(change) for change in request.json['changes']]

    return "{'response': 'Ok'}"
