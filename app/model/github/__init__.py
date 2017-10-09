import json
import requests
from ... import app
from .graphql_queries import PULL_REQUEST_QUERY, PULL_REQUESTS_QUERY

GITHUB_API_V3 = 'https://api.github.com'
GITHUB_API_V4 = 'https://api.github.com/graphql'


def _auth_headers(access_token):
    return {
        'Authorization': f"bearer {access_token}",
        'Content-Type': 'application/json'
    }


def _get_labels(pull_request):
    return (label['name'] for label in pull_request['labels']['nodes'])


def _next_labels(next_label, prev_labels):
    labels = (label for label in prev_labels
              if label not in app.config['MANAGED_LABELS'])

    return (*labels, next_label)


def set_label(pull_request, next_label, *, access_token):
    issue_id = pull_request['number']
    labels = _next_labels(next_label, _get_labels(pull_request))
    url = f"{GITHUB_API_V3}/repos/bionikspoon/test_repo/issues/{issue_id}"
    data = json.dumps({'labels': labels})

    response = requests.post(url, data, headers=_auth_headers(access_token))
    response.raise_for_status()
    app.logger.info('Added labels %r to github issue %i', labels, issue_id)

    return response


def pull_request(repo_owner, repo_name, pull_request_number, *, access_token):
    data = json.dumps({
        "query": PULL_REQUEST_QUERY,
        "variables": {
            "owner": repo_owner,
            "name": repo_name,
            "number": pull_request_number
        }
    })
    response = requests.post(
        GITHUB_API_V4, data, headers=_auth_headers(access_token))
    response.raise_for_status()

    return response.json()['data']['repository']['pullRequest']


def pull_requests(repo_owner, repo_name, *, access_token):
    data = json.dumps({
        "query": PULL_REQUESTS_QUERY,
        "variables": {
            "owner": repo_owner,
            "name": repo_name
        }
    })

    response = requests.post(
        GITHUB_API_V4, data, headers=_auth_headers(access_token))
    response.raise_for_status()

    return response.json()['data']['repository']['pullRequests']['nodes']
