from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import Registration, Login, UpdateAccountForm, UpdateAccountPassword, RequestResetForm, ResetPasswordForm
from main.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/registr", methods=['GET', 'POST'])
def registr():
    posts = Post.query.order_by(Post.data_posted.desc()).paginate(per_page=4)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_psw)
        db.session.add(user)
        db.session.commit()
        flash(f"Your acount has been created! You are now able to log in.",
              'success')
        return redirect(url_for("users.login"))

    return render_template("registr.html",
                           title="Registr",
                           posts=posts,
                           form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    PAGE = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_posted.desc()).paginate(per_page=4,
                                                                  page=PAGE)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember_psw.data)
            next_page = request.args.get('next', '/main.home')[1:]

            return redirect(url_for(next_page)) if next_page else redirect(
                url_for("main.home"))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    return render_template('login.html', title='Login', posts=posts, form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account has been updated!", 'success')
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title="My Account",
                           image_file=image_file,
                           form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.data_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to rest your password!',
            "success")
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_psw
        db.session.commit()
        flash(f"Your password has been changed! You are now able to log in.",
              'success')
        return redirect(url_for("users.login"))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form,
                           image_file=image_file)


@users.route("/change", methods=['GET', 'POST'])
@login_required
def change():
    form = UpdateAccountPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password,
                                               form.previous_password.data):
            hashed_psw = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = hashed_psw
            print(user.password)
            db.session.commit()
            flash(f"Your password has been updated!", 'success')
            return redirect(url_for("users.account"))
        else:
            flash('The password is uncorrect!', 'danger')
    return render_template("change_password_page.html",
                           title='Change Password Page',
                           form=form)