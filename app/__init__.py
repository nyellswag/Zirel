from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import click
from sqlalchemy import event
from sqlalchemy.engine import Engine

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Please log in to access your projects."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return db.session.get(User, int(user_id))


@event.listens_for(Engine, "connect")
def configure_sqlite_connection(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__ != "sqlite3":
        return

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=TRUNCATE")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=15000")
    cursor.close()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import main

    app.register_blueprint(main)
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    @app.cli.command("create-admin")
    def create_admin():
        """Create or promote the first admin user from environment variables."""
        import os

        from app.models import User

        username = os.environ.get("ADMIN_USERNAME", "").strip()
        email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
        password = os.environ.get("ADMIN_PASSWORD", "")

        if not username or not email or not password:
            raise click.ClickException(
                "Set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD before running this command."
            )

        user = User.query.filter_by(email=email).first()
        if user:
            user.username = user.username or username
            user.is_admin = True
            if password:
                user.set_password(password)
            db.session.commit()
            click.echo(f"Updated admin user: {email}")
            return

        if User.query.filter_by(username=username).first():
            raise click.ClickException(
                "ADMIN_USERNAME is already used by another account. Choose another username."
            )

        user = User(username=username, email=email, role="Other", is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created admin user: {email}")
