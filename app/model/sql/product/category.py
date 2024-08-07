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

    # 外键相关
    skcs = db.relationship('Skc', back_populates='category')

    def save(self, number: str, name: str):
        current_app.logger.info(f'创建品类 {number}, {name}', number, name)

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

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        """
        通过中文名称找id
        :param name: 品类中文名
        :return: 品类数据库记录的id
        """
        with current_app.app_context():
            # 查找具有指定名称的品类
            category = cls.query.filter_by(name=name).first()
            if category:
                return category.id
            else:
                return 0

    @classmethod
    def get_number_by_name(cls, name: str) -> str:
        """
        通过中文名称找对应品类代码
        :param name: 品类中文名
        :return: 品类数据库记录的对应品类代码
        """
        with current_app.app_context():
            # 查找具有指定名称的品类
            category = cls.query.filter_by(name=name).first()
            if category:
                return category.number
            else:
                return ''

    def to_json(self) -> dict:
        return dict(
            name=self.name,
            number=self.number
        )
