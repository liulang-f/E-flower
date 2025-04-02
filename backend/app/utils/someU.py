from flask_jwt_extended import get_jwt_identity
from ..models import Log,db


def addLog(operation,detail):
    user_id = get_jwt_identity()
    newLog = Log(
        user_id = user_id,
        operation=operation,
        detail=detail,
    )
    db.session.add(newLog)
    db.session.commit()
    return 1