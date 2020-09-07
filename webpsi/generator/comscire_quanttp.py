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

import os

import websocket

from webpsi.generator.base import Generator


class ComScireQuanttp(Generator, id='comscire_quanttp', bit_numbering=Generator.BitNumbering.LSB0):
    def __init__(self):
        self._ws = websocket.WebSocket()
        self._ws.connect('ws://%s/ws' % os.environ['QUANTTP_LOCATION'])

    def get_bytes(self, length: int) -> bytes:
        self._ws.send('CLEAR')
        self._ws.send('RANDBYTES %d' % length)
        return self._ws.recv()
