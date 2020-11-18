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

from enum import Enum


class Generator:

    class BitNumbering(Enum):
        LSB0 = 'lsb0'
        MSB0 = 'msb0'
        UNKNOWN = 'unknown'

    def __init_subclass__(cls, id: str, bit_numbering: BitNumbering, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = id
        cls.bit_numbering = bit_numbering

    def get_bytes(self, length: int) -> bytes:
        pass
