from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.database import db
from models.models import Post

post_bp = Blueprint("post", __name__)


@post_bp.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Пост успешно создан!", "success")
        return redirect(url_for("post.index"))
    return render_template("create.html")


@post_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы изменить пост!", "danger")
        return redirect(url_for("post.index"))

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("Пост успешно изменен!", "success")
        return redirect(url_for("post.index"))
    return render_template("edit.html", post=post)


@post_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы удалить пост.", "danger")
        return redirect(url_for("post.index"))

    db.session.delete(post)
    db.session.commit()
    flash("Пост успешно удален!", "success")
    return redirect(url_for("post.index"))
