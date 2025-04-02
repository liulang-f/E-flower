from flask_jwt_extended import get_jwt_identity
from sqlalchemy import asc, desc, text

from ..models import Order, OrderItem, db, Cart, Flower, User
from flask import request, jsonify
from datetime import datetime, timedelta


def create_order(request):
    # 获取前端发送的订单数据
    order_data = request.get_json()
    cart_ids = order_data.get('cart_ids')
    status = order_data.get('status')
    address = order_data.get('address')
    total_price = order_data.get('fTotal')
    remark = order_data.get('remark','')

    # 获取当前用户ID
    user_id = get_jwt_identity()

    # 查询购物车条目（仅限用户自己 & cart_ids 匹配的项）
    cart_items = Cart.query.filter_by(user_id=user_id).filter(Cart.id.in_(cart_ids)).all()

    if not cart_items:
        return {"message": "未找到符合条件的购物车商品"}, 400

    # 检查花卉库存是否足够
    for item in cart_items:
        flower = Flower.query.get(item.flower_id)
        if flower.stock < item.quantity:
            return {"message": f"花卉 {flower.name} 库存不足，无法完成订单"}, 400

    # 创建新订单
    new_order = Order(
        user_id=user_id,
        status=status,
        total_price=total_price,
        address=address,
        created_at=datetime.utcnow(),
        remark=remark
    )
    db.session.add(new_order)
    db.session.flush()  # 获取 new_order.id
    new_order_id = new_order.id

    # 只有当订单状态为 'paid' 时，才更新库存和销量
    if status == 'paid':
        # 创建订单项
        for item in cart_items:
            flower = Flower.query.get(item.flower_id)
            order_item = OrderItem(
                order_id=new_order_id,
                flower_id=item.flower_id,
                quantity=item.quantity,
                price=item.flower.price*item.flower.promotion.discount if item.flower.promotion_id else item.flower.price
            )
            db.session.add(order_item)

            # 更新花卉的库存和销量
            flower.stock -= item.quantity
            flower.sales += item.quantity

            # 从购物车中移除
            db.session.delete(item)

        db.session.commit()
    else:
        # 如果订单状态不是 'paid'，只创建订单和订单项，不更新库存和销量
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order_id,
                flower_id=item.flower_id,
                quantity=item.quantity,
                price=item.flower.price*item.flower.promotion.discount if item.flower.promotion_id else item.flower.price
            )
            db.session.add(order_item)
            db.session.delete(item)

        db.session.commit()

    return {"message": "订单创建成功", "order_id": new_order_id}, 201

# 获取订单列表
def get_orders(page, page_size, order_id=None, status=None):
    user_id = get_jwt_identity()

    # 基础查询 - 始终按用户ID筛选
    query = Order.query.filter_by(user_id=user_id)

    # 如果提供了order_id，添加订单ID筛选
    if order_id:
        query = query.filter(Order.id == order_id)

    # 如果提供了status，添加状态筛选
    if status:
        query = query.filter(Order.status == status)

    # 执行分页查询
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=False
    )

    orders = pagination.items

    order_list = []
    for order in orders:
        order_dict = {
            'id': order.id,
            'total_price': order.total_price,
            'status': order.status,
            'created_at': order.created_at,
            'address': order.address,
            'flower_count': len(order.items)
        }
        order_list.append(order_dict)

    # 返回响应，包含分页信息
    return jsonify({
        'orders': order_list,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_orders': pagination.total
    }), 200


# 获取订单详情
def get_order_details(order_id):
    # 查询指定订单
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    user = User.query.get(order.user_id)

    # 获取订单基本信息
    order_info = {
        "order_id": order.id,
        "username":user.username,
        "phone":user.phone,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "address": order.address,
        "remark": order.remark,
        "items": []
    }

    # 遍历订单项
    for item in order.items:
        # 获取花卉信息
        flower = Flower.query.get(item.flower_id)
        if not flower:
            continue  # 如果花卉不存在，跳过该订单项
        # 构建订单项信息
        item_info = {
            "flower_id": flower.id,
            "flower_name": flower.name,
            "flower_price": item.price,
            "flower_original_price": flower.price,
            "flower_description": flower.description,
            "flower_stock": flower.stock,
            "flower_quantity": item.quantity,
        }
        order_info["items"].append(item_info)

    return jsonify(order_info),200


# 修改订单状态（支付、发货、完成、取消）
def update_order_status(order_id, status):

    order = Order.query.get(order_id)

    if not order:
        return {"message": "订单不存在"}, 404

    valid_statuses = ['pending', 'paid', 'shipped', 'completed', 'cancelled']
    if status not in valid_statuses:
        return {"message": "无效的状态"}, 400

    order.status = status
    db.session.commit()
    return {"message": f"订单状态已更新为 {status}"}

#删除
def delOrder(order_id):

    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()

    return jsonify({"message":"删除成功"}),200

def buyNow(order_id):
    # 获取订单
    order = Order.query.get(order_id)
    if not order:
        return {"message": "订单不存在"},400

    # 检查库存
    for item in order.items:
        flower = Flower.query.get(item.flower_id)
        if flower.stock < item.quantity:
            return {"message": f"{flower.name}库存不足"},400

    # 更新库存和销量，修改订单状态
    for item in order.items:
        flower = Flower.query.get(item.flower_id)
        flower.stock -= item.quantity
        flower.sales += item.quantity

    order.status = 'paid'
    db.session.commit()

    return {"message": "支付成功"},200


def get_all_orders(request):
    # 获取可选的筛选条件
    status = request.args.get('status')
    date_range = request.args.getlist('dateRange[]')
    order_id = request.args.get('orderId')
    page = int(request.args.get('page', 1))  # 默认第1页
    page_size = int(request.args.get('pageSize', 10))  # 默认每页10条
    sort_by = request.args.get('sort')  # 排序字段
    order = request.args.get('order')  # 排序方式：ascending 或 descending

    # 初始化查询
    query = Order.query

    # 搜索条件
    if status:
        query = query.filter(Order.status == status)
    if date_range and len(date_range) == 2:
        start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
        query = query.filter(Order.created_at >= start_date, Order.created_at <= end_date)
    if order_id:
        query = query.filter(Order.id == order_id)

    # 排序逻辑
    valid_sort_columns = ['id', 'total_price', 'created_at']  # 有效排序字段
    if sort_by and sort_by in valid_sort_columns:
        sort_column = getattr(Order, sort_by)
        query = query.order_by(desc(sort_column) if order == 'descending' else asc(sort_column))
    else:
        query = query.order_by(desc(Order.created_at))  # 默认按创建时间降序

    # 分页查询
    paginated_orders = query.paginate(page=page, per_page=page_size, error_out=False)
    orders = paginated_orders.items
    total_orders = paginated_orders.total

    # 构造返回数据
    order_list = []
    for order in orders:
        user = User.query.get(order.user_id)
        order_info = {
            'id': order.id,
            'username': user.username,
            'totalPrice': order.total_price,
            'status': order.status,
            'createdAt': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'address': order.address
        }
        order_list.append(order_info)

    return jsonify({
        'orders': order_list,
        'total': total_orders
    }), 200

def getBaseOrderInf():
    # 获取今日日期范围
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # 今日订单数量
    today_orders_count = Order.query.filter(Order.created_at >= today_start, Order.created_at < today_end).count()

    # 待处理订单数量（status为'paid'的订单）
    pending_orders_count = Order.query.filter(Order.status == 'paid').count()

    # 配送中的订单数量（状态为'shipped'）
    shipped_orders_count = Order.query.filter(Order.status == 'shipped').count()

    # 今日收入，筛选除了'pending'之外的今日订单的总收入
    today_income = db.session.query(db.func.sum(Order.total_price)).filter(
        Order.created_at >= today_start, Order.created_at < today_end, Order.status != 'pending'
    ).scalar() or 0  # 如果没有订单，返回0

    return jsonify({"todaycount":today_orders_count, "todayclcount":pending_orders_count,
                    "todaypscount": shipped_orders_count,"todayincome": round(today_income,2)}),200



def adminOrderStatus(ids, status):
    """
    批量修改订单状态。

    :param ids: 订单ID列表
    :param status: 目标状态
    """

    if not ids:
        return jsonify({"message":"不存在需要修改的订单"}),400

    if status == 'shipped':
        # 当目标状态为'shipped'时，只修改原状态为'paid'的订单
        Order.query.filter(Order.id.in_(ids), Order.status == 'paid').update({'status': status}, synchronize_session=False)
    elif status == 'cancelled':
        Order.query.filter(Order.id.in_(ids), Order.status == 'paid').update({'status': status}, synchronize_session=False)
    else:
        # 其他情况下，直接修改所有指定ID的订单状态
        Order.query.filter(Order.id.in_(ids)).update({'status': status}, synchronize_session=False)

    db.session.commit()
    return jsonify({"message":"配置成功"}),200