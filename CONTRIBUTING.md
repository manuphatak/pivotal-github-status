## Setup

- clone
- using `pipenv`
  - `pip install pipenv`
  - `pipenv --three`
  - `pipenv install -d`
  - `pipenv shell`
- start service with `bin/run`
- recommended: get ngrok:
  - run `ngrok http 5000`
- make code changes
- using `yapf` (`prettier` for python)
  - run `yapf -ri app`
- using `flake8` for linting
  - run `flake8`
- commit -> pr -> :+1:
