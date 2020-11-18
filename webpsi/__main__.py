# Copyright (C) 2020 AndieNoir
#
# WebPsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebPsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with WebPsi.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask
from flask_breadcrumbs import Breadcrumbs, default_breadcrumb_root
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from webpsi.views import home, classic_reg, singlebit_pk


app = Flask(__name__)
sockets = Sockets(app)

Breadcrumbs(app)
default_breadcrumb_root(home.blueprint, '.')

app.register_blueprint(home.blueprint)

app.register_blueprint(classic_reg.blueprint, url_prefix='/classic_reg')
sockets.register_blueprint(classic_reg.ws_blueprint, url_prefix='/classic_reg')

app.register_blueprint(singlebit_pk.blueprint, url_prefix='/singlebit_pk')
sockets.register_blueprint(singlebit_pk.ws_blueprint, url_prefix='/singlebit_pk')

server = pywsgi.WSGIServer(('0.0.0.0', 58700), application=app, handler_class=WebSocketHandler)
server.serve_forever()

app.run(host='0.0.0.0', port=58700)
