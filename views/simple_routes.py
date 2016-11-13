"""
This Blueprint collects simple views that does not have their own Blueprint yet.
"""
from flask import Blueprint, render_template
from flask_login import login_required

simple_routes = Blueprint('simple_routes', __name__)


@simple_routes.route('/admin')
@login_required
def admin():
    return render_template('admin.html')
