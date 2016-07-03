from flask import Flask

app = Flask(__name__)

from application import views, models

if __name__ == '__main__':
    app.run()
