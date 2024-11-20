from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
import os


db = SQLAlchemy()
mail = Mail()  # Initialize Flask-Mail globally
migrate = Migrate()  # Initialize Flask-Migrate
DB_NAME = "travel.db"

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SECRET_KEY'] = 'safardarshan'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # File upload configurations
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Import blueprints
    from .view import views
    from .auth import auth
    from .admin import admin

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Import models
    from .models import Users, Places, City, Hotel, Restaurant, Favorite

    # Create the database if it doesn't exist
    create_database(app)

    # Initialize Flask-Login
    login_manager.login_view = 'auth.login'  

    # Flask-Login user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))  # Query user by ID

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'info@safardarshan.com'
    app.config['MAIL_PASSWORD'] = 'Safar@12345'   
    app.config['MAIL_DEFAULT_SENDER'] = '{{current_user.email}}'

    # Initialize Flask-Mail
    mail.init_app(app)

    # Utility to check if an item is favorited
    @app.context_processor
    def utility_processor():
        def is_favorited(item_id, category):
            if not current_user.is_authenticated:
                return False
            # Check if the item is in favorites
            return Favorite.query.filter_by(user_id=current_user.id, item_id=item_id, category=category).first() is not None

        return dict(is_favorited=is_favorited)


    return app

# Utility to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def create_database(app):
    if not os.path.exists(f'instance/{DB_NAME}'):  
        with app.app_context(): 
            db.create_all()
            print('Database created')
