import openpyxl as xl

from app.api.product.selection.common import process_st_xlsx_by_row


def process_st_xlsx(xlsx_path: str):
    """
    分析选品表格并存好选品数据
    :param xlsx_path: 选品表格，xlsx格式
    :return: boolean， true为正常处理完毕
    """
    wb = xl.load_workbook(xlsx_path)  # 加载一个现有的工作簿

    ws = wb.active  # 访问当前活动的工作表

    article = None
    for row in ws.iter_rows(values_only=True):  # values_only=True表示只获取单元格的值，不获取单元格对象
        # row是一个元组，包含了当前行的所有单元格的值
        article = process_st_xlsx_by_row(row, article)  # 把每一行数据存进数据库

    return True
