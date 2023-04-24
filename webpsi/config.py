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

import os

from webpsi.generator.comscire_local import ComScireLocal
from webpsi.generator.comscire_quanttp import ComScireQuanttp
from webpsi.generator.rndo_comscire import Randonautica_QRNG


GENERATOR_CLASS = ComScireQuanttp if ('QUANTTP_LOCATION' in os.environ) else ComScireLocal