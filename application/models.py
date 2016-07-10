import csv
import io
import logging
import os
import threading

from google.appengine.ext import ndb

from werkzeug.security import generate_password_hash, check_password_hash

tkey = ndb.Key('user', 'newUser')


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
    if not (validate(info)):
        return False
    newUser = user()
    newUser.username = info["login"]
    newUser.set_password(info["password"])
    newUser.email = info["email"]
    newUser.appName = info["appName"]
    newUser.put()
    return True


def validate(info):
    if (checkIfAlreadyExists(info)):
        return False
    if (len(info["login"]) < 2) or len(info["password"]) < 6 or len(info["email"]) < 5:
        return False
    return True


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
        return True
    qry = user.query(user.email == info["email"])
    res = qry.fetch(1)
    if (len(res) != 0):
        return True
    return False


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


def getInstallWithParam(installist, param):
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


def primitiveUlpoadOnServer(info):
    if not (checkIfAlreadyOnServer(info)):
        uploadOnServer(info)


def checkIfAlreadyOnServer(info):
    qry = install.query(install.appName == info["appName"], install.date == info["date"],
                        install.curDevInst == int(info["curDevInst"]))
    res = qry.fetch()
    logging.debug(res)
    if len(res) == 0:
        return False
    return True


def forceUploadOnServer(info):
    uploadOnServer(info)


def uploadOnServer(info):
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


def flushDatastore():
    ndb.delete_multi(
        install.query().fetch(keys_only=True)
    )
    return True


def getData():
    rootdir = 'application/static/installcom/fst/'
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
