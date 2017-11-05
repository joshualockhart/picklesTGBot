from tinydb import TinyDB, Query
from tinydb.operations import delete
import config

class DuplicateKeyError(Exception): pass
db = TinyDB(config.SESSION_DB_FILENAME)

class SessionDBHandler():
    def __init__(self):
        self.db = db

    def get_sessions_for_user_id(self, user_id):
        Session = Query()
        return self.db.search(Session.user_id == user_id)

    def update_session(self, user_id, sheet_id):
        sessions = self.get_sessions_for_user_id(user_id)
        if len(sessions) == 0:
            self.db.insert({'user_id':user_id, 'current_sheet_id':sheet_id})
        else:
            User = Query()
            self.db.update({'current_sheet_id':sheet_id}, User.user_id==user_id)

class Session():
    def __init__(self, user_id):
        self.dbh = SessionDBHandler()
        sessions = self.dbh.get_sessions_for_user_id(user_id)

        if len(sessions) == 0:
            self.current_sheet_id = None
        elif len(sessions) == 1:
            self.current_sheet_id = sessions[0]['current_sheet_id']
        else:
            raise DuplicateKeyError("Multiple sessions in DB for user with id '{}'".format(user_id))

        self.user_id = user_id

    def set_sheet_id(self, sheet_id):
        self.current_sheet_id = sheet_id

    def get_current_sheet_id():
        return self.current_sheet_id

    def commit(self):
        self.dbh.update_session(self.user_id, self.current_sheet_id)

