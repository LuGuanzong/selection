from app.extension.db import db


class Category(db.Model):
    """
    品类表
    """
    __table_name__ = 'categorios'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.String(10), nullable=False, unique=True)  # 品类号
    name = db.Column(db.String(50), nullable=False, unique=True)  # 品类名

    def to_json(self):
        return dict(
            name=self.name,
            number=self.number
        )
