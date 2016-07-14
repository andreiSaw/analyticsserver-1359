import csv
import datetime
import io
import logging
import os
import re
import threading

from dateutil.relativedelta import relativedelta
from google.appengine.ext import ndb
from pygal.style import Style

from werkzeug.security import generate_password_hash, check_password_hash

tkey = ndb.Key('user', 'newUser')

custom_style = Style(
    plot_background='rgba(255, 255, 255, 0.6)',
    background='rgba(255, 255, 255, 0.2)',
    value_background='rgba(229, 229, 229, 1)',
    foreground='rgba(0, 0, 0, .87)',
    foreground_strong='rgba(0, 0, 0, 1)',
    foreground_subtle='rgba(0, 0, 0, .54)',
    opacity='.6',
    opacity_hover='.9',
    colors=('rgb(11, 124, 184)', '#E8537A', '#E95355', '#E87653', '#E89B53'))


class user(ndb.Model):
    userid = ndb.IntegerProperty()
    username = ndb.StringProperty()
    pw_hash = ndb.StringProperty()
    email = ndb.StringProperty()
    appName = ndb.StringProperty()

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


def addUser(info):
    res = validate(info)
    if res != 'ok':
        return res
    newUser = user()
    newUser.username = info["login"]
    newUser.set_password(info["password"])
    newUser.email = info["email"]
    newUser.appName = info["appName"]
    newUser.put()
    return res


def validate(info):
    res = checkIfAlreadyExists(info)
    regex = "[^@]+@[^@]+\.[^@]"
    if res != 'ok':
        return res
    if len(info["login"]) < 4:
        res = 'Login should be provided with more that 4 symbols'
        return res
    if len(info["password"]) < 6:
        res = 'Password should be provided with more that 6 symbols'
        return res
    if not (re.match(regex, info["email"])):
        res = "Sorry, invalid email"
        return res
    return 'ok'


def checkLogin(_name, _pass):
    qry = user.query(user.username == _name)
    # delete
    logging.debug(_name)

    res = qry.fetch(1)
    # delete pls
    logging.debug(res)

    if len(res) == 0:
        return False

    elif res[0].check_password(str(_pass)):
        return True
    else:
        return False


def checkIfAlreadyExists(info):
    qry = user.query(user.username == info["login"])
    res = qry.fetch(1)
    logging.debug(res)
    if (len(res) != 0):
        return str.format("User with login %s already exist", info["login"])
    qry = user.query(user.email == info["email"])
    res = qry.fetch(1)
    if (len(res) != 0):
        return str.format("User with email %s already exist", info["email"])
    return "ok"


class install(ndb.Model):
    date = ndb.StringProperty()
    intDate = ndb.IntegerProperty()
    day = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    appName = ndb.StringProperty()
    curDevInst = ndb.IntegerProperty()
    dailyDevInst = ndb.IntegerProperty()
    dailyDevUnist = ndb.IntegerProperty()
    dailyDevUp = ndb.IntegerProperty()
    curUserInst = ndb.IntegerProperty()
    totUserInst = ndb.IntegerProperty()
    dailyUserInst = ndb.IntegerProperty()
    dailyUserUninst = ndb.IntegerProperty()

    def getIntDate(self):
        str1 = self.date[:4] + self.date[5:7] + self.date[-2:]
        return int(str1)


def getInstallsWithParam(installist, param):
    newList = []
    for inst in installist:
        switch = {
            'date': inst.date,
            'curDevInst': inst.curDevInst,
            'dailyDevInst': inst.dailyDevInst,
            'dailyDevUnist': inst.dailyDevUnist,
            'dailyDevUp': inst.dailyDevUp,
            'curUserInst': inst.curUserInst,
            'totUserInst': inst.totUserInst,
            'dailyUserInst': inst.dailyUserInst,
            'dailyUserUninst': inst.dailyUserUninst
        }
        newList.append(switch[param])
    return newList


def getCrashesList(crashes, param):
    newList = []
    for cr in crashes:
        switch = {
            'date': cr.date,
            'dailyCrashes': cr.dailyCrashes}
        newList.append(switch[param])
    return newList


def primitiveUlpoadOnServer(info):
    if not (checkIfInstallExist(info)):
        uploadInstall(info)


def checkIfInstallExist(info):
    qry = install.query(install.appName == info["appName"], install.date == info["date"])
    res = qry.fetch()
    logging.debug(res)
    if len(res) == 0:
        return False
    return True


def forceInstallUpload(info):
    uploadInstall(info)


def uploadInstall(info):
    new_install = install()
    new_install.date = info["date"]
    logging.debug(info['date'][:4])
    new_install.year = int(info['date'][:4])
    new_install.month = int(info['date'][5:7])
    logging.debug(info['date'][5:7])
    new_install.day = int(info['date'][-2:])
    logging.debug(info['date'][-2:])
    new_install.intDate = new_install.getIntDate()
    new_install.appName = info['appName']
    new_install.curDevInst = int(info['curDevInst'])
    new_install.dailyDevInst = int(info['dailyDevInst'])
    new_install.dailyDevUnist = int(info['dailyDevUnist'])
    new_install.dailyDevUp = int(info['dailyDevUp'])
    new_install.curUserInst = int(info['curUserInst'])
    new_install.totUserInst = int(info['totUserInst'])
    new_install.dailyUserInst = int(info['dailyUserInst'])
    new_install.dailyUserUninst = int(info['dailyUserUninst'])
    new_install.put()


def numeric_compare(x, y):
    year1 = int(x.date[:4])
    month1 = int(x.date[5:7])
    day1 = int(x.date[-2:])
    year2 = int(y.date[:4])
    month2 = int(y.date[5:7])
    day2 = int(y.date[-2:])
    if (year1 > year2):
        return 1
    elif (month1 > month2):
        return 1
    elif (day1 > day2):
        return 1
    elif (day2 == day1):
        return 0
    return -1


def getInstallFromServer(appName, dateStartWith, dateEndsWith):
    date1 = int(dateStartWith[:4] + dateStartWith[5:7] + dateStartWith[-2:])
    date2 = int(dateEndsWith[:4] + dateEndsWith[5:7] + dateEndsWith[-2:])

    qry = install.query(install.appName == appName, install.intDate >= date1, install.intDate <= date2)
    res = qry.fetch()
    res = sorted(res, cmp=numeric_compare)
    logging.debug(res)
    return res


def getInstallFromServerParam(appName, param):
    today = datetime.datetime.now()
    day = datetime.timedelta(days=1)
    datetoString = today - day

    switch = {
        'oneM': relativedelta(months=1),
        'threeM': relativedelta(months=3),
        'sixM': relativedelta(months=6),
        'twelveM': relativedelta(months=12),
        'allTime': relativedelta(months=72)
    }

    start = datetoString - switch[param]

    startDate = str(start)[:10]
    finishdate = str(datetoString)[:10]

    return getInstallFromServer(appName, startDate, finishdate)


def flushDatastore():
    ndb.delete_multi(
        install.query().fetch(keys_only=True)
    )
    return True


def getInstallData():
    rootdir = 'application/static/installcom/six/'
    list = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if (file != '.DS_Store'):
                res = os.path.join(subdir, file)
                list.append(res)
                logging.debug(res)

    for entry in list:
        t = threading.Thread(target=target1(entry))
        t.start()


def target1(filename):
    f = open(filename)
    stream = io.StringIO(f.read().decode("UTF16"), newline=None)
    csv_input = csv.reader(stream)
    flag = False
    for row in csv_input:
        logging.debug(row)
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


def getCrashesData():
    rootdir = 'application/static/crash/'
    list = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if (file != '.DS_Store'):
                res = os.path.join(subdir, file)
                list.append(res)
                print res

    for entry in list:
        t = threading.Thread(target=target2(entry))
        t.start()


def target2(filename):
    f = open(filename)
    stream = io.StringIO(f.read().decode("UTF16"), newline=None)
    csv_input = csv.reader(stream)
    flag = False
    for row in csv_input:
        print row
        if (not (flag)):
            flag = True
        else:
            info = {'date': row[0], 'appName': row[1], 'dailyCrashes': int(row[2]), 'dailyANRs': int(row[3])}
            primitiveCrashUlpoad(info)
    f.close()


def uploadCrash(info):
    new_crash = crash()
    new_crash.date = info["date"]
    new_crash.appName = info["appName"]
    new_crash.dailyCrashes = info["dailyCrashes"]
    new_crash.dailyANRs = info["dailyANRs"]

    new_crash.year = int(info['date'][:4])
    new_crash.month = int(info['date'][5:7])
    new_crash.day = int(info['date'][-2:])

    new_crash.intDate = new_crash.getIntDate()
    new_crash.put()


class crash(ndb.Model):
    date = ndb.StringProperty()
    appName = ndb.StringProperty()
    dailyCrashes = ndb.IntegerProperty()
    dailyANRs = ndb.IntegerProperty()
    day = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    intDate = ndb.IntegerProperty()

    def getIntDate(self):
        str1 = self.date[:4] + self.date[5:7] + self.date[-2:]
        return int(str1)


def getCrashFromServer(appName, dateStartWith, dateEndsWith):
    date1 = int(dateStartWith[:4] + dateStartWith[5:7] + dateStartWith[-2:])
    date2 = int(dateEndsWith[:4] + dateEndsWith[5:7] + dateEndsWith[-2:])

    qry = crash.query(crash.appName == appName, crash.intDate >= date1, crash.intDate <= date2)
    res = qry.fetch()
    res = sorted(res, cmp=numeric_compare)
    return res


def getCrashFromServerParam(appName, param):
    today = datetime.datetime.now()
    day = datetime.timedelta(days=1)
    datetoString = today - day

    switch = {
        'oneM': relativedelta(months=1),
        'threeM': relativedelta(months=3),
        'sixM': relativedelta(months=6),
        'twelveM': relativedelta(months=12),
        'allTime': relativedelta(months=72)
    }

    start = datetoString - switch[param]

    startDate = str(start)[:10]
    finishdate = str(datetoString)[:10]

    return getCrashFromServer(appName, startDate, finishdate)


def checkIfCrashExist(info):
    qry = crash.query(install.appName == info["appName"], install.date == info["date"])
    res = qry.fetch()
    if len(res) == 0:
        return False
    return True


def primitiveCrashUlpoad(info):
    if not (checkIfCrashExist(info)):
        uploadCrash(info)


def forceCrashUpload(info):
    uploadCrash(info)


def getRatesData():
    rootdir = 'application/static/rate/fst'
    list = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if (file != '.DS_Store'):
                res = os.path.join(subdir, file)
                list.append(res)
                print res

    for entry in list:
        t = threading.Thread(target=target3(entry))
        t.start()


def target3(filename):
    f = open(filename)
    stream = io.StringIO(f.read().decode("UTF16"), newline=None)
    csv_input = csv.reader(stream)
    flag = False
    for row in csv_input:
        print row
        if (not (flag)):
            flag = True
        else:
            info = {'date': row[0], 'appName': row[1], 'dailyR': row[2], 'totalR': row[3]}
            primitiveRateUpload(info)
    f.close()


def uploadRate(info):
    new_rate = rate()
    new_rate.date = info["date"]
    new_rate.appName = info["appName"]
    if (info["dailyR"] == 'NA'):
        new_rate.dailyR = 0
    else:
        new_rate.dailyR = float(info["dailyR"])
    if (info["totalR"] == 'NA'):
        new_rate.totalR = 0
    else:
        new_rate.totalR = float(info["totalR"])

    new_rate.year = int(info['date'][:4])
    new_rate.month = int(info['date'][5:7])
    new_rate.day = int(info['date'][-2:])

    new_rate.intDate = new_rate.getIntDate()

    new_rate.put()


class rate(ndb.Model):
    date = ndb.StringProperty()
    appName = ndb.StringProperty()

    dailyR = ndb.FloatProperty()
    totalR = ndb.FloatProperty()

    day = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    intDate = ndb.IntegerProperty()

    def getIntDate(self):
        str1 = self.date[:4] + self.date[5:7] + self.date[-2:]
        return int(str1)


def getRateFromServer(appName, dateStartWith, dateEndsWith):
    date1 = int(dateStartWith[:4] + dateStartWith[5:7] + dateStartWith[-2:])
    date2 = int(dateEndsWith[:4] + dateEndsWith[5:7] + dateEndsWith[-2:])

    qry = rate.query(rate.appName == appName, rate.intDate >= date1, rate.intDate <= date2)
    res = qry.fetch()
    res = sorted(res, cmp=numeric_compare)
    return res


def getRateFromServerParam(appName, param):
    today = datetime.datetime.now()
    day = datetime.timedelta(days=1)
    datetoString = today - day

    switch = {
        'oneM': relativedelta(months=1),
        'threeM': relativedelta(months=3),
        'sixM': relativedelta(months=6),
        'twelveM': relativedelta(months=12),
        'allTime': relativedelta(months=72)
    }

    start = datetoString - switch[param]

    startDate = str(start)[:10]
    finishdate = str(datetoString)[:10]

    return getRateFromServer(appName, startDate, finishdate)


def checkIfRateExist(info):
    qry = rate.query(rate.appName == info["appName"], rate.date == info["date"])
    res = qry.fetch()
    if len(res) == 0:
        return False
    return True


def primitiveRateUpload(info):
    if not (checkIfRateExist(info)):
        uploadRate(info)


def forceRateUpload(info):
    uploadRate(info)


def getRatesList(rates, param):
    newList = []
    for ra in rates:
        switch = {
            'date': ra.date,
            'dailyR': ra.dailyR,
            'totalR': ra.totalR
        }
        newList.append(switch[param])
    return newList
