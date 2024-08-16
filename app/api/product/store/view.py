from flask import Blueprint, request

from app.api.product.store import control as ctl
from app.util.code import ResponseCode
from app.util.exception import UserException, handle_errors
from app.util.response import ResMsg

store_bp = Blueprint('store', __name__)


@store_bp.route('/change_one_store', methods=['POST'], endpoint='change_one_store')
@handle_errors('为指定sku在指定货架里增加或减少一个库存')
def change_one_store():
    """
    为指定sku在指定货架里增加或减少一个库存
    :return:
    """
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


@store_bp.route('/sku_count', endpoint='sku_count')
@handle_errors('查询指定sku在各个货架的数量')
def search_sku_count():
    """
    查询指定sku在各个货架的数量
    :return:
    """
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


@store_bp.route('/all_shelf', endpoint='all_shelf')
@handle_errors('获取所有货架号')
def get_all_shelf():
    """
    获取所有货架号
    :return:
    """
    # 参数定义
    data = request.args
    keyword = data.get('keyword', '')  # 搜索的关键词

    shelves = ctl.get_all_shelf(keyword)
    return ResMsg(code=ResponseCode.Success, data=shelves).data


@store_bp.route('/valid_store_for_mat', endpoint='get_valid_store_for_mat')
@handle_errors('获取最长边为40厘米或50厘米的库存空位预测')
def get_valid_for_mat():
    """
    获取最长边为40厘米或50厘米的库存空位预测
    :return:
    """
    # 参数定义
    data = request.args
    longest = str(data.get('longest', ''))  # 最长边

    if longest not in ('40', '50'):
        return ResMsg(code=ResponseCode.InvalidParameter, msg='只支持最长边为40厘米或50厘米的地毯空位预测')

    rest_store_info = ctl.get_valid_store_for_mat(longest)

    return ResMsg(code=ResponseCode.Success, data=rest_store_info).data
