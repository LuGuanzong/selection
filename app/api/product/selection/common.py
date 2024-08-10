from app.extension.db import db
from app.model.sql.product.skc import Skc
from app.model.sql.product.sku import Sku
from app.model.sql.product.shelf import Shelf
from app.model.sql.product.shelf_and_sku import ShelfAndSku


def generate_xp_article() -> str:
    """
    生成选品的货号
    :return: str 货号
    """
    pass


def process_st_by_row(row: dict, selection_cp: dict) -> dict:
    """
    通过前端解析过的xlsx文件选品数组的每一行录入单个选品
    :param row: 单个选品数据
    :param selection_cp: 上一个品的选品数据
    :return: 这个品的选品数据
    """
    # 每一列的列名，‘备注’除外
    key_list = ['sku号', '商品', '型号', '工厂', '成本单价', '类目', '货号', '链接', '备注']

    for k in key_list:
        if not row.get(k):
            row[k] = selection_cp.get(k)

    if not row.get('货号'):
        raise ValueError("货号为空")

    # 先判断数据库里面是否有这个货号
    existed_skc = Skc.query.filter(Skc.article == row['货号']).first()

    if existed_skc:  # 如果有这个货号，那么在对应的skc下存储sku
        Sku().save(
            skc_id=existed_skc.id,
            article=row.get('sku号'),
            style=row.get('型号'),
            cost=row.get('成本单价'),
            img_url=''
        )
    else:  # 如果没有这个货号，那么就存储这个skc，并在这一行下存储sku
        skc = Skc()
        success = skc.save(
            article=row.get('货号'),
            category_ch=row.get('类目'),
            factory=row.get('工厂'),
            name=row.get('商品'),
            order_link=row.get('链接'),
            remark=row.get('备注', '')
        )

        if not success:
            raise Exception('保存skc失败')

        Sku().save(
            skc_id=skc.id,
            article=row.get('sku号'),
            style=row.get('型号'),
            cost=row.get('成本单价'),
            img_url=''
        )

    return row


def get_sku_id_by_skc_sku(skc_article: str, sku_article: str) -> int:
    """
    通过skc的货号和sku的货号找到sku的id
    :param skc_article:
    :param sku_article:
    :return: sku的id
    """
    sku_id = db.session.query(Sku.id). \
        join(Skc, Sku.skc_id == Skc.id). \
        filter(Skc.article == skc_article). \
        filter(Sku.article == sku_article). \
        first()

    return sku_id or 0


def add_store(shelf_article: str, skc_article: str, sku_article: str, times: int) -> None:
    """
    增加单个货架的特定sku的库存
    :param shelf_article: 货架号
    :param skc_article: skc号
    :param sku_article: sku号
    :param times: 增加多少件
    :return: None
    """
    # 根据货架号找到货架id
    shelf = Shelf.query.filter_by(article=shelf_article).first()
    shelf_id = shelf.id

    # 根据skc和sku号找到sku的id
    sku_id = get_sku_id_by_skc_sku(skc_article, sku_article)

    # 校验参数
    if not shelf_id or not sku_id:
        raise Exception(f'更改单个货架的特定sku的库存时发现空参数，shelf_id: {shelf_id}, sku_id: {sku_id}')

    # 循环调用，增加sku库存数，每次增加一个
    for _ in range(times):
        ShelfAndSku().save(
            shelf_id=shelf_id,
            sku_id=sku_id
        )


def reduce_store(shelf_article: str, skc_article: str, sku_article: str, times: int) -> None:
    """
    减少单个货架的特定sku的库存
    :param shelf_article: 货架号
    :param skc_article: skc号
    :param sku_article: sku号
    :param times: 减少加多少件
    :return: None
    """
    # 判断减少单个货架的特定sku的库存是否大于0
    if times <= 0:
        raise Exception(f'减少单个货架的特定sku的库存时，减少的数量不合规，times: {times}')

    # 根据货架号找到货架id
    shelf = Shelf.query.filter_by(article=shelf_article).first()
    shelf_id = shelf.id

    # 根据skc和sku号找到sku的id
    sku_id = get_sku_id_by_skc_sku(skc_article, sku_article)

    # 校验参数
    if not shelf_id or not sku_id:
        raise Exception(f'减少单个货架的特定sku的库存存时发现空参数，shelf_id: {shelf_id}, sku_id: {sku_id}')

    # 查询当前货架该sku数量
    count = ShelfAndSku.query.\
        filter_by(sku_id=sku_id, shelf_id=shelf_id).\
        count()
    if count < times:
        raise Exception(f'当前库存数量不足以减少指定数量，count: {shelf_id}, times: {times}，shelf_id: {shelf_id}, sku_id: {sku_id}')

    # 搜索当前货架里所有该sku库存
    shelf_and_skus = ShelfAndSku.query.filter_by(ku_id=sku_id, shelf_id=shelf_id).all()
    # 循环调用，减少sku库存数，每次减少一个
    for i in range(times):
        shelf_and_skus[i].delete()
