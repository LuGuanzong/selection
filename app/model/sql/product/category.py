from flask import current_app

from app.extension.db import db


class Category(db.Model):
    """
    品类表
    """
    __table_name__ = 'category'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.String(10), nullable=False, unique=True)  # 品类号
    name = db.Column(db.String(50), nullable=False, unique=True)  # 品类名

    def save(self, number:str, name: str):
        current_app.logger.info('创建品类', number, name)

        self.number = number
        self.name = name

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("创建品类成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"添加货架失败, number: {number}, name: {name}, err: {e}")
            return False

    def to_json(self):
        return dict(
            name=self.name,
            number=self.number
        )
