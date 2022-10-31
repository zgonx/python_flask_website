from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST', ])
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST', ])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Your email is too short!', category='error')
        elif len(firstName) < 2:
            flash('Your name is too short!', category='error')
        elif password1 != password2:
            flash('Your passwords don\'t match!', category='error')
        elif len(password1) < 8:
            flash('Your password must be at least 8 char !', category='error')
        else:
            flash('Account created!', category='success')

    return render_template("sign_up.html")
