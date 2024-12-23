from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from models import User, Post 
from backend.database import db


main = Blueprint("main", __name__)


@main.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@main.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Пост успешно создан!", "success")
        return redirect(url_for("main.index"))
    return render_template("create.html")


@main.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы изменить пост!", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("Пост успешно изменен!", "success")
        return redirect(url_for("main.index"))
    return render_template("edit.html", post=post)


@main.route("/delete/<int:id>")
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы удалить пост.", "danger")
        return redirect(url_for("main.index"))

    db.session.delete(post)
    db.session.commit()
    flash("Пост успешно удален!", "success")
    return redirect(url_for("main.index"))


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация успешна! Теперь вы можете войти.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Успешный вход!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Ошибка. Проверьте имя и пароль.", "danger")
    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли.", "success")
    return redirect(url_for("main.index"))
