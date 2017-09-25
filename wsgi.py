from app import app
import logging
import sys

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
if __name__ == '__main__':
    app.run()
