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
    installParam = 'curDevInst'
    dateParam = 'oneM'
    defDotSize=3

    curUser = request.cookies.get('username')
    print curUser
    qry = user.query(user.username == curUser)
    res = qry.fetch()
    if len(res) == 0:
        print 'No such userName'

    curAppName = res[0].appName
    print curAppName
    print "-------"

    if request.method == 'POST':
        installParam = request.form.get('selector')
        dateParam = request.form.get('selector_date')
        if dateParam!='oneM':
            defDotSize=1
    res = getInstallFromServerParam(curAppName, dateParam)

    chart = pygal.Line(show_x_labels=False,
                       width=700, height=300,
                       show_legend=False,
                       title=curAppName,
                       dots_size=defDotSize,
                       style=custom_style,
                       interpolate='cubic',
                       human_readable=True)

    print installParam
    print "-------"
    inst = getInstallWithParam(res, installParam)
    # change data to more obvious info
    chart.add('data', inst)
    dates = getInstallWithParam(res, 'date')
    chart.x_labels = dates
    chart = chart.render_data_uri()
    return render_template('controlpage.html', chart=chart, param1=installParam, param2=dateParam, curUser=curUser)


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
            if session.get('logged_in'):
                session.pop('logged_in', None)
            return redirect(url_for('login'))
        flash('Invalid Credentials. Please try again.')
    return render_template('registr.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # check
        if not (checkLogin(username, str(password))):
            flash('Invalid Credentials. Please try again.')
        else:
            resp = make_response(redirect(url_for('controlpage')))
            resp.set_cookie('username', username)
            session['logged_in'] = True
            flash('You were logged in.')
            return resp
    else:
        if session.get('logged_in'):
            return redirect(url_for('controlpage'))
    return render_template('login.html')


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
