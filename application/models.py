from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, \
    check_password_hash
from google.appengine.ext.db import stats

tkey = ndb.Key('user', 'newUser')


class user(ndb.Model):
    userid = ndb.IntegerProperty()
    username = ndb.StringProperty()
    pw_hash = ndb.StringProperty()
    email = ndb.StringProperty()
    appName=ndb.StringProperty()

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


def addUser(info):
    if (checkIfAlreadyExists(info)):
        return False
    newUser = user()
    newUser.username=info["login"]
    newUser.set_password(info["password"])
    newUser.userid = info["userid"]
    newUser.email = info["email"]
    newUser.put()
    return True


def checkLogin(_name, _pass):

    qry = user.query(user.username == _name)
    #delete
    print _name

    res = qry.fetch(1)
    #delete pls
    print res
    print res[0].check_password(_pass)
    print generate_password_hash(_pass)
    print res[0].pw_hash

    if len(res) == 0:
        return False

    elif res[0].check_password(str(_pass)):
        return True
    else:
        return False


def checkIfAlreadyExists(info):
    qry = user.query(user.username == info["login"])
    res = qry.fetch(1)
    print res
    if (len(res) != 0):
        return True
    qry = user.query(user.email == info["email"])
    res = qry.fetch(1)
    if (len(res) != 0):
        return True
    return False
