import logging

from flask import Blueprint, request

from app.api.product.selection import control as ctl
from app.util.response import ResMsg
from app.util.code import ResponseCode

selection_bp = Blueprint('selection', __name__)


@selection_bp.route('/upload_st_by_array', methods=['POST'])
def upload_st_by_array():
    """
    上传前端解析过的xlsx文件选品数组录入选品
    :return:
    """
    try:
        data = request.json
        selection_list = data.get('selection', [])

        success = ctl.process_st_by_array(selection_list)
        if success:
            return ResMsg(code=ResponseCode.Success).data
        else:
            return ResMsg(code=ResponseCode.Fail).data
    except Exception as e:
        logging.error(f'批量录入选品失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='批量录入选品失败').data


@selection_bp.route('/search_skus_by_keywords')
def search_skus_by_keywords():
    """
    通过空格间隔开的多个关键词，模糊匹配skc货号、skc商品名称、skc备注、sku货号、sku型号，返回对应sku信息；
    如果没有关键词，就返回空列表
    :return:
    """
    try:
        data = request.args
        keywords_str = data.get('keywords', '')

        if not keywords_str:
            return ResMsg(
                code=ResponseCode.Success,
                data=list()
            ).data

        # 把keywords通过空格分隔成字符串数组
        keywords_list = keywords_str.split()

        skus = ctl.search_skus_by_keywords(keywords_list)
        return ResMsg(
            code=ResponseCode.Success,
            data=skus
        ).data
    except Exception as e:
        logging.error(f'查询sku信息失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='查询sku信息失败').data
