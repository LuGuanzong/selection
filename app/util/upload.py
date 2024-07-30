import os

from app.util.code import ResponseCode
from app.util.response import ResMsg


def file_judge_invalid(rq_files):
    """
    上传文件时判断请求中文件是否存在
    :param rq_files:request.files
    :return: 如果存在返回值，那就直接返回到前端错误信息
    """
    # 判断是否存在存放上传文件的文件夹
    uploads_dir = 'uploads'
    uploads_path = os.path.join(os.getcwd(), uploads_dir)
    if not os.path.exists(uploads_path):
        os.makedirs(uploads_path)
        print(f"Directory '{uploads_path}' created.")

    if 'file' not in rq_files:
        return ResMsg(code=ResponseCode.InvalidParameter).data
    file = rq_files['file']
    if file.filename == '' or not file:
        return ResMsg(code=ResponseCode.InvalidParameter).data

    return None
