from ..models import Cart,Flower,db
from flask_jwt_extended import get_jwt_identity
from app.services.flower_service import get_flower_detail

def add_to_cart(flower_id, quantity):
    user_id = get_jwt_identity()
    # 检查该花卉是否存在
    flower = Flower.query.get(flower_id)
    if not flower:
        return {"message": "这朵花已经没有啦！"}, 404

    flower_name = flower.name

    # 检查购物车中是否已存在该花卉
    cart_item = Cart.query.filter_by(user_id=user_id, flower_id=flower_id).first()

    if cart_item:
        # 如果已存在，更新数量
        quantity = quantity + cart_item.quantity
        cart_item.quantity = quantity
        message = f"购物车中已经存在！已经将购物车中数据更新为{quantity}！"
    else:
        # 如果不存在，添加新购物车项
        cart_item = Cart(user_id=user_id, flower_id=flower_id, quantity=quantity)
        db.session.add(cart_item)
        message = f"成功将{cart_item.quantity}朵{flower_name}添加至购物车"

    db.session.commit()
    return {"message": message}, 200

def remove_from_cart(cart_id):
    user_id = get_jwt_identity()
    cart_item = Cart.query.get(cart_id)
    if not cart_item or str(cart_item.user_id) != user_id:
        return {"message": "购物车出错啦，请刷新重试！"}, 404
    db.session.delete(cart_item)
    db.session.commit()
    return {"message": "删除成功"}, 200

def clear_cart():
    user_id = get_jwt_identity()
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return {"message": "购物车成功清空"}, 200



def update_cart(flower_id, quantity):
    userid = get_jwt_identity()
    cart_item = Cart.query.filter_by(user_id=userid, flower_id=flower_id).first()
    if not cart_item:
        return {"message": "未找到该物品"}, 404

    if quantity < 0:
        return {"message": "数量不可以小于零"}, 400
    elif quantity == 0:
        db.session.delete(cart_item)
        db.session.commit()
        return {"message":"删除成功"}

    cart_item.quantity = quantity
    db.session.commit()
    return {"message": "修改成功"}, 200


def get_cart(flower_ids=None):
    user_id = get_jwt_identity()
    # 构建查询条件
    query = Cart.query.filter_by(user_id=user_id)
    # 如果传入了 flower_ids，筛选特定花卉
    if flower_ids:
        query = query.filter(Cart.flower_id.in_(flower_ids))
    # 获取结果，并加载关联的 Flower 数据
    cart_items = query.join(Flower).all()
    # 若购物车为空
    if not cart_items:
        return {"message": "这里暂时空空如也"}, 404
    # 格式化返回数据
    cart_data = []
    for item in cart_items:
        cart_data.append({
            "cart_id": item.id,  # 购物车 ID
            "flower_id": item.flower.id,  # 花朵 ID
            "flower_name": item.flower.name,  # 花朵名称
            "quantity": item.quantity,  # 购买数量
            "price": item.flower.price,  # 这朵花的单价
            "discount": item.flower.promotion.discount if item.flower.promotion_id else None,
        })
    return cart_data, 200


def get_cart_by_carts(ids=None):
    user_id = get_jwt_identity()
    query = Cart.query
    query = query.filter_by(user_id=user_id)
    cart_data = []

    if ids:
        query = query.filter(Cart.id.in_(ids))

    # 获取结果
    cart_items = query.all()

    # 若购物车为空
    if not cart_items:
        return cart_data, 401

    # 格式化返回数据

    for item in cart_items:
        flower, _ = get_flower_detail(item.flower_id)
        cart_data.append({
            "cart_id": item.id,
            "flower_id": flower.get('id'),
            "price": flower.get('price'),
            "quantity": item.quantity
        })

    return cart_data, 200

def get_user_carts_count():
    user_id = get_jwt_identity()
    query = Cart.query
    query = query.filter_by(user_id=user_id)
    carts = 0
    if not query:
        return carts

    for item in query.all():
        carts+=item.quantity
    return carts