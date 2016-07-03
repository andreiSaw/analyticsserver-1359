from flask import Flask

app = Flask(__name__, static_url_path='/application/static')

from application import views, models

if __name__ == '__main__':
    app.run()
