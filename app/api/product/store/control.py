from app.api.product.store import common as c
from app.util.store_bulk import Bulk


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

    return True


def search_sku_count(skc: str, sku: str) -> list:
    """
    查询指定sku在各个货架的数量
    :param skc: skc货号
    :param sku: sku货号
    :return: 从小到大排列的指定sku在各个货架的数量信息
    """
    sku_id = c.get_sku_id_by_skc_sku(skc, sku)
    return c.find_shelves_with_specified_sku_counts(sku_id)


def get_all_shelf(keyword: str) -> list:
    """
    获取所有货架号
    :param keyword 进行匹配的关键词
    :return:
    """
    return c.get_all_shelf(keyword)


def get_valid_store_for_mat(longest: str) -> list:
    """
    获取最长边40厘米或最长边50厘米的地垫的仓库空位
    :param longest 进行匹配的关键词
    :return:
    """
    res = list()

    # 判断当前的地垫最长边是40还是50
    if longest == '50':
        mat_room = Bulk.mat_rectangle_50
    else:
        mat_room = Bulk.mat_rectangle_40

    # 找到所有货仓
    shelves = c.get_all_shelf()

    # 判断每个货仓是否能装下指定地毯和可以装下多少地毯
    for article in shelves:
        rest_room = c.get_valid_room_for_mat(article)  # 找出剩下的空间

        if rest_room > mat_room:
            count = rest_room // mat_room
            res.append(dict(
                article=article,
                count=count,
                more=c.get_which_mat_more(article)
            ))

    return res


def get_shelf_products(shelf_article: str) -> list:
    """
    获取当前仓位具体存储的货品
    :param shelf_article: 货架号
    :return:
    """
    return c.get_shelf_products(shelf_article)
