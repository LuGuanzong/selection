import os

from flask import current_app

from app.extension.db import db
from app.model.sql.common import BaseModel
from app.model.sql.product.shelf_and_sku import ShelfAndSku  # 保证关联表先定义


class Sku(BaseModel):
    """
    sku表
    """
    __tablename__ = 'sku'

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

    def to_json(self, with_skc: bool = False) -> dict:
        res = dict(
            sku_article=self.article,
            style=self.style,
            cost=self.cost,
            img_url=self.img_url,
            remark=self.remark,
            count=len(self.shelf_and_skus)  # 当前型号的商品在仓库里的数量
        )

        if with_skc:
            skc_json = self.skc.to_json()
            res.update(skc_json)

        return res

    def change_img(self, img_url: str = '', del_before: bool = False) -> bool:
        """
        更换图片
        :param img_url: 新的图片位置
        :param del_before: 是否需要删除之前的图片
        :return: True代表运行正常
        """
        # 如果要删除之前的图片，需要判断不为空，并且确定是指定文件夹下的文件，才能删除
        if del_before and self.img_url:
            img_before_path = os.path.join(current_app.config['UPLOAD_FOLDER'], self.img_url)
            if os.path.exists(img_before_path) and '..' not in img_before_path:
                os.remove(img_before_path)
            else:
                current_app.logger.error(
                    f"删除之前的图片失败, 请确认之前的图片是否合法, sku_id: {self.id}, img_before_path: {img_before_path}"
                )
                raise Exception('请确认之前的图片是否合法')

        self.img_url = img_url

        db.session.add(self)
        # 提交会话，保存数据到数据库
        try:
            db.session.commit()
            current_app.logger.info("更换sku图片成功")
            return True
        except Exception as e:
            db.session.rollback()  # 如果保存失败，回滚会话
            current_app.logger.error(f"更换sku图片失败, sku_id: {self.id}, img_url: {img_url}, err: {e}")
            return False
