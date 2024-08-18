from flask import current_app

from app.extension.db import db
from app.model.sql.common import BaseModel
from app.model.sql.product.shelf import Shelf


class ShelfAndSku(BaseModel):
    """
    货架和sku联表
    """
    __tablename__ = 'shelf_and_sku'

    # 外键
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'), nullable=False)  # 货架的ID
    shelf = db.relationship('Shelf', back_populates='shelf_and_skus')
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'), nullable=False)  # SKU的ID
    sku = db.relationship('Sku', back_populates='shelf_and_skus')

    def save(self, sku_id: int, shelf_id: str):
        current_app.logger.info(f'商品存入货架, sku_id: {sku_id}, shelf_id: {shelf_id}')

        self.shelf_id = shelf_id
        self.sku_id = sku_id

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("商品存入货架成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"商品存入货架失败, sku_id: {sku_id}, shelf_id: {shelf_id}, err: {e}")
            return False
