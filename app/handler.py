"""Application handler."""
import logging
from sqlalchemy.orm import Session
from .models import Product
from .models import ProductCrawlRecord
from .weibo_handler import get_product_reviews
from .shihuo_handler import add_comment_for_product
from datetime import datetime, time

_logger = logging.getLogger("app")


def get_products_from_db(engine):
    """Function printing python version."""
    with Session(engine) as session:
        products = session.query(Product).filter(Product.enabled == 1).all()
    return products


def update_product_reviews(engine):
    current = datetime.combine(datetime.now().date(), time.min)
    products = get_products_from_db(engine)
    _logger.info("Found products %s", products)
    for product in products:
        _logger.info("Crawling content for %s ... ", product.stylecolor)
        weibo_crawl(engine, product, current)
        shihuo_crawl(engine, product, current)


def weibo_crawl(engine, product, current):
    platform = 'weibo'
    record = get_crawl_record(engine, product, current, platform)
    if record is None:
        try:
            get_product_reviews(engine, product)
            add_crawl_record(engine, product, current, platform)
        except Exception as e:
            _logger.error('Error when crawl %s, platform: %s, time: %s, error: %s', product.stylecolor, platform,
                          current, e)
    else:
        _logger.info(
            'skipping this crawling process for %s, because the data has already been crawled! platform: %s, time: %s',
            product.stylecolor, platform, current)


def shihuo_crawl(engine, product, current):
    platform = 'shihuo'
    record = get_crawl_record(engine, product, current, platform)
    if record is None:
        try:
            add_comment_for_product(engine, product)
            add_crawl_record(engine, product, current, platform)
        except Exception as e:
            _logger.error('Error when crawl %s, platform: %s, time: %s, error: %s', product.stylecolor, platform,
                          current, e)
    else:
        _logger.info(
            'skipping this crawling process for %s, because the data has already been crawled! platform: %s, time: %s',
            product.stylecolor, platform, current)


def get_crawl_record(engine, product, current, platform):
    with Session(engine) as session:
        record = session.query(ProductCrawlRecord).filter(ProductCrawlRecord.product_id == product.id,
                                                          ProductCrawlRecord.platform == platform,
                                                          ProductCrawlRecord.crawl_time == current).first()
    return record


def add_crawl_record(engine, product, current, platform):
    record = ProductCrawlRecord(product_id=product.id, stylecolor=product.stylecolor, platform=platform,
                                crawl_time=current)
    with Session(engine) as session:
        session.add(record)
        session.commit()
