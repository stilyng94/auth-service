import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('auth_service.config.config.DevConfig')

    print(app.secret_key)

# Handle proxy server headers
    if os.getenv("APP_CONFIG") == "auth_service.config.config.ProductionConfig":
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

    if test_config is not None:
        app.config.update(test_config)

    # extension init
    from .extension.db import db
    from .extension.f_session import f_session
    db.init_app(app)
    f_session.init_app(app)

    with app.app_context():
        # create tables
        from .models.user_model import UserModel
        db.create_all()

        # routes and blueprints
        from .blueprints.auth.routes import auth_bp
        app.register_blueprint(auth_bp)

        @app.route('/')
        def home():
            return {'success': True}, 200

        return app
