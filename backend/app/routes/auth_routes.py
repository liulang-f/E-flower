from flask import Blueprint, request, jsonify
import app.services.auth_service as AS
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

from app.utils.requiredU import admin_required

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

# 用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')

    if not all([username, password, phone]):
        return jsonify({"message": "缺少必要字段"}), 400

    result,_ = AS.register_user(username, password, phone)

    return jsonify(result),_

# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not all([username, password]):
        return jsonify({"message": "缺少用户名或密码"}), 400

    result,_ = AS.login_user(username, password)

    return jsonify(result),_


@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    if AS.logout_user():
        return jsonify({"message": "成功退出！"}),200
    return jsonify({"message": "服务器出错了！"}),401

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """
    检查 Token 是否在黑名单中
    """
    jti = jwt_payload["jti"]
    return AS.isBlack(jti)

@auth_bp.route('/checkAuth', methods=['GET'])
@jwt_required()
def checkAuth():
    user_id = get_jwt_identity()
    return AS.checkAuth(user_id)

@auth_bp.route('/getAuth', methods=['POST'])
@jwt_required()
def getAuth():
    user_id = get_jwt_identity()
    return AS.getAuth(user_id)

@auth_bp.route('/upAddress', methods=['POST'])
@jwt_required()
def updateAddress():
    return AS.updateAddress(request)

@auth_bp.route('/delAddress', methods=['POST'])
@jwt_required()
def delAddress():
    data = request.get_json()
    addrid = data.get('addrid')
    return AS.delAddress(addrid)

@auth_bp.route('/addAddress', methods=['POST'])
@jwt_required()
def addAddress():
    user_id = get_jwt_identity()
    data = request.get_json()
    addr = data.get('addr')
    return AS.addAddress(addr,user_id)

@auth_bp.route('/updateAuth', methods=['POST'])
@jwt_required()
def updateAuth():
    user_id = get_jwt_identity()
    return AS.updateAuth(request,user_id)

@auth_bp.route('/uploadAvatar', methods=['POST'])
@jwt_required()
def uploadAvatar():
    user_id = get_jwt_identity()
    return AS.uploadAvatar(request,user_id)


@auth_bp.route('/getUserList', methods=['GET'])
@admin_required
def getUserList():
    return AS.getUserList(request)
