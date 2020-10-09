from flask import request, render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db
from blog.models import User, BlogpPost
from blog.users.forms import LoginForm, RegisterationForm, UpdateUserForm
from blog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

@users.route('/logout')
def logout():
    logout_user()
    flash('you are logged out!')
    return redirect(url_for('core.index'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('thanks for registeration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('logged in successfully!')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)

