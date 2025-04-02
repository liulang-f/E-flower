from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import app.services.cart_service as CS

cart_bp = Blueprint('cart', __name__)

# 添加商品到购物车
@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    flower_id = data.get("flower_id")
    quantity = data.get("quantity")

    if not flower_id or not quantity:
        return jsonify({"message": "数据出问题啦！"}), 400

    return CS.add_to_cart(flower_id,quantity)

# 移除或清空购物车商品
@cart_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_cart():
    data = request.get_json()
    cart_id = data.get("cart_id")
    if not cart_id:
        return jsonify({"message":"没有购物车信息"})
    return CS.remove_from_cart(cart_id)

@cart_bp.route('/clear', methods=['GET'])
@jwt_required()
def clear_cart():
    return CS.clear_cart()

# 更新购物车商品的数量
@cart_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_cart():
    data = request.get_json()
    flower_id = data.get("flower_id")
    quantity = data.get("quantity")
    print(flower_id,quantity)
    return CS.update_cart(flower_id, quantity)


# 获取当前用户的购物车信息
@cart_bp.route('/getCarts', methods=['GET'])
@jwt_required()
def view_cart():
    result,_ = CS.get_cart()
    return jsonify(result),_