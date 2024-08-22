import os
import uuid

from flask import current_app

from app.api.product.selection import common as c
from app.api.product.store import common as c_store
from app.util.exception import UserException


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


def upload_st_imgs(file, matching):
    """
    上传sku的图片，根据图片文件不带后缀的名称进行匹配
    :param file: request.files['file']
    :param matching: skcsku-匹配的方式为{skc号}-{sku号}；style-匹配的方式为型号的中文
    :return:
    """
    filename = file.filename

    is_img = c.judge_is_img(filename)
    if not is_img:
        raise UserException('上传的文件需要是图片')

    sku_id_set = set()
    name, extension = os.path.splitext(filename)
    if matching == 'style':  # 通过中文型号匹配图片
        sku_id_set = c.get_sku_id_set_by_matching_style(style=name)
    elif matching == 'skcsku':  # 通过{skc号}-{sku号}的文件名称找到sku的id
        skc, sku = c_store.split_skc_sku(name)
        sku_id = c_store.get_sku_id_by_skc_sku(skc, sku)
        sku_id_set.add(sku_id)

    # 给文件一个新的名称
    new_filename = str(uuid.uuid4()) + extension
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    file.save(filepath)  # 保存文件

    # 同一张图片可能会关联不同规格的sku
    for sku_id in sku_id_set:
        c.save_sku_img(sku_id=sku_id, filename=new_filename)
