from flask import jsonify
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app.models import Order, User, db, Setting, Flower, Address, Promotion, Log

from datetime import datetime, timedelta

from app.utils.someU import addLog


def getBaseInfo():
    base_info = {}

    # 获取今日日期和昨日日期
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # 今日新增订单量
    today_orders = Order.query.filter(Order.created_at >= datetime.combine(today, datetime.min.time()),
                                      Order.created_at < datetime.combine(today, datetime.max.time())).count()
    base_info['today_orders'] = today_orders

    # 昨日新增订单量
    yesterday_orders = Order.query.filter(Order.created_at >= datetime.combine(yesterday, datetime.min.time()),
                                          Order.created_at < datetime.combine(yesterday, datetime.max.time())).count()
    base_info['yesterday_orders'] = yesterday_orders

    # 计算今日订单量相比昨天的百分比
    if yesterday_orders == 0:
        base_info['order_percentage'] = "N/A"
    else:
        base_info['order_percentage'] = f"{((today_orders - yesterday_orders) / yesterday_orders) * 100:.2f}%"

    # 今日新增用户量
    today_users = User.query.filter(User.created_at >= datetime.combine(today, datetime.min.time()),
                                    User.created_at < datetime.combine(today, datetime.max.time())).count()
    base_info['today_users'] = today_users

    # 昨日新增用户量
    yesterday_users = User.query.filter(User.created_at >= datetime.combine(yesterday, datetime.min.time()),
                                        User.created_at < datetime.combine(yesterday, datetime.max.time())).count()
    base_info['yesterday_users'] = yesterday_users

    # 计算今日新增用户量相比昨天的增长率
    if yesterday_users == 0:
        base_info['user_percentage'] = "N/A"
    else:
        base_info['user_percentage'] = f"{((today_users - yesterday_users) / yesterday_users) * 100:.2f}%"

    # 今日收益
    today_sales = db.session.query(db.func.sum(Order.total_price)).filter(Order.created_at >= datetime.combine(today, datetime.min.time()),
                                                                          Order.created_at < datetime.combine(today, datetime.max.time())).scalar()
    today_sales = round(today_sales,2) if today_sales is not None else 0
    base_info['today_sales'] = today_sales

    # 昨日收益
    yesterday_sales = db.session.query(db.func.sum(Order.total_price)).filter(Order.created_at >= datetime.combine(yesterday, datetime.min.time()),
                                                                              Order.created_at < datetime.combine(yesterday, datetime.max.time())).scalar()
    yesterday_sales = round(yesterday_sales,2) if yesterday_sales is not None else 0
    base_info['yesterday_sales'] = yesterday_sales

    # 计算今日收益相比昨天的增长率
    if yesterday_sales == 0:
        base_info['sales_percentage'] = "N/A"
    else:
        base_info['sales_percentage'] = f"{((today_sales - yesterday_sales) / yesterday_sales) * 100:.2f}%"

    # 获取库存预警线
    warning_line = Setting.query.filter_by(key="库存预警线").first()
    if warning_line:
        warning_line_value = int(warning_line.value)
        # 查询库存低于预警线的商品数量
        low_stock_flowers = Flower.query.filter(Flower.stock < warning_line_value).count()
        base_info['low_stock_flowers'] = low_stock_flowers
    else:
        base_info['low_stock_flowers'] = "库存预警线未设置"
    return jsonify(base_info),200

def get_sales_trend():
    # 获取近七天的日期
    today = datetime.utcnow()
    days = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]

    # 查询近七天的订单数量和订单总金额
    order_counts = []
    total_sales = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        # 查询当天的订单数量
        order_count = db.session.query(func.count(Order.id)).filter(
            Order.created_at >= date,
            Order.created_at < date + timedelta(days=1)
        ).scalar() or 0

        # 查询当天的订单总金额
        total_sale = db.session.query(func.sum(Order.total_price)).filter(
            Order.created_at >= date,
            Order.created_at < date + timedelta(days=1)
        ).scalar() or 0

        order_counts.append(order_count)
        total_sales.append(round(total_sale, 2))  # 保留两位小数

    return jsonify({
        'days': days,
        'order_counts': order_counts,
        'total_sales': total_sales
    }),200

def getTopFlowers():
    # 查询销量前20的花朵
    top_flowers = Flower.query.order_by(Flower.sales.desc()).limit(15).all()
    top_flowers = sorted(top_flowers, key=lambda x: x.sales)
    result = [
        {
            'name': flower.name,
            'sales': flower.sales
        }
        for flower in top_flowers
    ]
    return jsonify(result),200

def getTenOrder():
    try:
        # 查询最近的10条订单，关联用户表获取用户名
        recent_orders = db.session.query(
            Order.id,
            User.username,
            Order.total_price,
            Order.created_at,
            Order.address
        ).join(
            User, Order.user_id == User.id
        ).order_by(
            Order.created_at.desc()
        ).limit(10).all()

        orders_data = [{
            "id": order.id,
            "username": order.username,
            "total_price": float(order.total_price),
            "created_at": order.created_at.isoformat(),
            "address": order.address
        } for order in recent_orders]

        return jsonify(orders_data),200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "获取订单数据失败"
        }), 500

def reSetPwd(user_id):
    user = User.query.get(user_id)
    user.password = generate_password_hash('12345678')
    db.session.commit()
    return jsonify({"message":"重置成功"}),200

def delUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"删除成功"}),200

def getUserDetail(user_id):
    # 查询用户基本信息
    user = User.query.get(user_id)
    if not user:
        return None  # 如果用户不存在，返回 None

    # 构建用户基本信息
    user_info = {
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "vip": user.vip,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "consumption": user.consumption,
        "addresses":[],
    }

    # 查询用户的地址列表
    addresses = [
        {
            "id":address.id,
            "address": address.address,
            "is_default": address.is_default
        }
        for address in user.address
    ]

    # 将用户信息、地址列表和订单列表组合成最终结果
    user_info["addresses"] = addresses

    return jsonify(user_info),200

def getUserOrders(request):
    # 获取请求参数
    data = request.args
    user_id = data.get('userId', type=int)
    page = data.get('page', 1, type=int)
    page_size = data.get('pageSize', 10, type=int)

    if not user_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400

    try:
        # 查询订单基础信息
        orders_query = Order.query.filter_by(user_id=user_id)

        # 获取总数
        total = orders_query.count()

        # 分页查询
        orders = orders_query.order_by(Order.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()

        # 构建返回数据
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'total_price': order.total_price,
                'status': order.status,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'address': order.address,
                'remark': order.remark,
            })

        return jsonify({'orders': orders_data,'total': total})

    except Exception as e:
        return jsonify({'message': f'获取订单失败: {str(e)}'}), 500

def changeUserAddr(userId, addrId):
    # 查询用户的所有地址
    user_addresses = Address.query.filter_by(user_id=userId).all()

    # 检查是否存在 addrId 对应的地址
    target_address = None
    for address in user_addresses:
        if address.id == addrId:
            target_address = address
            break

    if not target_address:
        return jsonify({"message": "指定的地址不存在"}), 404

    # 将所有地址的 is_default 设为 0
    for address in user_addresses:
        address.is_default = 0

    # 将目标地址的 is_default 设为 1
    target_address.is_default = 1

    # 提交到数据库
    db.session.commit()

    return jsonify({"message": "修改成功"})

def allPromotion(page_size, page):
    """
    返回所有活动及其信息，并支持分页
    :param page_size: 每页显示的活动数量
    :param page: 当前页码
    :return: 查询结果列表和总活动数量
    """
    # 查询总活动数量
    total = Promotion.query.count()

    # 使用分页查询获取当前页的活动
    promotions = Promotion.query.paginate(page=page, per_page=page_size, error_out=False).items

    # 将查询结果转换为字典列表
    result = []
    for promotion in promotions:
        # 格式化 start_time 和 end_time 为 'YYYY-MM-DD HH:mm:ss'
        formatted_start = promotion.start_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_end = promotion.end_time.strftime('%Y-%m-%d %H:%M:%S')

        result.append({
            'id': promotion.id,
            'title': promotion.title,
            'discount': promotion.discount,
            'start_time': formatted_start,  # 格式化后的时间
            'end_time': formatted_end,      # 格式化后的时间
            'tags': promotion.tags.split(',') if promotion.tags else [],
            'description': promotion.description
        })

    # 返回分页结果和总活动数量
    return jsonify({
        'promotions': result,
        'total': total
    }), 200

def flowersPro(pro_id):
    result = []
    flowers = Flower.query.filter_by(promotion_id=pro_id)
    for flower in flowers:
        result.append(
            {
                "flower_id":flower.id,
                "flower_name":flower.name
            }
        )
    return jsonify(result),200

def allProTags():
    # 查询所有活动的标签字段
    tags_list = db.session.query(Promotion.tags).all()

    # 将所有标签拆分并去重
    all_tags = set()  # 使用集合自动去重
    for tags in tags_list:
        if tags[0]:  # 确保标签字段不为空
            tag_list = tags[0].split(",")  # 按逗号拆分
            all_tags.update(tag_list)  # 将拆分后的标签加入集合

    # 将集合转换为列表并返回
    result = list(all_tags)
    return jsonify(result), 200

def adminUpdatePromotion(request):
    """
    更新活动信息
    """
    try:
        data = request.get_json()

        # 验证必要字段
        required_fields = ['id', 'title', 'discount', 'start_time', 'end_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'code': 400, 'message': f'缺少必要字段: {field}'}), 400

        # 验证折扣率范围
        if not (0.1 <= float(data['discount']) <= 0.9):
            return jsonify({'code': 400, 'message': '折扣率必须在0.1到0.9之间'}), 400

        # 验证时间范围
        try:
            start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')

            if start_time >= end_time:
                return jsonify({'code': 400, 'message': '结束时间必须晚于开始时间'}), 400
        except ValueError:
            return jsonify({'code': 400, 'message': '时间格式不正确，应为YYYY-MM-DD HH:MM:SS'}), 400

        # 查找并更新活动
        promotion = Promotion.query.get(data['id'])
        if not promotion:
            return jsonify({'code': 404, 'message': '活动不存在'}), 404

        # 更新活动信息
        promotion.title = data['title']
        promotion.discount = data['discount']
        promotion.start_time = start_time
        promotion.end_time = end_time
        promotion.tags = data.get('tags', '')
        promotion.description = data.get('description', '')

        db.session.commit()

        return jsonify({
            'code': 200,
            'message': '活动更新成功',
            'data': {
                'id': promotion.id,
                'title': promotion.title,
                'discount': promotion.discount,
                'start_time': promotion.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': promotion.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'tags': promotion.tags,
                'description': promotion.description
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

def adminAddPromotion(request):
    """
    添加新活动
    """
    try:
        data = request.get_json()

        # 验证必要字段
        required_fields = ['title', 'discount', 'start_time', 'end_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'code': 400, 'message': f'缺少必要字段: {field}'}), 400

        # 验证折扣率范围
        if not (0.1 <= float(data['discount']) <= 0.9):
            return jsonify({'code': 400, 'message': '折扣率必须在0.1到0.9之间'}), 400

        # 验证时间范围
        try:
            start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')

            if start_time >= end_time:
                return jsonify({'code': 400, 'message': '结束时间必须晚于开始时间'}), 400
        except ValueError:
            return jsonify({'code': 400, 'message': '时间格式不正确，应为YYYY-MM-DD HH:MM:SS'}), 400

        # 创建新活动
        new_promotion = Promotion(
            title=data['title'],
            discount=data['discount'],
            start_time=start_time,
            end_time=end_time,
            tags=data.get('tags', ''),
            description=data.get('description', '')
        )

        db.session.add(new_promotion)
        db.session.commit()

        return jsonify({
            'code': 200,
            'message': '活动添加成功',
            'data': {
                'id': new_promotion.id,
                'title': new_promotion.title,
                'discount': new_promotion.discount,
                'start_time': new_promotion.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': new_promotion.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'tags': new_promotion.tags,
                'description': new_promotion.description
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

def adminDelPromotion(request):
    """
    删除活动
    """
    try:
        data = request.get_json()

        # 验证必要字段
        if 'id' not in data:
            return jsonify({'code': 400, 'message': '缺少活动ID'}), 400

        # 查找活动
        promotion = Promotion.query.get(data['id'])
        if not promotion:
            return jsonify({'code': 404, 'message': '活动不存在'}), 404

        # 删除活动
        db.session.delete(promotion)
        db.session.commit()

        return jsonify({
            'code': 200,
            'message': '活动删除成功',
            'data': {
                'id': data['id']
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

def get_logs(request):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    username = request.args.get('username', '').strip()
    operation = request.args.get('operation', '').strip()

    query = Log.query.join(User, Log.user_id == User.id)

    if username:
        query = query.filter(User.username.like(f'%{username}%'))
    if operation:
        query = query.filter(Log.operation == operation)

    # 按时间降序排列
    query = query.order_by(Log.operation_time.desc())

    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    logs = pagination.items

    result = {
        'items': [{
            'id': log.id,
            'username': log.user.username if log.user else '未知用户',
            'operation': log.operation,
            'detail': log.detail,
            'operation_time': log.operation_time.isoformat()
        } for log in logs],
        'total': pagination.total
    }

    return jsonify(result)


def get_settings():
    try:
        settings = Setting.query.all()
        result = [
            {
                'id': setting.id,
                'key': setting.key,
                'value': setting.value,
                'description':setting.description
            }
            for setting in settings
        ]
        return jsonify(result),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_setting(id,newV):
    if newV is None:
        return jsonify({'error': 'Value is required'}), 400

    setting = Setting.query.get_or_404(id)
    setting.value = newV

    addLog('update','系统设置 '+setting.key+' 被修改为 '+ str(newV))

    db.session.commit()

    return jsonify({'message': '设置修改成功'}),200