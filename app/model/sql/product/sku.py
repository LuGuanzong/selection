from flask import current_app

from app.extension.db import db
from app.model.sql.common import Time
from app.model.sql.product import shelf_and_sku  # 保证关联表先定义


class Sku(db.Model, Time):
    """
    sku表
    """
    __table_name__ = 'sku'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article = db.Column(db.String(30), nullable=False)  # 货号
    style = db.Column(db.String(100), nullable=False)  # 型号
    cost = db.Column(db.String(20), nullable=False)  # 成本
    img_url = db.Column(db.Text)  # 图片链接
    remark = db.Column(db.String(250))  # 备注

    # 外键
    skc_id = db.Column(db.Integer, db.ForeignKey('skc.id'), nullable=False)
    skc = db.relationship('Skc', back_populates='skus')

    shelf_and_skus = db.relationship('ShelfAndSku', back_populates='sku')

    def save(self, skc_id: str, article: str, style: str, cost: str, img_url: str):
        current_app.logger.info(f'添加sku {article}, {style}, {cost}, {img_url}', )

        self.skc_id = skc_id
        self.article = article
        self.style = style
        self.cost = cost
        self.img_url = img_url

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("添加sku成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"添加sku失败, skc_id: {skc_id}, article: {article}, err: {e}")
            return False

    def to_json(self):
        return dict(
            article=self.article,
            style=self.style,
            cost=self.cost,
            img_url=self.img_url,
            remark=self.remark,
            count=self.shelf_and_skus.count()  # 当前型号的商品在仓库里的数量
        )
