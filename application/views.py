import csv
import io

import pygal

from application import app
from decorators import login_required
from flask import session, redirect, url_for, flash, request, render_template
from models import *


@app.route('/')
def home():
    return redirect(url_for('welcome'))


# use decorators to link the function to a url
@app.route('/welcome')
def welcome():
    list = [
        "application/static/installs/installs_com.rubeacon.redcup_201507_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201508_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201509_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201510_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201511_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201512_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201601_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201602_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201603_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201604_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201605_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201606_overview.csv",
        "application/static/installs/installs_com.rubeacon.redcup_201607_overview.csv"]
    for entry in list:
        f = open(entry)
        stream = io.StringIO(f.read().decode("UTF16"), newline=None)
        csv_input = csv.reader(stream)
        flag = False
        for row in csv_input:
            print(row)
            if (not (flag)):
                flag = True
            else:
                info = {'date': row[0], 'appName': row[1], 'curDevInst': int(row[2]), 'dailyDevInst': int(row[3]),
                        'dailyDevUnist': int(row[4]), 'dailyDevUp': int(row[5]),
                        'curUserInst': int(row[6]), 'totUserInst': int(row[7]), 'dailyUserInst': int(row[8]),
                        'dailyUserUninst': int(row[9])
                        }
                primitiveUlpoadOnServer(info)
        f.close()
    return render_template('welcome.html')  # render a template


@app.route('/controlpage')
@login_required
def controlpage():
    res = getInstallFromServer("com.rubeacon.redcup", "2016-05-01", "2016-07-01")
    # curDevInst = getInstallWithParam(res, 'curDevInst')
    dailyDevInst = getInstallWithParam(res, 'dailyDevInst')
    dailyDevUnist = getInstallWithParam(res, 'dailyDevUnist')
    dates = getInstallWithParam(res, 'date')

    chart = pygal.Line(show_x_labels=False)
    # chart.add('Current Device Installs', curDevInst)
    chart.add('Daily Device Installs', dailyDevInst)
    chart.add('Daily Device Uninstalls', dailyDevUnist)
    chart.x_labels=dates

    chart = chart.render_data_uri()
    return render_template('controlpage.html', chart=chart)  # render a template


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
