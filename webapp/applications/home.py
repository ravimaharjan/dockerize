from flask import Blueprint, render_template, url_for
from flask_login import login_required

home_app = Blueprint("home_app", __name__,template_folder="../templates")

@login_required
@home_app.route("/", methods=['GET'])
@home_app.route("/index", methods=['GET'])
def index():
    user = {'username': 'FlaskUser'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Today is a beautify sunny day outside!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
