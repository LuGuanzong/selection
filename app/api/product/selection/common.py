from app.model.sql.product.skc import Skc
from app.model.sql.product.sku import Sku


def generate_xp_article():
    """
    生成选品的货号
    :return:
    """
    pass


def process_st_xlsx_by_row(row, article: str):
    """
    分析选品表格并存好选品数据时，对每一行进行分析
    :param article: 当前行的货物的货号，如果当前行没有，就会使用到这个参数；用上面最接近的货号作为本行产品货号
    :param row ws.iter_rows的返回值
    :return: 返回当前商品的货号
    """
    if row[0] and 'XP' not in row[0]:  # 防止第一行是列名
        return None

    if row[0]:  # 如果存在货号，那么这个商品的货号就是这个
        article = row[0]
    else:
        article = article

    if not article:  # 如果往上一直没有货号，就不处理了
        return None

    # 先判断数据库里面是否有这个货号
    already_exist = Skc.query.filter(Skc.article == article).first()

    if already_exist:  # 如果有这个货号，那么在对应的skc下存储sku
        Sku().save(
            skc_id=article,
            article=row[8],
            style=row[5],
            cost=row[6],
            img_url=''
        )
    else:  # 如果没有这个货号，那么就存储这个skc，并在这一行下存储sku
        Skc().save(
            article=article,
            category_ch=row[2],
            factory=row[1],
            name=row[4],
            order_link=row[5],
            remark=row[9]
        )
        Sku().save(
            skc_id=article,
            article=row[8],
            style=row[5],
            cost=row[6],
            img_url=''
        )

    return article
