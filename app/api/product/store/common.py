from sqlalchemy import func

from app.extension.db import db
from app.model.sql.product.shelf import Shelf
from app.model.sql.product.shelf_and_sku import ShelfAndSku
from app.model.sql.product.skc import Skc
from app.model.sql.product.sku import Sku
from app.util.exception import UserException
from app.util.store_bulk import Bulk


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

    if not sku_id:
        raise UserException('无法通过skc的货号和sku的货号找到对应sku')

    return sku_id[0]


def split_skc_sku(skc_sku: str) -> tuple:
    """
    把格式为{skc}-{sku}的拼接货号分割成skc和sku号
    :param skc_sku: {skc}-{sku}的拼接货号
    :return: 返回一个skc和sku的元祖 (skc, sku)
    """
    if not skc_sku:
        return '', ''

    sk_list = skc_sku.split('-')

    if len(sk_list) == 1:
        return sk_list[0], ''
    else:
        return sk_list[0], sk_list[1]


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
    shelf = Shelf.find_by_article(shelf_article)
    shelf_id = shelf.id

    # 根据skc和sku号找到sku的id
    sku_id = get_sku_id_by_skc_sku(skc_article, sku_article)
    print(sku_id)

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
    shelf = Shelf.find_by_article(shelf_article)
    shelf_id = shelf.id

    # 根据skc和sku号找到sku的id
    sku_id = get_sku_id_by_skc_sku(skc_article, sku_article)

    # 校验参数
    if not shelf_id or not sku_id:
        raise Exception(f'减少单个货架的特定sku的库存存时发现空参数，shelf_id: {shelf_id}, sku_id: {sku_id}')

    # 查询当前货架该sku数量
    count = ShelfAndSku.query_with_soft_delete(). \
        filter_by(sku_id=sku_id, shelf_id=shelf_id). \
        count()
    if count < times:
        raise UserException(f'当前库存数量不足以减少指定数量，count: {shelf_id}, times: {times}，shelf_id: {shelf_id}, sku_id: {sku_id}')

    # 搜索当前货架里所有该sku库存
    shelf_and_skus = ShelfAndSku.query_with_soft_delete().filter_by(sku_id=sku_id, shelf_id=shelf_id).all()
    # 循环调用，减少sku库存数，每次减少一个
    for i in range(times):
        shelf_and_skus[i].delete()


def find_shelves_with_specified_sku_counts(sku_id: int) -> list:
    """
    查询每个货架上指定SKU的数量，并按数量排序
    :param sku_id: 指定sku数量
    :return: 排好序的每个货架上的指定sku数量
    """
    # # 使用子查询来过滤出特定SKU的ShelfAndSku记录
    subquery = db.session.query(ShelfAndSku.shelf_id) \
        .filter(ShelfAndSku.sku_id == sku_id) \
        .filter(ShelfAndSku.deleted_at.is_(None)) \
        .subquery()

    # 主查询，使用子查询来过滤货架，并计算每个货架的SKU数量
    shelves_with_counts = db.session.query(
        Shelf.id,
        Shelf.article,
        func.count(subquery.c.shelf_id).label('sku_count')
    ).join(subquery, Shelf.id == subquery.c.shelf_id) \
        .group_by(Shelf.id, Shelf.article) \
        .order_by('sku_count')

    result = shelves_with_counts.all()

    return [dict(id=s[0], article=s[1], count=s[2]) for s in result]


def get_all_shelf(keyword: str = '') -> list:
    """
    获取所有货架号
    :param keyword: 货架号关键词
    :return: 货架号列表
    """
    shelves = Shelf.query_with_soft_delete().filter(Shelf.article.ilike(f'%{keyword}%')).all()

    return [shelf.article for shelf in shelves]


def get_invalid_room_for_mat(mat_40: int, mat_50: int):
    """
    获取当前货仓里，地垫已占据的空间
    :param mat_40: 最长边为40的地垫的数量
    :param mat_50: 最长边为50的地垫的数量
    :return: float
    """
    room_40 = Bulk.mat_rectangle_40 * mat_40
    room_50 = Bulk.mat_rectangle_50 * mat_50

    return room_40 + room_50


def get_valid_room_for_mat(article: str) -> float:
    """
    获取当前货仓针对于地垫剩余的空间
    :return: 剩余空间所占的比例
    """
    shelf = Shelf.find_by_article(article)
    count = dict(
        mat_40=0,
        mat_50=0
    )

    for shelf_and_sku in shelf.shelf_and_skus:
        if shelf_and_sku.deleted_at:
            continue

        if '31.5' in shelf_and_sku.sku.style:
            count['mat_50'] += 1
        elif '15.75' in shelf_and_sku.sku.style:
            count['mat_40'] += 1

    invalid_room = get_invalid_room_for_mat(count['mat_40'], count['mat_50'])

    return 1 - invalid_room


def get_shelf_products(shelf_article: str) -> list:
    """
    获取当前货仓具体有哪些产品
    :param shelf_article: 货仓号，即货仓的article
    :return:
    """
    res = list()

    shelf = Shelf.find_by_article(shelf_article)

    # 通过货架找到所有关联的 ShelfAndSku 实例
    shelf_and_skus = shelf.shelf_and_skus

    # 遍历 ShelfAndSku 实例，获取 Sku 和 Skc 信息
    unique_set = set()
    for shelf_and_sku in shelf_and_skus:
        sku = shelf_and_sku.sku
        product_info = sku.to_json(need_skc=True)

        # 去重
        skc_sku = f'{sku.skc.article}-{sku.article}'
        if skc_sku not in unique_set:
            unique_set.add(skc_sku)

            # 找出sku在指定仓库内的数量
            sku_count_in_shelf = ShelfAndSku.query_with_soft_delete().filter_by(shelf_id=shelf.id, sku_id=sku.id).count()
            product_info['sku_count_in_shelf'] = sku_count_in_shelf
            product_info['skc_sku'] = skc_sku

            res.append(product_info)

    return res

