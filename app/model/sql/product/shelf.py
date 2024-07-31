from flask import current_app

from app.extension.db import db
from app.model.sql.common import Time


class Shelf(db.Model, Time):
    """
    skc表
    """
    __table_name__ = 'shelfs'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article = db.Column(db.String(30), nullable=False, unique=True)  # 货架号

    # 外键
    skus = db.relationship('Sku')

    def save(self, article: str):
        current_app.logger.info('添加货架', article)

        self.article = article

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("添加货架成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"添加货架失败, article: {article}, err: {e}")
            return False
