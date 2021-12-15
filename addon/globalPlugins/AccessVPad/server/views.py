import json

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from .utils import expose, render_template

import config
import globalVars

def not_found(request):
	return render_template("not_found.html")

@expose("/app/")
def index(request):
	border = str(config.conf["AccessVPad"]["settings"]["border"]).lower()
	color = config.conf["AccessVPad"]["settings"]["color"]
	return render_template("index.html", border=border, color=color)

@expose("/api")
def api(request):
	if request.method == 'POST':
		data = json.loads(request.data)
		globalVars.rootModel.active_window['data'].pointer = data["pointer"]
		globalVars.rootModel.setFocus()

	try:
		data = [[cell.value for cell in row]for row in globalVars.rootModel.active_window['data'].data]
	except:
		data = []
	try:
		pointer = globalVars.rootModel.active_window['data'].pointer
	except:
		pointer = {}

	content = json.dumps({
		"data": data,
		"pointer": pointer,
	})
	return Response(content, mimetype="application/json")
