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

from flask import Blueprint, render_template
from flask_breadcrumbs import register_breadcrumb


blueprint = Blueprint('home', __name__)


@blueprint.route('/')
@register_breadcrumb(blueprint, '.', 'Home')
def home():
    return render_template('home.html')
