from pathlib import Path


def read_file(file_name):
    file_path = Path(__file__, '..', file_name).resolve()
    with file_path.open() as file:
        return file.read()


PULL_REQUESTS_QUERY = read_file('pull_requests_query.graphql')
PULL_REQUEST_QUERY = read_file('pull_request_query.graphql')
