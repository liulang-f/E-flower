from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import app.services.order_service as OSe
from app.utils.requiredU import admin_required

order_bp = Blueprint('order', __name__)

@order_bp.route('/add', methods=['POST'])
@jwt_required()
def create():
    result, status_code = OSe.create_order(request)
    return jsonify(result), status_code

# 获取订单列表
@order_bp.route('/list', methods=['GET'])
@jwt_required()
def list_orders():
    page = request.args.get('page', 1, type=int)  # 添加type=int
    per_page = request.args.get('per_page', 10, type=int)  # 添加type=int
    order_id = request.args.get('order_id','')
    status = request.args.get('status','')
    return OSe.get_orders(page, per_page,order_id,status)

# 删除
@order_bp.route('/delorder', methods=['POST'])
@jwt_required()
def delorder():
    data = request.get_json()
    order_id = data.get('order_id')
    return OSe.delOrder(order_id)

# 获取订单详情
@order_bp.route('/orderdetail', methods=['POST'])
@jwt_required()
def order_detail():
    order_id = request.get_json().get('order_id')
    if not order_id:
        return jsonify("message","订单不能为空"),401
    return OSe.get_order_details(order_id)


# 修改订单状态（支付、发货、完成、取消）
@order_bp.route('/status', methods=['PUT'])
@jwt_required()
def update_status():
    data = request.get_json()
    status = data.get('status')
    order_id = data.get('order_id')
    result = OSe.update_order_status(order_id, status)
    return jsonify(result), 200

# 现在购买
@order_bp.route('/buyNow', methods=['POST'])
@jwt_required()
def buyNow():
    order_id = request.get_json().get("order_id")
    result, status_code = OSe.buyNow(order_id)
    return jsonify(result), status_code

# 管理员获取订单列表
@order_bp.route('/getAllOrders', methods=['GET'])
@admin_required
def getAllOrders():
    return OSe.get_all_orders(request)

# 管理员获取订单列表
@order_bp.route('/getOrderBaseInfo', methods=['GET'])
@admin_required
def getOrderBaseInfo():
    return OSe.getBaseOrderInf()

# 管理员获取订单列表
@order_bp.route('/adminOrderStatus', methods=['PUT'])
@admin_required
def adminOrderStatus():
    data = request.get_json()
    ids = data.get('ids')
    status = data.get('status')
    return OSe.adminOrderStatus(ids,status)