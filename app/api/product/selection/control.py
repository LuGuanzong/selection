from app.api.product.selection import common as c


def process_st_by_array(selection_list: list) -> bool:
    """
    通过前端解析过的xlsx文件选品数组录入选品
    :param selection_list: 选品字典数组
    :return: boolean， true为正常处理完毕
    """
    if len(selection_list) == 0:
        return True

    selection_cp = selection_list[0]
    for selection in selection_list:
        selection_cp = c.process_st_by_row(selection, selection_cp)

    return True


def search_skus_by_keywords(keywords: list) -> list:
    """
    通过多个关键词搜索对应sku
    :param keywords: 关键词列表
    :return: sku信息列表
    """
    return c.search_skus_by_keywords(keywords)