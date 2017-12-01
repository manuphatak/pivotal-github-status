import json
import requests
from ... import app
from .graphql_queries import PULL_REQUEST_QUERY, PULL_REQUESTS_QUERY

GITHUB_API_V3 = 'https://api.github.com'
GITHUB_API_V4 = 'https://api.github.com/graphql'


def _auth_headers(access_token):
    return {
        'Authorization': f'bearer {access_token}',
        'Content-Type': 'application/json'
    }


def _get_labels(pull_request):
    return (label['name'] for label in pull_request['labels']['nodes'])


def _next_labels(next_labels, prev_labels):
    labels = (label for label in prev_labels
              if label not in app.config['MANAGED_LABELS'])

    return (*labels, *next_labels)


def set_labels(pull_request, owner, repo, labels, *, access_token):
    issue_id = pull_request['number']
    next_labels = tuple(_next_labels(labels, _get_labels(pull_request)))
    url = f'{GITHUB_API_V3}/repos/{owner}/{repo}/issues/{issue_id}'
    data = json.dumps({'labels': next_labels})

    response = requests.post(url, data, headers=_auth_headers(access_token))
    response.raise_for_status()
    app.logger.info('Added labels %r to github issue %i', next_labels,
                    issue_id)

    return response


def pull_request(repo_owner, repo_name, pull_request_number, *, access_token):
    data = json.dumps({
        'query': PULL_REQUEST_QUERY,
        'variables': {
            'owner': repo_owner,
            'name': repo_name,
            'number': pull_request_number
        }
    })
    response = requests.post(
        GITHUB_API_V4, data, headers=_auth_headers(access_token))
    response.raise_for_status()

    pull_request = response.json()['data']['repository']['pullRequest']

    app.logger.info('Fetched github pull_request #%s for %s/%s: %r',
                    pull_request_number, repo_owner, repo_name,
                    pull_request['title'])

    return pull_request


def pull_requests(repo_owner, repo_name, *, access_token):
    data = json.dumps({
        'query': PULL_REQUESTS_QUERY,
        'variables': {
            'owner': repo_owner,
            'name': repo_name
        }
    })

    response = requests.post(
        GITHUB_API_V4, data, headers=_auth_headers(access_token))
    response.raise_for_status()

    app.logger.info('Fetched github pull_requests for %s/%s', repo_owner,
                    repo_name)

    return response.json()['data']['repository']['pullRequests']['nodes']
