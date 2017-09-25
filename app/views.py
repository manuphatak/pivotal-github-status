from app import app
from flask import request


@app.route("/", methods=['POST'])
def index():

    app.logger.info(request.form)
    return "{'response': 'Ok'}"
