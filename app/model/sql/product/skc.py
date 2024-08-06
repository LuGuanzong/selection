import json

from flask import current_app

from app.extension.db import db
from app.model.sql.common import Time
from app.model.sql.product.category import Category  # 保证提前初始化好关联的表


class Skc(db.Model, Time):
    """
    skc表
    """
    __table_name__ = 'skc'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article = db.Column(db.String(30), nullable=False, unique=True)  # 货号
    factory = db.Column(db.String(50), nullable=False)  # 工厂名
    name = db.Column(db.String(100), nullable=False)  # 商品名称
    order_link = db.Column(db.Text)  # 订购链接
    tags = db.Column(db.Text)  # 使用 TEXT 类型存储 JSON 数据 ,是一个标签字符串数组
    remark = db.Column(db.String(250))  # 备注

    # 外键
    skus = db.relationship('Sku')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')

    def save(self, article: str, category_ch: str, factory: str, name: str, order_link: str, remark: str):
        current_app.logger.info('添加skc', article, factory, name, order_link, remark)

        from app.model.sql.product.category import Category

        self.article = article
        self.factory = factory
        self.name = name
        self.order_link = order_link
        self.remark = remark
        self.category_id = Category.get_id_by_name(category_ch)

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("添加skc成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"添加skc失败, article: {article} err: {e}")
            return False

    def to_json(self, need_sku=None):
        base_json = dict(
            article=self.article,
            factory=self.factory,
            name=self.name,
            order_link=self.order_link,
            tags=json.loads(self.tags),
            remark=self.remark,
        )

        if not need_sku:
            return base_json
        else:
            return base_json.update(dict(
                skus=[sku.to_josn for sku in self.skus]
            ))
