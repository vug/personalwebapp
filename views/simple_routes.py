"""
This Blueprint collects simple views that does not have their own Blueprint yet.
"""
import subprocess

from flask import Blueprint, render_template, send_file
from flask_login import login_required

simple_routes = Blueprint('simple_routes', __name__)


@simple_routes.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@simple_routes.route('/log_report')
@login_required
def log_report():
    """Generate a nginx log report dashboard using Goaccess.

    This is meant to be run on the EC2 instance with goaccess installed in the system PATH."""
    cmd = 'goaccess -f /home/ubuntu/personalwebapp/logs/nginx/access.log -a -o /home/ubuntu/personalwebapp/instance/report.html'
    subprocess.call(cmd, shell=True)
    return send_file('instance/report.html')
