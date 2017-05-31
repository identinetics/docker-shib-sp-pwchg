import os
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException
from jinja2 import Environment, FileSystemLoader
from session import SessionStore
import pprint


class WzServer(object):
    def __init__(self):
        self.session_store = SessionStore()
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)
        self.url_map = None

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def save_session_data(self,request, response):
        if request.session.should_save:
            self.session_store.save(request.session)
            response.set_cookie("session_id", request.session.sid)
        return
