from application import app

from flask import session, redirect, url_for, flash, request, render_template, jsonify
from decorators import login_required
from models import *


@app.route('/')
def home():
    return redirect(url_for('welcome'))


# use decorators to link the function to a url
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/controlpage')
@login_required
def controlpage():
    return render_template('controlpage.html')  # render a template


# route for handling the login page logic
@app.route('/registr', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        info = {"userid": 1,
                "login": username,
                "email": email,
                "password": password
                }
        if (addUser(info)):
            session['logged_in'] = True
            flash('You were signed up.')
            return redirect(url_for('controlpage'))
        error = 'Invalid Credentials. Please try again.'
    return render_template('registr.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # check
        if not (checkLogin(username, str(password))):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('controlpage'))
    else:
        if (session.get('logged_in')):
            return redirect(url_for('controlpage'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# Add an error handler. This is useful for debugging the live application,
# however, you should disable the output of the exception for production
# applications.
@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
