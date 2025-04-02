from datetime import datetime

from PIL import Image
from flask import jsonify
from app.models import Flower,db
from sqlalchemy import desc, asc
import json
import os

def get_flowers(search='', tags=None, min_price=None, max_price=None, sort_by='sales', order='desc', page=1, per_page=10, promotion=0, create_at=None, stock=None):
    """
    通用方法：根据筛选条件获取花朵数据
    :param search: 搜索关键字
    :param tags: 标签列表
    :param min_price: 最低价格
    :param max_price: 最高价格
    :param sort_by: 排序字段
    :param order: 排序方式（asc/desc）
    :param page: 当前页码
    :param per_page: 每页数量
    :param promotion: 优惠id
    :return: 花朵数据和分页信息
    :create_at: 创建时间
    """
    # 初始化查询
    query = Flower.query

    # 搜索条件
    if search:
        query = query.filter((Flower.name.like(f"%{search}%")) | (Flower.description.like(f"%{search}%")))
    if tags:
        for tag in tags:
            query = query.filter(Flower.tags.like(f"%{tag}%"))
    if min_price is not None:
        query = query.filter(Flower.price >= min_price)
    if max_price is not None:
        query = query.filter(Flower.price <= max_price)
    if create_at is not None:
        query = query.filter(Flower.created_at > create_at)
    if stock:
        query = query.filter(Flower.stock >= stock)
    elif stock==0:
        query = query.filter(Flower.stock == 0)

    # 优惠筛选逻辑
    if promotion == -1:
        # 返回所有有优惠的花朵
        query = query.filter(Flower.promotion_id.isnot(None))
    elif promotion > 0:
        # 按活动 ID 返回花朵
        query = query.filter(Flower.promotion_id == promotion)

    # 排序逻辑
    valid_sort_columns = ['sales', 'stock', 'created_at', 'price']
    sort_column = getattr(Flower, sort_by, Flower.sales) if sort_by in valid_sort_columns else Flower.sales
    query = query.order_by(desc(sort_column) if order == 'desc' else asc(sort_column))
    totalflower = query.count()

    # 分页查询
    flowers_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    # 构造返回数据
    flowers_data = [
        {
            "id": f.id,
            "name": f.name,
            "price": f.price,
            "tags": f.tags.split(',') if f.tags else [],
            "stock": f.stock,
            "sales": f.sales,
            "created_at": f.created_at,
            "discount": f.promotion.discount if f.promotion_id else None,  # 只有 promotion_id 存在时返回 discount
            "description": f.description if f.description else None,
            "promotion_id": f.promotion_id if f.promotion_id else None,
        }
        for f in flowers_paginated.items
    ]

    unique_tags = set()
    for flower in flowers_paginated.items:
        if flower.tags:
            tags = flower.tags.split(',')
            unique_tags.update(tags)
    sorted_tags = sorted(list(unique_tags))

    # 返回 JSON 数据
    return {
        "flowers": flowers_data,
        "pages": flowers_paginated.pages,
        "current_page": flowers_paginated.page,
        "tags": sorted_tags,
        "totalflower":totalflower
    }

def get_show_flowers():
    # 查询推荐的花卉，并按销售量降序排列
    data = get_flowers(tags=['推荐']).get('flowers')
    # 返回JSON格式的数据和HTTP状态码200
    return jsonify({
        "flowers": data
    }), 200

def get_hot_flowers():
    # 查询推荐的花卉，并按销售量降序排列
    data = get_flowers(per_page=8).get('flowers')
    # 返回JSON格式的数据和HTTP状态码200
    return jsonify({
        "flowers": data
    }), 200

def get_discount_flowers():
    # 查询推荐的花卉，并按销售量降序排列
    data = get_flowers(promotion=-1,per_page=8).get('flowers')
    # 返回JSON格式的数据和HTTP状态码200
    return jsonify({
        "flowers": data
    }), 200


def get_flower_detail(flower_id):
    flower = Flower.query.get(flower_id)
    if not flower:
        return jsonify({"error": "花卉不存在"}), 404

    flower_data = {
        "id": flower.id,
        "name": flower.name,
        "price": flower.price,
        "tags": flower.tags.split(',') if flower.tags else [],
        "stock": flower.stock,
        "sales": flower.sales,
        "created_at": flower.created_at,
        "discount": flower.promotion.discount if flower.promotion_id else None,
        "description": flower.description,
        "promotion": flower.promotion.title if flower.promotion_id else None,
    }
    return flower_data,200

def delete_flower(flower_id):
    flower = Flower.query.get(flower_id)
    if not flower:
        return jsonify({"error": "花卉不存在"}), 404
    db.session.delete(flower)
    db.session.commit()
    return jsonify({"message": "花卉删除成功"}),200

def update_flower(request):
    """ 更新花卉信息，包括库存与销量 """
    data = request.get_json()
    flower_id = data.get('id')
    flower = Flower.query.get(flower_id)
    if not flower:
        return jsonify({"message": "花卉未找到"}), 404


    # 更新花卉信息和销售/库存
    for key, value in data.items():
        if hasattr(flower, key) and key != 'id':
            if key == 'sales':
                flower.sales += value
            elif key == 'stock':
                flower.stock -= value
            else:
                setattr(flower, key, value)

    db.session.commit()
    return jsonify({"message": "花卉信息已更新"})


def get_tags():
    flowers = Flower.query.all()
    unique_tags = set()

    for flower in flowers:
        if flower.tags:
            tags = flower.tags.split(',')
            unique_tags.update(tags)

    # 按字母顺序排序
    sorted_tags = sorted(list(unique_tags))

    return sorted_tags


def adminAddFlower(request):
    if request.method != 'POST':
        return jsonify({'status': 'error', 'message': '请求方法不允许'}), 405

    try:
        # 获取表单数据
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')

        # 处理标签，将JSON字符串转为Python对象，然后转为逗号分隔的字符串存储
        tags_str = request.form.get('tags', '[]')
        tags_list = json.loads(tags_str)
        tags_db_str = ','.join(tags_list)  # 转换为数据库可存储的格式

        # 获取促销ID
        promotion_id = request.form.get('promotion_id')
        if promotion_id == "":
            promotion_id = None

        # 基本数据验证
        if not name or not price or stock is None:
            return jsonify({'status': 'error', 'message': '缺少必要字段'}), 400

        # 检查花卉名称是否已存在
        existing_flower = Flower.query.filter_by(name=name).first()
        if existing_flower:
            return jsonify({'status': 'error', 'message': '该花卉名称已存在'}), 400

        # 处理图片上传
        image_file = request.files.get('image')
        if image_file:
            # 确保目录存在
            img_dir = os.path.join(os.getcwd(), 'app', 'static', 'img')
            os.makedirs(img_dir, exist_ok=True)

            # 确定文件路径
            file_path = os.path.join(img_dir, f"{name}.png")

            # 保存图片
            image_file.save(file_path)

            # 如果需要处理图片（调整大小或格式）
            img = Image.open(file_path)
            img = img.convert('RGBA')  # 确保PNG透明度
            img.save(file_path, 'PNG')

        # 创建新花卉记录
        new_flower = Flower(
            name=name,
            price=float(price),
            stock=int(stock),
            description=description,
            tags=tags_db_str,
            promotion_id=promotion_id,
            sales=0,  # 初始销量为0
            created_at=datetime.utcnow()
        )

        # 保存到数据库
        db.session.add(new_flower)
        db.session.commit()

        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': '花卉添加成功',
            'flower': {
                'id': new_flower.id,
                'name': new_flower.name,
                'price': new_flower.price,
                'stock': new_flower.stock,
                'description': new_flower.description,
                'tags': tags_list,  # 返回原始标签列表
                'promotion_id': new_flower.promotion_id,
                'sales': new_flower.sales,
                'created_at': new_flower.created_at.isoformat()
            }
        }), 201

    except json.JSONDecodeError:
        return jsonify({'status': 'error', 'message': '标签格式无效'}), 400
    except Exception as e:
        # 出错回滚事务
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'添加花卉失败: {str(e)}'}), 500


def adminUpdateFlower(request, flower_id):
    if request.method != 'PUT':
        return jsonify({'status': 'error', 'message': '请求方法不允许'}), 405

    try:
        # 获取要更新的花卉
        flower = Flower.query.get(flower_id)
        if not flower:
            return jsonify({'status': 'error', 'message': '花卉不存在'}), 404

        # 获取表单数据
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description','')

        # 处理标签
        tags_str = request.form.get('tags', '[]')
        tags_list = json.loads(tags_str)
        tags_db_str = ','.join(tags_list)

        # 获取促销ID
        promotion_id = request.form.get('promotion_id')
        if promotion_id == "":
            promotion_id = None

        # 如果更改了名称，检查新名称是否已存在（除了当前花卉）
        if name != flower.name and Flower.query.filter_by(name=name).first():
            return jsonify({'status': 'error', 'message': '该花卉名称已存在'}), 400

        # 处理图片上传
        image_file = request.files.get('image')
        if image_file:
            # 如果花卉名称已更改，需要处理旧图片
            old_image_path = os.path.join(os.getcwd(), 'app', 'static', 'img' , f"{flower.name}.png")

            # 确保目录存在
            img_dir = os.path.join(os.getcwd(), 'app', 'static', 'img')

            os.makedirs(img_dir, exist_ok=True)

            # 确定新文件路径
            new_image_path = os.path.join(img_dir, f"{name}.png")

            # 保存新图片
            image_file.save(new_image_path)

            # 处理新图片
            img = Image.open(new_image_path)
            img = img.convert('RGBA')
            img.save(new_image_path, 'PNG')

            # 如果名称已更改，删除旧图片
            if name != flower.name and os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except:
                    pass  # 忽略删除旧图片的错误

        # 更新花卉信息
        flower.name = name
        flower.price = float(price)
        flower.stock = int(stock)
        flower.description = description
        flower.tags = tags_db_str
        flower.promotion_id = promotion_id

        # 保存更新
        db.session.commit()

        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': '花卉更新成功',
            'flower': {
                'id': flower.id,
                'name': flower.name,
                'price': flower.price,
                'stock': flower.stock,
                'description': flower.description,
                'tags': tags_list,
                'promotion_id': flower.promotion_id,
                'sales': flower.sales,
                'created_at': flower.created_at.isoformat()
            }
        })

    except json.JSONDecodeError:
        return jsonify({'status': 'error', 'message': '标签格式无效'}), 400
    except Exception as e:
        # 出错回滚事务
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'更新花卉失败: {str(e)}'}), 500