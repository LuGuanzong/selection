import logging

from flask import Blueprint, request

from app.api.product.selection.control import  process_st_by_array
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

        success = process_st_by_array(selection_list)
        if success:
            return ResMsg(code=ResponseCode.Success).data
        else:
            return ResMsg(code=ResponseCode.Fail).data
    except Exception as e:
        logging.error(f'批量录入选品失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='批量录入选品失败').data
