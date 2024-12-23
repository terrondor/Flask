from flask import Flask
from flask_login import LoginManager
from backend.database import db
from routers.routers import main
from models import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = "wewqwe1231e1r3er2tr24t34t34tg54g45htgergfds"
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "main.login"
app.register_blueprint(main)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
