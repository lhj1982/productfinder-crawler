import requests
import logging
import datetime
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import Product

_logger = logging.getLogger(__name__)


def generate_url_for_launches_with_page(pages, start_date, end_date):
    if pages.get('next') is None:
        return (f'https://edge-int.prod.commerce.nikecloud.com.cn/launch/launches/v2?'
                f'filter=startEntryDateAfter({start_date})'
                f'&filter=startEntryDateBefore({end_date})'
                f'&filter=channel(SNKRS,SNKRSWEB,SNKRSPASS,NIKEAPP,NIKECOM)'
                f'&filter=draft(false)')
    else:
        next_filters = pages.get('next')
        return f'https://edge-int.prod.commerce.nikecloud.com.cn/launch/launches/v2?{next_filters}'


def get_launches(oscar_token, start_date, end_date):
    launches = []
    if oscar_token is not None and oscar_token != '':
        headers = {
            'Authorization': f'Bearer {oscar_token}',
            'x-current-user': '{"firstname":"productfinder-crawler","lastname":"productfinder-crawler",'
                              '"email":"productfinder-crawler","groups":["Lst-Commerce.Frame.Test.Launch.View",'
                              '"Lst-Commerce.Frame.Prod.Launch.View"]}'
        }
        pages = {}
        request_number = 0
        while True:
            url = generate_url_for_launches_with_page(pages, start_date, end_date)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                pages = response.json().get('pages')
                launches.extend(response.json().get('objects'))
            request_number += 1
            if request_number >= 50 or pages.get('next') is None:
                break
    return launches


def get_product(product_id, oscar_token):
    headers = {
        'Authorization': f'Bearer {oscar_token}'
    }
    params = {
        'sort': 'publishedContent.viewStartDateDesc',
        'filter': [
            'marketplace(CN)',
            'language(zh-Hans)',
            'channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647,008be467-6c78-4079-94f0-70e2d6cc4003)',
            'exclusiveAccess(true,false)',
            f'productInfo.merchProduct.id({product_id})'
        ]
    }
    response = requests.get('https://api.nike.com.cn/product_feed/threads/v3/secured', headers=headers, params=params)
    if response.status_code == 200 and len(response.json().get('objects')) > 0:
        return response.json().get('objects')[0]
    else:
        raise ValueError(f'No product found for product id {product_id}')


def search_launches(oscar_token):
    now = datetime.utcnow()
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    hour_after_24 = current_hour + timedelta(hours=7 * 24)
    start_date = current_hour.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_date = hour_after_24.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return get_launches(oscar_token, start_date, end_date)


def search_product_from_db(engine, style_color):
    with Session(engine) as session:
        products = session.query(Product).filter(Product.stylecolor == style_color).all()
    return products


def convert_feed_to_product(feed, product_id):
    style_color = ''
    label_name = ''
    current_price = 0
    image_url = ''

    product_content = feed.get('publishedContent') if feed is not None else None
    product_info = feed.get('productInfo') if feed is not None else None
    if product_info is not None and len(product_info) > 0:
        for info in product_info:
            merch_price = info.get('merchPrice')
            info_product_id = merch_price.get('productId') if merch_price is not None else None
            if info_product_id == product_id:
                current_price = merch_price.get('currentPrice') if merch_price.get('currentPrice') is not None else 0
                merch_product = info.get('merchProduct')
                style_color = merch_product.get('styleColor') if merch_product is not None else ''
                label_name = merch_product.get('labelName') if merch_product is not None else ''
                break

    if product_content is not None:
        nodes = product_content.get('nodes')
        if nodes is not None and len(nodes) > 0:
            content_nodes = nodes[0].get('nodes') if nodes[0] is not None and len(nodes[0]) > 0 else None
            image_node = content_nodes[0] if content_nodes is not None and len(content_nodes) > 0 else None
            image_properties = image_node.get('properties') if image_node is not None else None
            image_url = image_properties.get('squarishURL') if image_properties is not None else ''

    if style_color is None or style_color == '':
        raise ValueError("No product info is found")
    else:
        return {
            'style_color': style_color,
            'label_name': label_name,
            'current_price': current_price,
            'image_url': image_url
        }


def insert_product(engine, product):
    china_utc_offset = timedelta(hours=8)
    current = datetime.utcnow()
    china_current = current + china_utc_offset
    try:
        with Session(engine) as session:
            insert_query = text("""
                insert into products (stylecolor, name, price, url, created_at,enabled)
                values (:stylecolor , :name , :price , :url , :create_at , :enabled)
            """)
            session.execute(insert_query, {
                'stylecolor': product.get('style_color'),
                'name': product.get('label_name'),
                'price': product.get('current_price'),
                'url': product.get('image_url'),
                'create_at': china_current,
                'enabled': 1
            })
            session.commit()
    except Exception as e:
        _logger.error('Error when syncing product information , error: %s', e)


def insert_launches(engine, oscar_token):
    launches = search_launches(oscar_token)
    for launch in launches:
        try:
            forecasted_visitors = launch.get('forecastedVisitors')
            if forecasted_visitors is not None and forecasted_visitors >= 200000:
                product_id = launch.get('productId')
                feed = get_product(product_id, oscar_token)
                product = convert_feed_to_product(feed, product_id)
                db_products = search_product_from_db(engine, product.get('style_color'))
                if db_products is not None and len(db_products) > 0:
                    _logger.info('this styleColor already exists in db, styleColor: %s, launchId: %s',
                                 product.get('style_color'), launch.get('id'))
                else:
                    insert_product(engine, product)
            else:
                _logger.info(
                    'skip this launch due to the forecast number is too low, launchId: %s, forecastedVisitors: %s',
                    launch.get('id'), launch.get('forecastedVisitors'))
        except Exception as e:
            _logger.error('Error when syncing launch product to db, launchId: %s error: %s', launch.get('id'), e)
