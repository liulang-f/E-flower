from flask import Blueprint, request, jsonify
from ..models import Promotion, db, Setting
from ..utils.requiredU import admin_required
import app.services.admin_service as ASs

admin_bp = Blueprint('admin', __name__)

# 创建促销活动
@admin_bp.route('/promotion', methods=['POST'])
@admin_required
def create_promotion():
    data = request.json
    new_promo = Promotion(**data)
    db.session.add(new_promo)
    db.session.commit()
    return {"message": "促销活动创建成功"}, 201


# 获取促销活动列表
@admin_bp.route('/promotions', methods=['GET'])
@admin_required
def get_promotions():
    promotions = Promotion.query.all()
    promo_list = [{"id": p.id, "title": p.title, "discount": p.discount} for p in promotions]
    return {"promotions": promo_list}, 200

# 获取基础信息
@admin_bp.route('/getBaseInfo', methods=['GET'])
@admin_required
def getBaseInfo():
    return ASs.getBaseInfo()

# 获取近七日销量
@admin_bp.route('/getSalesTrend', methods=['GET'])
@admin_required
def getSalesTrend():
    return ASs.get_sales_trend()

# 获取十五朵花
@admin_bp.route('/getTopFlower', methods=['GET'])
@admin_required
def getTopFlower():
    return ASs.getTopFlowers()

#order10
@admin_bp.route('/getTenOrder', methods=['GET'])
@admin_required
def getTenOrder():
    return ASs.getTenOrder()

@admin_bp.route('/reSetPwd', methods=['POST'])
@admin_required
def reSetPwd():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    return ASs.reSetPwd(user_id)

@admin_bp.route('/delUser', methods=['DELETE'])
@admin_required
def delUser():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    return (ASs.delUser(user_id))

@admin_bp.route('/getUserInf', methods=['GET'])
@admin_required
def GetUserInf():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    return ASs.getUserDetail(user_id)

@admin_bp.route('/getUserOrders', methods=['GET'])
@admin_required
def getUserOrders():
    return ASs.getUserOrders(request)

@admin_bp.route('/changeUserAddr', methods=['POST'])
@admin_required
def changeUserAddr():
    data = request.get_json()
    userId = data.get('userId')
    addrId = data.get('addrId')
    return ASs.changeUserAddr(userId,addrId)

@admin_bp.route('/getAllPro', methods=['GET'])
@admin_required
def getAllPro():
    page_size = request.args.get('size',10,int)
    page = request.args.get('page',1,int)
    return ASs.allPromotion(page_size,page)

@admin_bp.route('/flowersPro', methods=['GET'])
@admin_required
def flowersPro():
    pro_id = request.args.get("promotion_id")
    return ASs.flowersPro(pro_id)

@admin_bp.route('/allProTags', methods=['GET'])
@admin_required
def allProTags():
    return ASs.allProTags()

@admin_bp.route('/updatePro', methods=['POST'])
@admin_required
def updatePro():
    return ASs.adminUpdatePromotion(request)

@admin_bp.route('/addPro', methods=['POST'])
@admin_required
def addPro():
    return ASs.adminAddPromotion(request)

@admin_bp.route('/delPro', methods=['POST'])
@admin_required
def delPro():
    return ASs.adminDelPromotion(request)

@admin_bp.route('/logs', methods=['GET'])
@admin_required
def logs():
    return ASs.get_logs(request)

@admin_bp.route('/settings', methods=['GET'])
@admin_required
def settings():
    return ASs.get_settings()

@admin_bp.route('/updateSetting', methods=['PUT'])
@admin_required
def updateSetting():
    data = request.get_json()
    new_value = data.get('value')
    id = data.get('id')
    return ASs.update_setting(id,new_value)