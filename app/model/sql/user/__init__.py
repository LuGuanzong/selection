from app.extension.db import db
from app.model.sql.common import BaseModel


class User(BaseModel):
    """
    用户表
    """
    __tablename__ = 'user'

    username = db.Column(db.String(50), nullable=False, unique=True)  # 用户名
    password = db.Column(db.String(50), nullable=False)  # 密码
