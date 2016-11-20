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


@simple_routes.route('/access_pattern')
@login_required
def access_pattern():
    """Generate access pattern using Visitors."""
    cmd = '/home/ubuntu//visitors_0.7/visitors /home/ubuntu/personalwebapp/logs/nginx/access.log --prefix 66.65.39.198 --graphviz > /home/ubuntu/personalwebapp/instance/graph.dot'
    subprocess.call(cmd, shell=True)
    cmd = 'dot /home/ubuntu/personalwebapp/instance/graph.dot -Tpng > /home/ubuntu/personalwebapp/instance/access_pattern.png'
    subprocess.call(cmd, shell=True)
    return send_file('instance/access_pattern.png')


@simple_routes.route('/dump_database')
@login_required
def dump_database():
    """Serve app.db file for backup."""
    return send_file('app.db', as_attachment=True)
