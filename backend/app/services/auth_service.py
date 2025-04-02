import redis
from PIL import Image
from flask import jsonify
from sqlalchemy import and_, desc, asc
from sympy import false
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt
from werkzeug.utils import secure_filename
from ..models import db, User, Address
from datetime import timedelta
import time
from .cart_service import get_user_carts_count
import os

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# 用户注册逻辑
def register_user(username, password, phone):
    # 检查用户名或手机号是否已存在
    user = User.query.filter((User.username == username) | (User.phone == phone)).first()
    if user:
        return {"message": "用户名或手机号已存在"}, 400

    # 创建新用户
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, phone=phone)

    try:
        # 添加并提交新用户到数据库
        db.session.add(new_user)
        db.session.commit()  # 提交事务，此时 new_user.id 会被赋值

        # 生成访问令牌
        access_token = create_access_token(identity=str(new_user.id), fresh=True, expires_delta=timedelta(days=1))
        return {"message": "注册成功", "access_token": access_token}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": f"注册失败: {str(e)}"}, 500

# 用户登录逻辑
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User.query.filter_by(phone=username).first()

    if user and check_password_hash(user.password, password):
        # 生成JWT token（包含用户ID，1天过期）
        access_token = create_access_token(identity=str(user.id), fresh=True, expires_delta=timedelta(days=1))
        if user.role == 'admin':
            return {"message": "登录成功", "access_token": access_token,"isAdmin":True}, 200
        return {"message": "登录成功", "access_token": access_token}, 200
    return {"message": "用户名或密码错误"}, 401

def logout_user():
    jti = get_jwt()["jti"]  # 获取当前 Token 的唯一标识 (JTI)
    expires_at = get_jwt()["exp"]  # Token 的过期时间（Unix 时间戳）
    current_time = int(time.time())
    expires_in = expires_at - current_time  # 剩余有效期（秒）
    if expires_in>0:
        # 将 Token 加入黑名单
        addBlack(jti, expires_in)
        return 1
    return 0

# 黑名单机制
def addBlack(jti, expires_in):
    """
    将 Token 的唯一标识 (JTI) 加入黑名单，并设置过期时间
    """
    redis_conn.set(jti, "true", ex=expires_in)

def isBlack(jti):
    """
    检查 Token 是否在黑名单中
    """
    return redis_conn.exists(jti)

def checkAuth(user_id):
    user = User.query.get(user_id)
    name = user.username
    carts = get_user_carts_count()
    isAdmin = False
    if user.role == 'admin':
        isAdmin = True
    return jsonify({"username":name,"carts":carts,"isAdmin":isAdmin}), 200

def getAuth(user_id):
    user = User.query.get(int(user_id))

    data = {
        "username": user.username,
        "phone": user.phone,
        "address": []
    }

    if user.address:
        for addr in user.address:
            address_info = {
                "id": addr.id,
                "address": addr.address,
                "is_default": addr.is_default
            }
            data["address"].append(address_info)
    return jsonify(data),200

def updateAddress(request):
    data = request.get_json()
    addrid = data.get('addrid')
    addr = data.get('addr')
    is_default = data.get('is_default')

    # 获取要更新的地址对象
    addrN = Address.query.get(addrid)
    if not addrN:
        return jsonify({"message": "地址未找到"}), 404

    # 更新地址信息
    if addr:
        addrN.address = addr

    # 如果 is_default 为 1，则将其他地址的 is_default 设为 0
    if is_default:
        addrN.is_default = 1
        # 获取当前用户的所有地址，排除当前地址
        other_addresses = Address.query.filter(
            and_(Address.user_id == addrN.user_id, Address.id != addrid)
        ).all()

        # 将其他地址的 is_default 设为 0
        for other_addr in other_addresses:
            other_addr.is_default = 0

    # 提交事务
    db.session.commit()

    return jsonify({"message": "地址已经更新"}), 200

def delAddress(id):
    # 根据 id 查询要删除的地址
    addr = Address.query.get(id)

    # 如果地址不存在，返回 404 错误
    if not addr:
        return jsonify({"message": "地址未找到"}), 404

    try:
        # 删除地址
        db.session.delete(addr)
        # 提交事务
        db.session.commit()
        return jsonify({"message": "删除成功"}), 200
    except Exception as e:
        # 如果发生错误，回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({"message": f"删除失败: {str(e)}"}), 500

def addAddress(address,user_id):
    # 检查必要的字段是否存在
    if not user_id or not address:
        return jsonify({"message": "用户 ID 和地址不能为空"}), 400

    try:
        # 创建新的地址对象
        new_address = Address(
            user_id=user_id,
            address=address
        )

        # 添加到数据库会话
        db.session.add(new_address)
        # 提交事务
        db.session.commit()
        addr = {
            'id':new_address.id,
            'addr': new_address.address,
            'is_default':new_address.is_default
        }

        return jsonify({"message": "地址添加成功", "addr": addr}), 201
    except Exception as e:
        # 如果发生错误，回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({"message": f"地址添加失败: {str(e)}"}), 500

def updateAuth(request, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "用户不存在"}), 404

    data = request.get_json()
    name = data.get('name')
    oldpwd = data.get('oldpwd')
    newpwd = data.get('newpwd')
    phone = data.get('phone')

    # 检查用户名是否重复
    if name and name != user.username:
        existing_user = User.query.filter_by(username=name).first()
        if existing_user:
            return jsonify({"message": "用户名已存在"}), 400

    # 检查手机号是否重复
    if phone and phone != user.phone:
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return jsonify({"message": "手机号已存在"}), 400


    # 获取当前文件所在的目录
    img_dir = os.path.join(os.getcwd(),'app','static','img','avatar')

    # 更新用户名称
    if name:
        old_name = user.username  # 保存旧的名称
        user.username = name

        old_avatar_path = os.path.join(img_dir, f"{old_name}.png")  # 假设图像文件是.png格式
        new_avatar_path = os.path.join(img_dir, f"{name}.png")

        # 检查旧的图像文件是否存在
        if os.path.exists(old_avatar_path):
            # 重命名图像文件
            os.rename(old_avatar_path, new_avatar_path)

    # 更新密码
    if newpwd:
        if check_password_hash(user.password, oldpwd):
            hashed_password = generate_password_hash(newpwd)
            user.password = hashed_password
        else:
            return jsonify({"message": "旧密码不正确"}), 400

    # 更新手机号
    if phone:
        user.phone = phone

    # 提交数据库更改
    db.session.commit()

    return jsonify({"message": "信息更新成功"}), 200

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def uploadAvatar(request, userid):
    if 'avatar' not in request.files:
        return jsonify({'message': '没有文件上传'}), 400

    file = request.files['avatar']

    # 检查文件是否为空
    if file.filename == '':
        return jsonify({'message': '未选择文件'}), 400

    # 检查文件类型和扩展名
    if not allowed_file(file.filename):
        return jsonify({'message': '只支持 JPG 或 PNG 格式的图片'}), 400

    # 检查文件大小（2MB）
    max_size = 2 * 1024 * 1024  # 2MB
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length > max_size:
        return jsonify({'message': '文件大小不能超过 2MB'}), 400

    user, _ = getAuth(userid)
    username = user.get_json().get('username')

    try:
        # 打开图像文件
        image = Image.open(file.stream)

        # 重命名为 username.png
        filename = f"{username}.png"
        file_path = os.path.join(os.getcwd(), 'app', 'static', 'img', 'avatar', filename)

        # 保存为 PNG 格式
        image.save(file_path, 'PNG')

        return jsonify({'message': '头像上传成功', 'file_path': file_path}), 200
    except Exception as e:
        return jsonify({'message': '文件处理失败', 'details': str(e)}), 500

def getUserList(request):
    # 获取可选的筛选条件
    page = int(request.args.get('page', 1))  # 默认第1页
    page_size = int(request.args.get('pageSize', 10))  # 默认每页10条
    search = request.args.get('search')  # 用户名或手机号
    sort_by = request.args.get('sort')  # 排序字段
    order = request.args.get('order')  # 排序方式：ascending 或 descending

    # 初始化查询
    query = User.query

    # 搜索条件
    if search:
        query = query.filter((User.username.like(f'%{search}%')) | (User.phone.like(f'%{search}%')))

    # 排序逻辑
    valid_sort_columns = ['id', 'username', 'phone', 'created_at', 'consumption', 'vip']  # 有效排序字段
    if sort_by and sort_by in valid_sort_columns:
        sort_column = getattr(User, sort_by)
        query = query.order_by(desc(sort_column) if order == 'descending' else asc(sort_column))
    else:
        query = query.order_by(desc(User.created_at))  # 默认按创建时间降序

    # 分页查询
    paginated_users = query.paginate(page=page, per_page=page_size, error_out=False)
    users = paginated_users.items
    total_users = paginated_users.total

    # 构造返回数据
    user_list = []
    for user in users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "role": user.role,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化时间
            "consumption": user.consumption,
            "vip": user.vip
        }
        user_list.append(user_info)

    return jsonify({
        'users': user_list,
        'total': total_users
    }), 200