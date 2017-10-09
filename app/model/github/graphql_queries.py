from pathlib import Path

_pull_requests_query_path = Path(__file__, '..',
                                 'pull_requests_query.graphql').resolve()
with _pull_requests_query_path.open() as file:
    PULL_REQUESTS_QUERY = file.read()

_pull_request_query_path = Path(__file__, '..',
                                'pull_request_query.graphql').resolve()
with _pull_request_query_path.open() as file:
    PULL_REQUEST_QUERY = file.read()
