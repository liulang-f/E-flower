from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from .utils.redisU import start_redis
from .models import db
from .routes.auth_routes import auth_bp, jwt
from .routes.flower_routes import flower_bp
from .routes.cart_routes import cart_bp
from .routes.order_routes import order_bp
from .routes.admin_routes import admin_bp
from .routes.promotion_routes import promotion_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.static_folder = 'static'
    app.config['STATIC_FOLDER'] = Config.STATIC_FOLDER
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    start_redis()

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(flower_bp, url_prefix='/flower')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(promotion_bp, url_prefix='/promotion')

    return app