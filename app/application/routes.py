from flask import current_app as app


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'
