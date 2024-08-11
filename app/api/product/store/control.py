from app.api.product.store.common import add_store, reduce_store


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
        add_store(
            shelf_article=shelf_article,
            skc_article=skc_article,
            sku_article=sku_article,
            times=1
        )
    elif mode == 'reduce':
        reduce_store(
            shelf_article=shelf_article,
            skc_article=skc_article,
            sku_article=sku_article,
            times=1
        )
    else:
        raise Exception(f'更改一个sku的库存时，参数不符规则，mode: {mode}')