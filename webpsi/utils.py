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

import datetime
import math
import os

from webpsi.config import GENERATOR_CLASS
from webpsi.generator.base import Generator


_LOOKUP_TABLE = [
    -8, -6, -6, -4, -6, -4, -4, -2, -6, -4, -4, -2, -4, -2, -2,  0,
    -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
    -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
    -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
    -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
    -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
    -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
     0,  2,  2,  4,  2,  4,  4,  6,  2,  4,  4,  6,  4,  6,  6,  8
]

_LAST_BYTE_LOOKUP_TABLE_LSB0 = [
    -7, -5, -5, -3, -5, -3, -3, -1, -5, -3, -3, -1, -3, -1, -1,  1,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -1,  1,  1,  3,  1,  3,  3,  5,  1,  3,  3,  5,  3,  5,  5,  7,
    -7, -5, -5, -3, -5, -3, -3, -1, -5, -3, -3, -1, -3, -1, -1,  1,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
    -1,  1,  1,  3,  1,  3,  3,  5,  1,  3,  3,  5,  3,  5,  5,  7
]

_LAST_BYTE_LOOKUP_TABLE_MSB0 = [
    -7, -7, -5, -5, -5, -5, -3, -3, -5, -5, -3, -3, -3, -3, -1, -1,
    -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
    -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
    -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
    -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
    -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
    -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
     1,  1,  3,  3,  3,  3,  5,  5,  3,  3,  5,  5,  5,  5,  7,  7
]

_generator_instance = GENERATOR_CLASS()


def to_gaussian(data: bytes) -> float:
    deviation = 0
    for byte in data:
        deviation += _LOOKUP_TABLE[byte]
    return deviation / math.sqrt(len(data) * 8)


def to_bool(data: bytes, bit_numbering: Generator.BitNumbering) -> bool:
    deviation = 0
    for i in range(len(data) - 1):
        deviation += _LOOKUP_TABLE[data[i]]
    if bit_numbering == Generator.BitNumbering.MSB0:
        deviation += _LAST_BYTE_LOOKUP_TABLE_MSB0[data[-1]]
    else:
        deviation += _LAST_BYTE_LOOKUP_TABLE_LSB0[data[-1]]
    return deviation / math.sqrt(len(data) * 8 - 1) > 0


def create_logs_dir_if_not_exist():
    os.makedirs('logs', exist_ok=True)


def get_generator_instance():
    return _generator_instance


def utc_datetime_string():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
