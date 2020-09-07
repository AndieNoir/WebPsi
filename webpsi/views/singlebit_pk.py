# Copyright (C) 2020 AndieNoir
#
# WebPsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebPsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebPsi.  If not, see <https://www.gnu.org/licenses/>.

import base64
import secrets

from flask import Blueprint, render_template, request
from flask_breadcrumbs import register_breadcrumb
from geventwebsocket.websocket import WebSocket

from webpsi.utils import *


_BYTES_PER_TRIAL = 125

blueprint = Blueprint('singlebit_pk', __name__)
ws_blueprint = Blueprint('singlebit_pk_ws', __name__)

create_logs_dir_if_not_exist()
_log_file = open('logs/singlebit_pk.csv', 'a')
if os.stat('logs/singlebit_pk.csv').st_size == 0:
    _log_file.write('dt,ip_address,session_id,hit,raw_data,generator_id,generator_bit_numbering\n')
    _log_file.flush()

_generator = get_generator_instance()

_valid_session_ids = []


@blueprint.route('/')
@register_breadcrumb(blueprint, '.', 'Single-Bit PK Game')
def singlebit_pk():
    return render_template('singlebit_pk.html')


@blueprint.route('/api/session_id')
def generate_session_id():
    session_id = secrets.token_bytes(4).hex()
    _valid_session_ids.append(session_id)
    return session_id


@ws_blueprint.route('/ws')
def ws(websocket: WebSocket):
    while not websocket.closed:
        split_message = websocket.receive().split()
        action = split_message[0].upper()
        if action == 'RUN':
            session_id = split_message[1]
            if session_id in _valid_session_ids:
                data = _generator.get_bytes(_BYTES_PER_TRIAL)
                hit = to_bool(data, _generator.bit_numbering)
                websocket.send('HIT %d' % (1 if hit else 0))
                _log_file.write('%s,%s,%s,%.3f,%s,%s,%s' % (utc_datetime_string(), request.remote_addr, session_id, hit, str(base64.b64encode(data)), _generator.id, _generator.bit_numbering.value))
                _log_file.flush()
