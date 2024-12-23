from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from forms.forms import LoginForm, RegistrationForm
from models.models import User
from backend.database import db


user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.", "danger")
            return redirect(url_for("user.register"))
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация успешна! Теперь вы можете войти.", "success")
        return redirect(url_for("user.login"))
    return render_template("register.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Успешный вход!", "success")
            return redirect(url_for("post.index"))
        else:
            flash("Ошибка. Проверьте имя и пароль.", "danger")
    return render_template("login.html", form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли.", "success")
    return redirect(url_for("post.index"))
