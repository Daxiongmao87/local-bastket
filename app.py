import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User
from services.email_service import email_service
from config import config


def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    email_service.init_app(app)
    
    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_path, exist_ok=True)
    
    # Register blueprints (routes organized by feature as per DEVELOPMENT.md)
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.shop import shop_bp
    from routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)