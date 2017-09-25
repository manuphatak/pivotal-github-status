from app import app
from flask import request


@app.route("/", methods=['POST'])
def index():

    app.logger.info(request.data)
    app.logger.info(request.form)
    app.logger.info(request.values)
    return "{'response': 'Ok'}"
