from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# 初始化数据库
db = SQLAlchemy()

# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user' 或 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    consumption = db.Column(db.Float, nullable=False, default = 0)
    vip = db.Column(db.Integer,default = 0)
    address = db.relationship('Address', backref='user', lazy=True ,cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)

# 花卉表
class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(255))  # 多标签用逗号分隔
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sales = db.Column(db.Integer, default=0) #销售量
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=True)#活动id
    promotion = db.relationship('Promotion', backref='flower', lazy=True)

# 购物车表
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flower_id = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    flower = db.relationship('Flower', backref='cart', lazy=True)

# 订单表
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'shipped', 'completed',"canceled"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

# 订单详情表
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    flower_id = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    discount = db.Column(db.Float, nullable=False)  # 折扣率
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    tags = db.Column(db.String(255))  # 多标签用逗号分隔
    description = db.Column(db.Text)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    is_default = db.Column(db.Integer, default= 0 )

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), db.ForeignKey('user.id'), nullable=True)
    operation = db.Column(db.String(50), nullable=True) # 增删改查，系统自动
    detail = db.Column(db.String(155), nullable=True)
    operation_time = db.Column(db.DateTime, default=datetime.now())
    user = db.relationship('User', backref='logs')
