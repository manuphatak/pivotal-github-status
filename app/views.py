from app import app
from flask import request


@app.route("/", methods=['POST'])
def index():

    app.logger.debug(request.form)
    return "{'response': 'Ok'}"
