from app.api.product.store import common as c


def process_change_one_store(shelf_article: str, skc_article: str, sku_article: str, mode: str):
    """
    更改一个sku的库存
    :param shelf_article: 货架
    :param skc_article: skc号
    :param sku_article: sku号
    :param mode: add\reduce,表示当前是加一还是减1
    :return: boolean， true为正常处理完毕
    """
    if mode == 'add':
        c.add_store(
            shelf_article=shelf_article,
            skc_article=skc_article,
            sku_article=sku_article,
            times=1
        )
    elif mode == 'reduce':
        c.reduce_store(
            shelf_article=shelf_article,
            skc_article=skc_article,
            sku_article=sku_article,
            times=1
        )
    else:
        raise Exception(f'更改一个sku的库存时，参数不符规则，mode: {mode}')


def search_sku_count(skc: str, sku: str) -> list:
    """
    查询指定sku在各个货架的数量
    :param skc: skc货号
    :param sku: sku货号
    :return: 从小到大排列的指定sku在各个货架的数量信息
    """
    sku_id = c.get_sku_id_by_skc_sku(skc, sku)
    return c.find_shelves_with_specified_sku_counts(sku_id)
