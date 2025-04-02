from flask import Blueprint, request, jsonify

from app.services import promotion_service as PS
from datetime import datetime

from app.utils.requiredU import admin_required

# 创建 Blueprint
promotion_bp = Blueprint('promotion_bp', __name__)

@promotion_bp.route('/promotions', methods=['GET'])
def get_promotions():
    """获取所有优惠活动"""
    tag = request.args.get('tag')  # 获取前端传递的tag参数
    page = int(request.args.get('page', 1))  # 获取前端传递的page参数，默认为1
    per_page = int(request.args.get('pageSize', 2))  # 获取前端传递的pageSize参数，默认为2

    query = PS.get_all_promotions()

    # 获取所有活动的标签
    all_tags = set()
    for p in query.all():
        if p.tags:
            all_tags.update(p.tags.split(','))

    if tag:
        # 如果前端传递了tag参数，则根据tag搜索
        query = PS.get_promotions_by_tag(tag)

    # 使用paginate方法进行分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    promotions = pagination.items  # 当前页的数据
    total_pages = pagination.pages  # 总页数
    current_page = pagination.page  # 当前页码

    # 构造返回数据
    result = [
        {
            "id": p.id,
            "title": p.title,
            "discount": p.discount,
            "start_time": p.start_time.isoformat(),
            "end_time": p.end_time.isoformat(),
            "description": p.description,
            "tags": p.tags.split(',') if p.tags else []
        }
        for p in promotions
    ]

    return jsonify({
        "promotions": result,
        "pages": total_pages,
        "current_page": current_page,
        "tags": list(all_tags)
    }), 200


@promotion_bp.route('/promotions/<int:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    """根据 ID 获取优惠活动"""
    promotion = PS.get_promotion_by_id(promotion_id)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404

    result = {
        "id": promotion.id,
        "title": promotion.title,
        "discount": promotion.discount,
        "start_time": promotion.start_time.isoformat(),
        "end_time": promotion.end_time.isoformat(),
        "description": promotion.description,
        "tags": promotion.tags.split(',') if promotion.tags else []
    }
    return jsonify(result), 200


@promotion_bp.route('/promotions', methods=['POST'])
def create_new_promotion():
    """创建优惠活动"""
    data = request.json
    title = data.get('title')
    discount = data.get('discount')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not (title and discount and start_time and end_time):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
        new_promotion = PS.create_promotion(title, discount, start_time, end_time)
        return jsonify({
            "id": new_promotion.id,
            "title": new_promotion.title,
            "discount": new_promotion.discount,
            "start_time": new_promotion.start_time.isoformat(),
            "end_time": new_promotion.end_time.isoformat()
        }), 201

    except ValueError:
        return jsonify({"message": "Invalid date format. Use ISO format."}), 400


@promotion_bp.route('/promotions/<int:promotion_id>', methods=['PUT'])
def update_existing_promotion(promotion_id):
    """更新优惠活动"""
    data = request.json
    title = data.get('title')
    discount = data.get('discount')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if start_time:
        try:
            start_time = datetime.fromisoformat(start_time)
        except ValueError:
            return jsonify({"message": "Invalid start_time format. Use ISO format."}), 400

    if end_time:
        try:
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            return jsonify({"message": "Invalid end_time format. Use ISO format."}), 400

    updated_promotion = PS.update_promotion(promotion_id, title, discount, start_time, end_time)

    if not updated_promotion:
        return jsonify({"message": "Promotion not found"}), 404

    return jsonify({
        "id": updated_promotion.id,
        "title": updated_promotion.title,
        "discount": updated_promotion.discount,
        "start_time": updated_promotion.start_time.isoformat(),
        "end_time": updated_promotion.end_time.isoformat()
    }), 200


@promotion_bp.route('/promotions/<int:promotion_id>', methods=['DELETE'])
def delete_existing_promotion(promotion_id):
    """删除优惠活动"""
    promotion = PS.delete_promotion(promotion_id)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404

    return jsonify({"message": "Promotion deleted successfully"}), 200

@promotion_bp.route('/allpromotions', methods=['GET'])
@admin_required
def allpromotions():
    result =  PS.all_promotion()
    return jsonify(result), 200
