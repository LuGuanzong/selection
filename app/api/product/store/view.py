import logging

from flask import Blueprint, request

from app.api.product.store.control import process_change_one_store
from app.util.code import ResponseCode
from app.util.response import ResMsg


store_bp = Blueprint('store', __name__)


@store_bp.route('/change_one_store', methods=['POST'])
def change_one_store():
    """
    为指定sku在指定货架里增加或减少一个库存
    :return:
    """
    try:
        # 参数定义
        data = request.json
        mode = data.get('mode', 'add')  # add: 增加；reduce: 减少
        shelf_article = data.get('shelf', '')  # 货架号
        skc_article = data.get('skc', '')  # skc号
        sku_article = data.get('sku', '')  # sku号

        # 参数校验
        if mode not in ('add', 'reduce'):
            return ResMsg(code=ResponseCode.InvalidParameter, msg='mode参数错误').data
        if not shelf_article or not skc_article or not sku_article:
            return ResMsg(code=ResponseCode.InvalidParameter, msg='mode参数错误').data

        success = process_change_one_store(shelf_article, skc_article, sku_article, mode)
        if success:
            return ResMsg(code=ResponseCode.Success).data
        else:
            return ResMsg(code=ResponseCode.Fail).data
    except Exception as e:
        logging.error(f'为指定sku在指定货架里增加或减少一个库存失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='为指定sku在指定货架里增加或减少一个库存失败').data