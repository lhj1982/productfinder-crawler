"""Application handler."""
import logging
import _thread
from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import Product
from .models import ProductCrawlRecord
from .weibo_handler import get_product_reviews
from .shihuo_handler import add_comment_for_product
from datetime import datetime, time


_logger = logging.getLogger(__name__)


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
        _thread.start_new_thread(shihuo_crawl, (engine, product, current))


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


def update_product_rating(engine):
    """Update product rating"""
    rule_weights = {
        1: 0.9,  # price
        2: 0.1  # reviews
    }
    with Session(engine) as session:
        products = session.query(Product).filter(Product.enabled == 1).all()
        for product in products:
            rating = calc_rating(product, rule_weights)
            product.rating = rating
            # print(product)
        session.commit()


def calc_rating(product, rule_weights):
    from operator import itemgetter
    rating = 0
    price_score = 0
    review_score = 0
    for rule in rule_weights:
        weight = rule_weights[rule]
        if rule == 1:
            arr = []
            for price in product.prices:
                if price.price is not None or price.lastsaleprice is not None:
                    arr.append(
                        {"product_id": price.product_id, "price": price.price, 'lastsaleprice': price.lastsaleprice, "check_date": price.check_date})

            sorted_arr = sorted(
                arr, key=itemgetter('check_date'), reverse=True)
            if sorted_arr:  # not empty list
                highest_price_obj = sorted_arr[0]
                if highest_price_obj['price'] is not None:
                    market_price = highest_price_obj['price']
                else:
                    market_price = highest_price_obj['lastsaleprice']
                original_price = product.price

                # if product.id == 5:
                #     print('==============')
                #     print(highest_price_obj)
                #     print(original_price)
                price_score = market_price/(market_price+original_price)*100
                rating += price_score * weight

        elif rule == 2:
            count = len(product.reviews)
            if count > 0 and count <= 20:
                review_score = 50
            elif count > 20 and count <= 100:
                review_score = 80
            elif count > 100:
                review_score = 100
            rating += review_score * weight
    print(rating)
    return rating

def update_prices(engine):
    try:
        with Session(engine) as session:
            update_query = text("""
                UPDATE product_catalog.products p 
                SET p.release_date = (
                    SELECT STR_TO_DATE(max(lpp.releasedate), '%Y-%m-%d') 
                    FROM launch_bot_users.launch_productfinder_products lpp 
                    WHERE lpp.stylecolor = p.stylecolor 
                    GROUP BY lpp.stylecolor
                )
            """)
            session.execute(update_query)

            # 清空产品价格表
            truncate_query = text("TRUNCATE table product_catalog.product_prices")
            session.execute(truncate_query)

            # 插入产品价格信息
            insert_query = text("""
                INSERT INTO product_catalog.product_prices (product_id, price, retailprice, lastsaleprice, stockxlowestprice, stockxhighestprice, check_date) 
                SELECT 
                    (SELECT DISTINCT id FROM product_catalog.products p WHERE p.stylecolor = lpp.stylecolor) as product_id,
                    MAX(lpp.shihuoprice) as price,
                    MAX(lpp.retailprice) as retailprice,
                    MAX(lpp.lastsaleprice) as lastsaleprice,
                    MAX(lpp.stockxlowestprice) as stockxlowestprice,
                    MAX(lpp.stockxhighestprice) as stockxhighestprice,
                    FROM_UNIXTIME(lpp.searchtime div 1000, '%Y-%m-%d %h:%i:%s') as check_date
                FROM 
                    launch_bot_users.launch_productfinder_products lpp 
                WHERE 
                    (SELECT 1 FROM product_catalog.products p2 WHERE p2.stylecolor = lpp.stylecolor) 
                GROUP BY 
                    lpp.searchtime, lpp.stylecolor
            """)
            session.execute(insert_query)
            session.commit()
    except Exception as e:
        _logger.error('Error when syncing product information , error: %s', e)
