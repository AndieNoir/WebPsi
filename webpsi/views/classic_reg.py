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

import secrets
import threading
import time

from flask import Blueprint, render_template, request
from flask_breadcrumbs import register_breadcrumb
from geventwebsocket.websocket import WebSocket

from webpsi.utils import *


_BYTES_PER_TRIAL = 25

blueprint = Blueprint('classic_reg', __name__)
ws_blueprint = Blueprint('classic_reg_ws', __name__)

create_logs_dir_if_not_exist()
_log_file = open('logs/classic_reg.csv', 'a')
if os.stat('logs/classic_reg.csv').st_size == 0:
    _log_file.write('dt,ip_address,run_id,trial_number,z_score,generator_id\n')
    _log_file.flush()

_generator = get_generator_instance()

_valid_run_ids = []


@blueprint.route('/')
@register_breadcrumb(blueprint, '.', 'Classic REG Experiment')
def classic_reg():
    return render_template('classic_reg.html')


@blueprint.route('/api/run_id')
def generate_run_id():
    run_id = secrets.token_bytes(4).hex()
    _valid_run_ids.append(run_id)
    return run_id


@ws_blueprint.route('/ws')
def ws(websocket: WebSocket):
    while not websocket.closed:
        split_message = websocket.receive().split()
        action = split_message[0].upper()
        if action == 'PING':
            _generator.get_bytes(_BYTES_PER_TRIAL)
            websocket.send('PONG')
        elif action == 'RUN':
            run_id = split_message[1]
            trial_count = int(split_message[2])
            if run_id in _valid_run_ids:
                threading.Thread(target=run_trials, args=(websocket, run_id, trial_count, request.remote_addr)).start()


def run_trials(websocket: WebSocket, run_id: str, trial_count: int, remote_addr: str):
    for i in range(trial_count):
        time.sleep(0.5)
        data = _generator.get_bytes(_BYTES_PER_TRIAL)
        gaussian = to_gaussian(data)
        websocket.send('GAUSSIAN %f' % gaussian)
        _log_file.write(f'{utc_datetime_string()},{remote_addr},{run_id},{i + 1},{gaussian:.3f},{_generator.id}\n')
        _log_file.flush()
    _valid_run_ids.remove(run_id)
