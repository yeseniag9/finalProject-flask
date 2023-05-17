from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user) 
            db.session.commit()  

            return redirect(url_for('site.home'))
    except: 
        raise Exception('Invalid form data; please check your form.')
    return render_template('register.html', form = form)

@auth.route('/login', methods = ['GET', 'POST']) 
def login():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password): 
                login_user(logged_user)
                return redirect(url_for('site.profile'))
            else:
                return redirect(url_for('auth.login')) 
    except:
        raise Exception('Invalid form data; please check your form.')
    return render_template('login.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))