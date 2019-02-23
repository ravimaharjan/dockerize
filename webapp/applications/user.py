from webapp.applications import *
from webapp.forms.login_form import LoginForm
from webapp.forms.register_form import RegisterForm
from webapp.models import User
from db_provider import db
from flask_login import current_user, login_user, logout_user, login_required

user_app = Blueprint("user_app", __name__, template_folder='../templates')

@user_app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('home_app.index'))

        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        print user
        if user:
            flash("Login Successful for user {0}, remember_me {1}".format(
            form.username.data, form.remember_me.data))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home_app.index'))
        else:
            flash('Invalid username or password')
            render_template('login.html', form=form) 
    return render_template('login.html', form=form)

@login_required
@user_app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print request.form
    if form.validate_on_submit():
        new_user = User(
            username=request.form['username'], 
            email=request.form['email'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

@login_required
@user_app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home_app.index'))

