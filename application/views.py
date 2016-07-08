import pygal

from application import app
from decorators import login_required
from flask import session, redirect, url_for, flash, request, render_template
from models import *


@app.route('/')
def home():
    return redirect(url_for('transform_view'))


@app.route('/well')
def simple():
    chart = pygal.Line(include_x_axis=True)
    chart.add('line', [.0002, .0005, .00035])
    chart.render()
    """ render svg graph """
    bar_chart = pygal.Bar()
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    bar_chart = bar_chart.render_data_uri()
    # return Response(response=bar_chart.render(), content_type='image/svg+xml')
    return render_template('controlpage.html', chart=bar_chart)
    # return chart.render_response()


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
        info = {"login": username,
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
        if session.get('logged_in'):
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


@app.route('/transform')
def transform_view():
    f = open("/application/static/installs/installs_com.rubeacon.redcup_201601_overview.csv")
    print f
    return True


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")
