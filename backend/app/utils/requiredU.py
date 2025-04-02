from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import User

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.role=="admin":
            return {"message": "只有管理员可以访问该接口"}, 403
        return fn(*args, **kwargs)
    return wrapper
