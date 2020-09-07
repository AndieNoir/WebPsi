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

from webpsi.generator.base import Generator


class ComScireLocal(Generator, id='comscire_local', bit_numbering=Generator.BitNumbering.LSB0):
    def __init__(self):
        self._os_windows = os.name == 'nt'
        if self._os_windows:
            import win32com.client
            self._qng = win32com.client.Dispatch('QWQNG.QNG')
        else:
            import ctypes
            import platform
            self._qwqng_wrapper = ctypes.cdll.LoadLibrary('./libqwqng-wrapper-x86-64.so' if platform.machine().endswith('64') else './libqwqng-wrapper.so')
            self._qwqng_wrapper.GetQwqngInstance.restype = ctypes.c_void_p
            self._qwqng_wrapper.RandBytes.argtypes = [ctypes.c_void_p, ctypes.c_int]
            self._qwqng_wrapper.RandBytes.restype = ctypes.POINTER(ctypes.c_char)
            self._qwqng_wrapper.Clear.argtypes = [ctypes.c_void_p]
            self._qng_pointer = self._qwqng_wrapper.GetQwqngInstance()

    def get_bytes(self, length: int) -> bytes:
        return self._get_bytes_windows(length) if self._os_windows else self._get_bytes_linux(length)

    def _get_bytes_windows(self, length: int) -> bytes:
        self._qng.Clear()
        if length <= 8192:
            return bytes(self._qng.RandBytes(length))
        else:
            data = bytearray()
            for x in range(length // 8192):
                data.extend(bytearray(self._qng.RandBytes(8192)))
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(bytearray(self._qng.RandBytes(bytes_needed)))
            return bytes(data)

    def _get_bytes_linux(self, length: int) -> bytes:
        self._qwqng_wrapper.Clear(self._qng_pointer)
        if length <= 8192:
            return self._qwqng_wrapper.RandBytes(self._qng_pointer, length)[:length]
        else:
            data = bytearray()
            for x in range(length // 8192):
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, 8192)[:8192])
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, bytes_needed)[:bytes_needed])
            return bytes(data)
