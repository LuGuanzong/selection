from app.model.sql.product.skc import Skc
from app.model.sql.product.sku import Sku


def generate_xp_article() -> str:
    """
    生成选品的货号
    :return: str 货号
    """
    pass


def process_st_by_row(row: dict, selection_cp: dict) -> dict:
    """
    通过前端解析过的xlsx文件选品数组的每一行录入单个选品
    :param row: 单个选品数据
    :param selection_cp: 上一个品的选品数据
    :return: 这个品的选品数据
    """
    # 每一列的列名，‘备注’除外
    key_list = ['sku号', '商品', '型号', '工厂', '成本单价', '类目', '货号', '链接', '备注']

    for k in key_list:
        if not row.get(k):
            row[k] = selection_cp.get(k)

    if not row.get('货号'):
        raise ValueError("货号为空")

    # 先判断数据库里面是否有这个货号
    existed_skc = Skc.query.filter(Skc.article == row['货号']).first()

    if existed_skc:  # 如果有这个货号，那么在对应的skc下存储sku
        Sku().save(
            skc_id=existed_skc.id,
            article=row.get('sku号'),
            style=row.get('型号'),
            cost=row.get('成本单价'),
            img_url=''
        )
    else:  # 如果没有这个货号，那么就存储这个skc，并在这一行下存储sku
        skc = Skc()
        success = skc.save(
            article=row.get('货号'),
            category_ch=row.get('类目'),
            factory=row.get('工厂'),
            name=row.get('商品'),
            order_link=row.get('链接'),
            remark=row.get('备注', '')
        )

        if not success:
            raise Exception('保存skc失败')

        Sku().save(
            skc_id=skc.id,
            article=row.get('sku号'),
            style=row.get('型号'),
            cost=row.get('成本单价'),
            img_url=''
        )

    return row
