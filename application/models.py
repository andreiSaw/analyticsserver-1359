from google.appengine.ext import ndb
from google.appengine.ext.db import stats

tkey = ndb.Key('user', 'newUser')


class user(ndb.Model):
    userid = ndb.IntegerProperty()
    login = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()


def addUser(info):
    if (checkIfAlreadyExists(info)):
        return False
    newUser = user(parent=tkey)
    newUser.userid = info["userid"]
    newUser.login = info["login"]
    newUser.email = info["email"]
    newUser.password = info["password"]
    newUser.put()
    return True


def checkLogin(_name, _pass):
    qry = user.query(user.login == _name)
    print _name

    res = qry.fetch(1)
    print res

    if len(res) == 0:
        return False

    elif str(res[0].password) == str(_pass):
        return True
    else:
        return False


def checkIfAlreadyExists(info):
    qry = None
    qry = user.query(user.login == info["login"])
    res= qry.fetch(1)
    print res
    if (len(res) != 0):
        return True
    qry = user.query(user.email == info["email"])
    res = qry.fetch(1)
    if (len(res) != 0):
        return True
    return False
