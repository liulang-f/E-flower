from flask import Blueprint, request, jsonify

import app.services.flower_service as FS
from ..utils.requiredU import admin_required

flower_bp = Blueprint('flower', __name__)


# --------- 花卉列表展示 ---------
@flower_bp.route('/flowers', methods=['GET'])
def get_flowers():
    search = request.args.get('search', '').strip()
    tags = request.args.get('tags', '').split(',') if request.args.get('tags') else []
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by', 'sales')  # 默认按照销量降序
    order = request.args.get('order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    promotion = request.args.get('promotionId', 0, type=int)  # 优惠筛选参数
    create_at = request.args.get('create_at', None)
    stock = request.args.get('stock', None, type=int)
    result = FS.get_flowers(search, tags, min_price, max_price, sort_by, order, page, per_page, promotion, create_at,
                            stock)
    return jsonify(result), 200


# --------- 推荐花卉展示 ---------
@flower_bp.route('/showFlowers', methods=['GET'])
def get_show_flowers():
    return FS.get_show_flowers()


@flower_bp.route('/hotFlowers', methods=['GET'])
def get_hot_flowers():
    return FS.get_hot_flowers()


@flower_bp.route('/discountFlowers', methods=['GET'])
def get_discount_flowers():
    return FS.get_discount_flowers()


# --------- 花卉详情展示 ---------
@flower_bp.route('/flowers/<int:flower_id>', methods=['GET'])
def get_flower_detail(flower_id):
    result, _ = FS.get_flower_detail(flower_id)
    return jsonify(result), _


# --------- 增加花卉 ---------
@flower_bp.route('/addFlower', methods=['POST'])
@admin_required
def add_flower():
    return FS.adminAddFlower(request)


# --------- 修改花卉 ---------
@flower_bp.route('/updateFlower/<int:flower_id>', methods=['PUT'])
@admin_required
def updateFlower(flower_id):  # 直接使用路径参数
    return FS.adminUpdateFlower(request, flower_id)


# --------- 删除花卉 ---------
@flower_bp.route('/delFlowerAdmin', methods=['DELETE'])
def delete_flower():
    f_id = request.get_json().get('id')
    return FS.delete_flower(f_id)


# --------- 修改花卉信息 ---------
@flower_bp.route('/flowers', methods=['PUT'])
def update_flower():
    return FS.update_flower(request)


# --------- 查找标签 ---------
@flower_bp.route('/tags', methods=['get'])
def get_tags():
    data = FS.get_tags()
    return jsonify(data), 200
