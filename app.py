from flask_login import login_required

from factory import create_app

app = create_app()


@app.route('/admin')
@login_required
def admin():
    return 'Welcome to admin page. You must be a PersonalWebApp user.'
