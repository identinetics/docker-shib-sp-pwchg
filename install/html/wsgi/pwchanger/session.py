from werkzeug.contrib.sessions import FilesystemSessionStore
import tempfile


class SessionStore(object):
    path = tempfile.gettempdir()
    session_store = FilesystemSessionStore(path)

    def new(self):
        session = self.session_store.new()
        return session

    def get(self,sid):
        session = self.session_store.get(sid)
        return session

    def get_or_new(self,sid):
        if sid is None:
            return self.new()
        else:
            return self.get(sid)

    def save(self,session):
        self.session_store.save(session)
