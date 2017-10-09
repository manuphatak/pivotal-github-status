from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import middleware  # noqa: E402,F401
from app import views  # noqa: E402,F401

if __name__ == '__main__':
    app.run(host='0.0.0.0')
