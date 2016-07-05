from flask import Flask

app = Flask(__name__, static_url_path='/application/static')
app.secret_key="developers only"
from application import views,models
# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
