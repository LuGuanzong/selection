from flask import Blueprint

from app.api.product.selection.view import selection_bp

product_bp = Blueprint('product', __name__)

product_bp.register_blueprint(selection_bp, url_prefix='/product')
