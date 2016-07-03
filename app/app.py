# import the Flask class from the flask module
from functools import wraps

from google.appengine.ext import ndb

from flask import Flask, render_template, redirect, url_for, request, session, flash, g

# config
#  create the application object
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'my precious'


class User(ndb.Model):
    """Sub model for representing an author."""
    username = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
def home():
    return redirect(url_for('welcome'))


# use decorators to link the function to a url
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/main')
def mainpage():
    return render_template('main.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))
