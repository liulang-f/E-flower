from ..models import db, Promotion

def get_all_promotions():
    """获取所有优惠活动"""
    return Promotion.query

def get_promotions_by_tag(tags):
    query = Promotion.query
    for tag in tags:
        query = query.filter(Promotion.tags.like(f"%{tag}%"))
    return query


def get_promotion_by_id(promotion_id):
    """根据 ID 获取优惠活动"""
    return Promotion.query.get(promotion_id)


def create_promotion(title, discount, start_time, end_time):
    """创建新的优惠活动"""
    try:
        new_promotion = Promotion(
            title=title,
            discount=discount,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(new_promotion)
        db.session.commit()
        return new_promotion
    except Exception as e:
        db.session.rollback()
        raise e


def update_promotion(promotion_id, title=None, discount=None, start_time=None, end_time=None):
    """更新优惠活动"""
    promotion = Promotion.query.get(promotion_id)
    if not promotion:
        return None

    if title:
        promotion.title = title
    if discount:
        promotion.discount = discount
    if start_time:
        promotion.start_time = start_time
    if end_time:
        promotion.end_time = end_time

    try:
        db.session.commit()
        return promotion
    except Exception as e:
        db.session.rollback()
        raise e


def delete_promotion(promotion_id):
    """删除优惠活动"""
    promotion = Promotion.query.get(promotion_id)
    if not promotion:
        return None

    try:
        db.session.delete(promotion)
        db.session.commit()
        return promotion
    except Exception as e:
        db.session.rollback()
        raise e


def all_promotion():
    """
    返回所有活动及其信息
    :return: 查询结果列表
    """
    # 查询所有活动
    promotions = Promotion.query.all()

    # 将查询结果转换为字典列表
    result = []
    for promotion in promotions:
        result.append({
            'id': promotion.id,
            'title': promotion.title,
            'discount': promotion.discount,
            'start_time': promotion.start_time,
            'end_time': promotion.end_time,
            'tags': promotion.tags,
            'description': promotion.description
        })

    return result