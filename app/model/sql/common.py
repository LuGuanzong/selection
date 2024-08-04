from datetime import datetime, timezone
from abc import ABC

from app.extension.db import db
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import declared_attr


class SoftDeleteMixin:
    """
    软删除混合类，用于自动过滤已删除的记录。
    """
    deleted_at = db.Column(db.DateTime)  # 删除时间

    @classmethod
    @declared_attr
    def query_class(cls):
        """
        返回自定义的查询类。
        """

        class QueryWithSoftDelete(Query, ABC):
            def get(self, ident, *args, **kwargs):
                """
                重写 get 方法以添加软删除过滤。
                """
                return super().get(ident, *args, **kwargs, filters=[cls.deleted_at.is_(None)])

            def filter(self, *criterion):
                """
                重写 filter 方法以自动添加软删除过滤。
                """
                return super().filter(cls.deleted_at.is_(None), *criterion)

            def filter_by(self, **kwargs):
                """
                重写 filter_by 方法以自动添加软删除过滤。
                """
                kwargs.setdefault('deleted_at', None)
                return super().filter_by(**kwargs)

        return QueryWithSoftDelete

    def delete(self):
        """
        删除本身
        :return:
        """
        self.deleted_at = datetime.now(timezone.utc)
        db.session.commit()  # 不要忘记提交会话 不要忘记提交会话


class Time(SoftDeleteMixin):
    """
    自动添加时间
    """
    created_at = db.Column(db.DateTime, nullable=False)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False)  # 更新时间
