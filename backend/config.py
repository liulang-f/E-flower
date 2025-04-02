import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 禁用 Flask SQLAlchemy 的事件系统以提升性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 从 .env 文件获取 SECRET_KEY，如果没有设置则使用默认值
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    # 从 .env 文件获取数据库连接 URI，默认值为 mysql://root:password@localhost/flower_shop
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:password@localhost/flower_shop')

    # 可选配置：配置 Flask-JWT-Extended
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')  # JWT 密钥
    #JWT黑名单
    JWT_BLACKLIST_ENABLED = True

    STATIC_FOLDER = 'static'