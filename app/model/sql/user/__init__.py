from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin

from app.extension.db import db
from app.model.sql.common import BaseModel


class User(BaseModel, UserMixin):
    """
    用户表
    """
    __tablename__ = 'user'

    username = db.Column(db.String(50), nullable=False, unique=True)  # 用户名
    password = db.Column(db.Text, nullable=False)  # 密码

    def save(self, username: str, password: str):
        self.username = username
        self.password = self.encode_psw(password)

        db.session.add(self)

        try:
            db.session.commit()
            current_app.logger.info("保存用户成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"保存用户失败, username: {username}, password: {password} err: {e}")
            return False

    @classmethod
    def encode_psw(cls, password: str) -> str:
        """
        通过用户密码生成一个哈希值
        :param password 明文密码
        :return: 加密后的密码
        """
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        return hashed_password

    def check_psw(self, password: str) -> bool:
        """
        验证账户密码是否正确
        :param password 明文密码
        :return:
        """
        return check_password_hash(self.password, password)
