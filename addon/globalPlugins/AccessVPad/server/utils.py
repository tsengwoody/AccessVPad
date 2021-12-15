from os import path

from jinja2 import Environment, FileSystemLoader
from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule
from werkzeug.urls import url_parse
from werkzeug.utils import cached_property
from werkzeug.wrappers import Response

APP_PATH = path.join(path.dirname(__file__), "app")
TEMPLATES_PATH = path.join(path.dirname(__file__), "templates")

env = Environment(
	loader=FileSystemLoader(TEMPLATES_PATH),
	variable_start_string='{|{',
	variable_end_string='}|}'
)

ALLOWED_SCHEMES = frozenset(["http", "https", "ftp", "ftps"])
URL_CHARS = "abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789"

local = Local()
local_manager = LocalManager([local])
application = local("application")

url_map = Map([
	Rule("/app/<file>", endpoint="app", build_only=True),
])

def expose(rule, **kw):
	def decorate(f):
		kw["endpoint"] = f.__name__
		url_map.add(Rule(rule, **kw))
		return f

	return decorate


def url_for(endpoint, _external=False, **values):
	return local.url_adapter.build(endpoint, values, force_external=_external)


def render_template(template, **context):
	template = env.get_template(template)
	content = template.render(context)
	return Response(
		content, mimetype="text/html"
	)

def validate_url(url):
	return url_parse(url)[0] in ALLOWED_SCHEMES
