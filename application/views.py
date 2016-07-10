import pygal

from application import app
from decorators import login_required
from flask import session, redirect, url_for, flash, request, render_template, make_response
from models import *

curAppName = ""
curUser = ""


@app.route('/')
def home():
    return redirect(url_for('welcome'))


# use decorators to link the function to a url
@app.route('/welcome')
def welcome():
    # flushDatastore()
    # getData()
    return render_template('welcome.html')  # render a template


@app.route('/controlpage', methods=['GET', 'POST'])
@login_required
def controlpage():
    param='curDevInst'
    curUser = request.cookies.get('username')
    print curUser
    qry = user.query(user.username == curUser)
    res = qry.fetch()
    if len(res) == 0:
        print 'pizdec'

    curAppName = res[0].appName
    print curAppName
    chart = pygal.Line(show_x_labels=False,
                       width=800, height=500,
                       show_legend=False)
    if request.method == 'POST':
        param=request.form.get('selector')

        res = getInstallFromServer(curAppName, "2016-05-01", "2016-07-01")
    else:
        res = getInstallFromServer(curAppName, "2016-05-01", "2016-07-01")
    print param
    print "-------"
    inst = getInstallWithParam(res, param)
    chart.add('data', inst)
    dates = getInstallWithParam(res, 'date')
    chart.x_labels = dates
    chart = chart.render_data_uri()
    return render_template('controlpage.html', chart=chart,param1=param)


# route for handling the login page logic
@app.route('/registr', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        appName = request.form["appName"]
        info = {"login": username,
                "email": email,
                "password": password,
                "appName": appName
                }
        if (addUser(info)):
            flash('You were signed up.')
            return redirect(url_for('login'))
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
            resp = make_response(redirect(url_for('controlpage')))
            resp.set_cookie('username', username)
            session['logged_in'] = True
            flash('You were logged in.')
            return resp
    else:
        if session.get('logged_in'):
            return redirect(url_for('controlpage'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    curAppName = ""
    curUser = ""
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
