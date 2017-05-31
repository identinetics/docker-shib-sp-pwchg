import os
from werkzeug.routing import Map, Rule
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.exceptions import abort
from ldap import LDAPConnection
from config import Config
from password import Password, PasswordTooShortException
from tools import Log, randomword
from wzserver import WzServer
import pprint
from werkzeug.wrappers import Response

class PwChangeServer(WzServer):
    def __init__(self):

        super(PwChangeServer, self).__init__()

        self.url_map = Map([
            Rule('/change.html', endpoint='change'),
            Rule('/final.html', endpoint='final'),
        ])

        config = Config()
        try:
            print ("trying to connect LDAP server")
            self.ldap = LDAPConnection(config)
        except Exception as e:
            msg = "Error connecting LDAP on {}: {}".format(config.server, e)
            print(msg)
            exit(-1)

    def _test_username_password(self, user_dn, password):
        pw = Password()
        pw.set_password(password, checks=False)
        authenticated = self.ldap.test_userdn_password(userdn=user_dn, password=str(pw))
        if authenticated:
            return True
        return False

    def _put_the_user_session_in_the_request(self, request):
        sid = request.cookies.get("session_id")
        the_session = self.session_store.get_or_new(sid)
        request.session = the_session
        return

    def _ldap_filter_from_request(self, request):
        #pprint.pprint(request.environ)
        user_id = request.environ['shib_uid']
        print("searching for: {}".format(user_id))
        from ldap import LDAPFilter
        f = LDAPFilter()
        f.add_filter('uid', user_id)
        return (f)

    def on_change(self, request):
        print ("on_change")
        error = None
        self._put_the_user_session_in_the_request(request)

        errors = []
        if request.method == 'POST':
            session_csrf = request.session['_csrf_token']
            form_csrf = request.form['csrf_token']
            if session_csrf != form_csrf:
                Log.logline(request, "somebody tries CSRF")
                abort(403)

            try:
                old_pw = request.form['j_oldpassword']
                pw1 = request.form['j_password1']
                pw2 = request.form['j_password2']
                if pw1 != pw2:
                    errors.append("Die eingegebenen Passwörter sind unterschiedlich.")

                ldap_filter = self._ldap_filter_from_request(request)

                # note: we do not catch exceptions here.
                # They should never happen
                user_dn = self.ldap.search_user(ldap_filter)

                if not self._test_username_password(user_dn, old_pw):
                    errors.append("Sie haben Ihr Passwort nicht richtig eingegeben.")
                    Log.logline(request, "pw change error: old password incorrect")

                if not errors:

                    new_password = Password(pw1)
                    self.ldap.change_password(user_dn, str(new_password))
                    Log.logline(request, "pw change success")
        
                    t_html = "/secure/wsgi/pwchanger.wsgi/final.html"
                    t_host = request.environ['SERVER_NAME']
                    final_target = "https://{}:{}".format(t_host,t_html)
                    print("redirect to:{}".format(final_target))

                    response = redirect(final_target)
                    return response


            except PasswordTooShortException:
                errors.append("Das Passwort muss mindestens 8 Zeichen lang sein.")

        request.session['_csrf_token'] = randomword(8)
        if errors:
            error = ", ".join(errors)

        response = self.render_template('change.html', error=error, csrf_token=request.session['_csrf_token'])

        self.save_session_data(request, response)

        return response

    def on_final(self, request):
        print ("on_final")
        sid = request.cookies.get("session_id")
        try:
            request.session = self.session_store.get(sid)
        except TypeError:
            # todo: log: somebody tried to bypass the login
            abort(403)

        response = self.render_template('takeoff.html')
        return response


def create_app():
    app = PwChangeServer()
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static': os.path.join(os.path.dirname(__file__), 'static')
    })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
