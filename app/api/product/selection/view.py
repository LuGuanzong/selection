import logging
import os
import uuid

from flask import Blueprint, request

from app.api.product.selection.control import process_st_xlsx
from app.util.response import ResMsg
from app.util.code import ResponseCode
from app.util.upload import file_judge_invalid

selection_bp = Blueprint('selection', __name__)


@selection_bp.route('/upload_st_by_xlsx', methods=['GET'])
def upload_st_by_xlsx():
    """
    上传文件录入选品
    :return:
    """
    try:
        file_is_invalid = file_judge_invalid(request.files)
        if file_is_invalid:
            return file_is_invalid

        file = request.files['file']
        if file.filename.endswith('.xlsx'):
            filename = file.filename + str(uuid.uuid4())
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            success = process_st_xlsx()
            if success:
                return ResMsg(code=ResponseCode.Success).data
            else:
                return ResMsg(code=ResponseCode.Fail).data

        return ResMsg(code=ResponseCode.InvalidParameter).data
    except Exception as e:
        logging.error(f'上传文件录入选品失败, err: {e}')
        return ResMsg(code=ResponseCode.Fail, msg='上传文件录入选品失败').data
