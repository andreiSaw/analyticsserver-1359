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
    print _name

    res = qry.fetch(1)
    # delete pls
    print res

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


class BlobIterator:
    """Because the python csv module doesn't like strange newline chars and
    the google blob reader cannot be told to open in universal mode, then
    we need to read blocks of the blob and 'fix' the newlines as we go"""

    def __init__(self, blob_reader):
        self.blob_reader = blob_reader
        self.last_line = ""
        self.line_num = 0
        self.lines = []
        self.buffer = None

    def __iter__(self):
        return self

    def next(self):
        if not self.buffer or len(self.lines) == self.line_num + 1:
            self.buffer = self.blob_reader.read(1048576)  # 1MB buffer
            self.lines = self.buffer.splitlines()
            self.line_num = 0

            # Handle special case where our block just happens to end on a new line
            if self.buffer[-1:] == "\n" or self.buffer[-1:] == "\r":
                self.lines.append("")

        if not self.buffer:
            raise StopIteration

        if self.line_num == 0 and len(self.last_line) > 0:
            result = self.last_line + self.lines[self.line_num] + "\n"
        else:
            result = self.lines[self.line_num] + "\n"

        self.last_line = self.lines[self.line_num + 1]
        self.line_num += 1

        return result


def upload_data():
    r = requests.get('https://www.google.com/images/srpr/logo11w.png')
    with open('google_logo.png', 'wb') as f:
        f.write(r.content)
