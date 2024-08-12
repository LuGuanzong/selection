import logging

from flask import Blueprint, request

from app.api.product.store import control as ctl
from app.util.code import ResponseCode
from app.util.exception import UserException
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

        success = ctl.process_change_one_store(shelf_article, skc_article, sku_article, mode)
        if success:
            return ResMsg(code=ResponseCode.Success).data
        else:
            return ResMsg(code=ResponseCode.Fail).data
    except UserException as e:
        logging.error(f'为指定sku在指定货架里增加或减少一个库存失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg=f'为指定sku在指定货架里增加或减少一个库存失败, {e}').data
    except Exception as e:
        logging.error(f'为指定sku在指定货架里增加或减少一个库存失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='为指定sku在指定货架里增加或减少一个库存失败').data


@store_bp.route('/search_sku_count')
def search_sku_count():
    """
    查询指定sku在各个货架的数量
    :return:
    """
    err_msg_prefix = '查询指定sku在各个货架的数量失败'

    try:
        # 参数定义
        data = request.args
        skc_article = data.get('skc', '')  # skc号
        sku_article = data.get('sku', '')  # sku号

        if not skc_article or not sku_article:
            raise UserException('请输入正确skc和sku号')

        shelves_with_sku_count = ctl.search_sku_count(
            skc=skc_article,
            sku=sku_article
        )
        return ResMsg(code=ResponseCode.Success, data=shelves_with_sku_count).data
    except UserException as e:
        logging.error(f'{err_msg_prefix}, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg=f'{err_msg_prefix}, {e}').data
    except Exception as e:
        logging.error(f'{err_msg_prefix}, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg=f'{err_msg_prefix}').data