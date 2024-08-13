from flask import current_app

from app.extension.db import db
from app.model.sql.common import BaseModel
from app.util.exception import UserException


class Shelf(BaseModel):
    """
    货架表
    """
    __tablename__ = 'shelf'

    article = db.Column(db.String(30), nullable=False, unique=True)  # 货架号

    # 外键相关
    shelf_and_skus = db.relationship('ShelfAndSku', back_populates='shelf')

    def save(self, article: str):
            current_app.logger.info(f'添加货架 {article}')

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

    def to_json(self):
        return dict(
            article=self.article,
            count=self.shelf_and_skus.count(),  # 当前货仓货品数量
        )

    @classmethod
    def find_by_article(cls, shelf_article):
        """
        通过货架号查找货架
        :return: 返回货架
        """
        shelf = cls.query_with_soft_delete().filter_by(article=shelf_article).first()
        if not shelf:
            raise UserException(f'没有该货架：{shelf_article}')

        return shelf
