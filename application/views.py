import threading

import pygal

from application import app
from decorators import login_required
from flask import session, redirect, url_for, flash, request, render_template, make_response
from models import *

curAppName = ""
curUser = ""


@app.route('/update')
def update():
    t1 = threading.Thread(target=getInstallData)

    t2 = threading.Thread(target=getCrashesData)

    t3 = threading.Thread(target=getRatesData)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return redirect(url_for('welcome'))


# use decorators to link the function to a url
@app.route('/welcome')
def welcome():
    # flushDatastore()
    getInstallData()
    # getCrashesData()
    #getRatesData()
    return render_template('welcome.html')  # render a template


@app.route('/controlpage', methods=['GET', 'POST'])
@login_required
def controlpage():
    installParam = 'curDevInst'
    dateParam = 'oneM'
    defDotSize = 3

    curUser = request.cookies.get('username')

    qry = user.query(user.username == curUser)
    res = qry.fetch()
    if len(res) == 0:
        print 'No such userName'

    curAppName = res[0].appName

    chart = pygal.Line(show_x_labels=False,
                       width=600, height=400,
                       show_legend=False,
                       title=curAppName,
                       dots_size=defDotSize,
                       style=custom_style,
                       human_readable=True,
                       interpolate='cubic')

    if request.method == 'POST':
        installParam = request.form.get('selector')
        dateParam = request.form.get('selector_date')
        if dateParam != 'oneM':
            defDotSize = 2
            chart = pygal.Line(show_x_labels=False,
                               width=600, height=400,
                               show_legend=False,
                               title=curAppName,
                               dots_size=defDotSize,
                               style=custom_style,
                               human_readable=True)
        else:
            chart = pygal.Line(show_x_labels=False,
                               width=600, height=400,
                               show_legend=False,
                               title=curAppName,
                               dots_size=defDotSize,
                               style=custom_style,
                               human_readable=True,
                               interpolate='cubic')

        if (installParam == 'dailyCrashes'):
            res = getCrashFromServerParam(curAppName, dateParam)
            inst = getCrashesList(res, installParam)
            dates = getCrashesList(res, 'date')
            print "crashes"
        elif (installParam == 'dailyR') or (installParam == 'totalR'):
            res = getRateFromServerParam(curAppName, dateParam)
            inst = getRatesList(res, installParam)
            dates = getRatesList(res, 'date')
            print "rates"
        else:
            res = getInstallFromServerParam(curAppName, dateParam)
            inst = getInstallsWithParam(res, installParam)
            dates = getInstallsWithParam(res, 'date')
            print "installs"
    else:
        res = getInstallFromServerParam(curAppName, dateParam)
        inst = getInstallsWithParam(res, installParam)
        dates = getInstallsWithParam(res, 'date')
        print "get"

    chart.add('data', inst)
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
        res = addUser(info)
        if (res == 'ok'):
            flash('You were signed up.')
            if session.get('logged_in'):
                session.pop('logged_in', None)
            return redirect(url_for('login'))
        flash(res)
    return render_template('registr.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # check
        if not (checkLogin(username, str(password))):
            flash('Invalid Credentials. Please try again')
        else:
            resp = make_response(redirect(url_for('controlpage')))
            resp.set_cookie('username', username)
            session['logged_in'] = True
            flash('You were logged in')
            return resp
    else:
        if session.get('logged_in'):
            return redirect(url_for('controlpage'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
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
