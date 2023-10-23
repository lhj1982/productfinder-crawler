"""Application handler."""
import logging
# import requests
from flask import request, render_template, make_response
# from datetime import datetime as dt
# from flask import current_app as app
from sqlalchemy.orm import Session
from .models import Product
# from sqlalchemy import select
from .weibo_handler import get_product_reviews

# log = logging.getLogger("myapp")

# logging.basicConfig(level=logging.INFO,
# format="%(levelname)s | %(asctime)s | %(message)s")

_logger = logging.getLogger("app")


def get_products_from_db(engine):
    """Function printing python version."""
    with Session(engine) as session:
        products = session.query(Product).filter(Product.enabled == 1).all()
        # session.commit()
    return products


def update_product_reviews(engine):
    products = get_products_from_db(engine)
    _logger.info("Found products %s", products)
    for product in products:
        stylecolor = product.stylecolor
        _logger.info("Crawling content for %s ... ", stylecolor)
        product_reviews = get_product_reviews(engine, product)
        # search_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D" + \
        #     stylecolor + "&page_type=searchall"
        # response = requests.get(search_url)
        # response_obj = response.json()
        # print(response_obj.keys())
        # for card in response_obj['data']['cards']:
        #     anchor_id = card['anchorId']
        #     print(anchor_id)
