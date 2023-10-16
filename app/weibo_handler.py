"""Weibo crawler handler."""
import logging
from time import sleep
import re
from datetime import datetime
import requests
from sqlalchemy.orm import Session
from .models import ProductReview

_logger = logging.getLogger("app")


def get_product_reviews(engine, product):
    """Get product reviews by stylecolor from weibo"""
    product_reviews = []
    stylecolor = product.stylecolor
    account_ids = get_product_review_account_ids(stylecolor)
    for account_id in account_ids:
        product_reviews = get_product_review_by_account_id(
            account_id, product)
        try:
            with Session(engine) as session:
                session.add_all(product_reviews)
                session.commit()
        except Exception as e:
            _logger.warning('Error when updating db, error: %s', e)
        # product_reviews.append(product_review)

        sleep(3)  # wait 3 seconds between requests
    return product_reviews


def get_product_review_account_ids(stylecolor):
    """Find review accounts by a given stylecolor"""
    search_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D" + \
        stylecolor + "&page_type=searchall"
    response = requests.get(search_url, timeout=10)
    response_obj = response.json()
    # print(response_obj.keys())
    anchors = []
    for card in response_obj['data']['cards']:
        card_type = card['card_type']
        if card_type == 9:
            anchor_id = card['anchorId']
            anchors.append(anchor_id)
        elif card_type == 11:
            for group in card['card_group']:
                if group['card_type'] == 9:
                    anchors.append(group['anchorId'])
                    break
    account_ids = []
    for anchor in anchors:
        p = re.compile('mid=([0-9]{16})&')
        result = p.search(anchor)
        try:
            account_ids.append(result[1])
        except Exception as e:
            _logger.warn(
                'Error when capture account id from %s, error: %s', anchor, e)
    return account_ids


def get_product_review_by_account_id(account_id, product):
    """Get product reivew by account id"""
    stylecolor = product.stylecolor
    product_id = product.id
    _logger.info('Crawling reviews for account %s, stylecolor: %s ...',
                 account_id, stylecolor)
    acount_detail_url = f"https://m.weibo.cn/comments/hotflow?id={account_id}&mid={account_id}&max_id_type=0"
    product_reviews = []
    try:
        response = requests.get(acount_detail_url, timeout=10)
        response_obj = response.json()
        status = response_obj['ok']
        if status == 1:
            # print(response_obj['data']['data'])
            for data in response_obj['data']['data']:
                datetime_object = datetime.strptime(
                    data['created_at'], '%a %b %d %H:%M:%S %z %Y')
                print(data['text'])
                review_user = data['user']
                product_review = ProductReview(
                    account_id=account_id, product_id=product_id, text=data['text'], timestamp=datetime_object, source='weibo', like_count=data['like_count'], review_user_id=review_user['id'], review_user_name=review_user['screen_name'])
                # product_review.product = product
                product_reviews.append(product_review)
        else:
            print('No data')
    except Exception as e:
        _logger.warn(
            f'Error when crawling reviews for account {account_id}, stylecolor: {stylecolor}, error: {e}')
    # print(product_reviews)
    return product_reviews
