from datetime import datetime, timezone
from sqlalchemy import func

from app.extension.db import db


class Time:
    """
    自动添加时间
    """
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now())  # 更新时间


class BaseModel(db.Model):
    __abstract__ = True  # 表示这是一个抽象基类，不会被用作实际的表

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)  # 删除时间

    def delete(self):
        """
        删除本身
        :return:
        """
        self.deleted_at = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def query_with_soft_delete(cls, *args, **kwargs):
        return cls.query.filter_by(deleted_at=None)
