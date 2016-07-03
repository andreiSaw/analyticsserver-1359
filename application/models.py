from google.appengine.ext import ndb


class User(ndb.Model):
    """Sub model for representing an author."""
    username = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)
