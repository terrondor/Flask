from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = "wewqwe1231e1r3er2tr24t34t34tg54g45htgergfds"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Пост успешно создан!", "success")
        return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы изменить пост!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("Пост успешно изменен!", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", post=post)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Вы не авторизованы чтобы удалить пост.", "danger")
        return redirect(url_for("index"))

    db.session.delete(post)
    db.session.commit()
    flash("Пост успешно удален!", "success")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация успешна! Теперь вы можете войти.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Успешный вход!", "success")
            return redirect(url_for("index"))
        else:
            flash("Ошибка. Проверьте имя и пароль.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():  # Создаем контекст приложения
        db.create_all()  # Создает базу данных
    app.run(debug=True)
