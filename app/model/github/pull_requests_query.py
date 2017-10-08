from pathlib import Path

query_path = Path(__file__, '..', 'pull_requests_query.graphql').resolve()
with query_path.open() as file:
    PULL_REQUESTS_QUERY = file.read()
