from flask import Blueprint
from flask_login import login_required

simple_routes = Blueprint('simple_routes', __name__)


@simple_routes.route('/admin')
@login_required
def admin():
    return 'Welcome to admin page. You must be a PersonalWebApp user.'
