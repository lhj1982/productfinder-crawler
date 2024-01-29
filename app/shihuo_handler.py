import requests
import logging
import itertools
from .models import ProductReview
from datetime import datetime
from sqlalchemy.orm import Session
from time import sleep

_logger = logging.getLogger("app")


def add_comment_for_product(engine, product):
    style_color = product.stylecolor
    search_product = search_style_color(style_color)
    if check_product(search_product):
        list = discussion_list(search_product)
        for discussion in list:
            product_reviews = comment_list(discussion, product)
            try:
                with Session(engine) as session:
                    session.add_all(product_reviews)
                    session.commit()
            except Exception as e:
                _logger.warning('Error when updating db, error: %s', e)
            sleep(1)


def search_style_color(style_color):
    response = requests.post(
        "https://sh-gateway.shihuo.cn/v3/sh-api/daga/search/goods/v1",
        params={
            "platform": "ios",
            "timestamp": "1687937374689",
            "token": "6d270d01afc9ccaeacd57e6b4fa132fe",
            "v": "7.46.1"
        },
        headers={
            'Host': 'sh-gateway.shihuo.cn',
            'Cookie': 'JSESSIONID=BAF9F1AE43DEBA1E56BB79A27FF188C5',
            'sh-sign': '1A6B7CD77FF4298142EEADBC1F9FC864',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 network/wifi shihuo/7.46.1 iPhone13,2 sc(699b35e8082ec37947237ba3ad5ed1a4,appstore) iPhone 12',
            'sh-ba': 'V9UuQSoggaODk1MjAwZTQ4NmRhOGI5ZTYyR71I/TDK3XasNZYKbyOXFIgzGVJI6LkOAxO479os4DyXeJQQHxEC6jEtYn3i9rafvAfVSlj+FbTOwWU9EketmU+ae8joMMHI++fPPeUV7sXaq7IWDFldb2HPylnAnK6PDMfJa1GbEW66RUkU93AxXFgUor4w2jidhNOtKAdOmkwRU6YsoL6r7dT1i7IAjcNU0/huIdtLHf1qn6H3K9Sv3r6+3Ng3H1SG533WppOLnfXwnKn80e8Tb5n5UIzj4fg+',
            'sh-jt': 'YTqy7iqUOhMjg0MGIwZmZiY2ExN2M3NDA548TwZJUAYw06DvXQtTxmH2mgFoYGURWmNao3pK2TquJt+T3U7lyJjF3ynl8maOYisFWopme9+5UpKm66ZR/Bmw==',
            'app-v': '7.46.1',
            'daga-ban-personal': '0',
            'osv': '16.5',
            'sh-token': 'RTMezILg8XMTNlMmQwOTI5OTU3YzZiYWUxtCmwEYVCdfv7bj8ZpEssWVyEPeiIBNZbjYKQ5AmIPjBQlD8EEWrW1reiMgTu9+0fS9YdiEkX/4oZTO3rpsBXjxL07a+U3YOJRmD2ho7RTNFuVUQITV3vxinosnD/UKfPDpvOyANcuCCzIPOrGP6VL4wv6OUbTt2MyJgWX+t8xucOBfhn60bMBfAZ5rpTjHE0WbtYGOktBWd5ErN9MvzyNa/HOIgBLaIn/YpCccWL4KxT5BwH4lMnJiowrYX3vbiZV44gJ3NqNwwJ4A2mltv7/CZRFKj5tVn3q3jdEMm+61pwNPS4m7XfathtwEnxuaWv4jWVKLK3tIfAxNYZ9OoW679oKoX0JKtLqu45mbXD37bYlFUnR8Q9VruF+n+/TTpPogUwDxkdnx8RqDxXLFTiLQ==',
            'sh-id': '5mw29yrly88b6c19cd5dcd8fa903c83d',
            'platform': 'ios',
            'timestamp': '1687937374688',
            'sh_session': 'EE7FC9A7-0E96-47A2-A4D5-C849DDF20865_active_599575',
            'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'network': '1',
            'sk': '9MHVBULPWPoKQLVowM8N2POFTcpWomTVHZuusBFHNTTQj9d8UWbj26KKIh5puX7keBjnUvhHv6PFjXnUmoNdtKOqxn1y',
            'sign-data': 'kxuBeQHaedOh_sh-McOGQQACAXJRrbtHy4UDryYc09sBqDujndsZL-Ybtb6lVrR_vmty',
            'content-type': 'application/json',
            'shreqid': '3c8a47bddfb157b3',
            'accept': '*/*',
            'pragma': 'no-cache',
            'cache-control': 'no-cache'
        },
        json={
            "needAttrs": 1,
            "page": 1,
            "route": "homeSearchList",
            "pageContext": "{\"pageId\":\"SHGoodsSearchModule.SHGlobalSearchViewController_1f6096e394a6e623\",\"ptiRoot\":{\"biz\":\"\",\"pageId\":\"appHome_7c448c08546c596b\",\"toInfo\":{\"back_keywords\":\"音速11\"},\"name\":\"\",\"pageOptions\":{\"is_new_version\":\"1\",\"haveSkin\":\"0\"},\"id\":\"home:searchInput\"},\"layer\":1}",
            "predictSex": "2",
            "pageSize": 10,
            "lspm": "922d9361b44a9285",
            "sort": "hot",
            "keywords": style_color,
            "preload": "1"
        })
    search_product = {
        'style_color': style_color
    }
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        if data is not None:
            lists = data.get('lists')
            if lists is not None and len(lists) > 0:
                style_lists = lists[0].get('style_lists')
                if style_lists is not None and len(style_lists) > 0:
                    product = style_lists[0]
                    search_product['goods_id'] = product.get('goods_id')
                    search_product['style_id'] = product.get('style_id')
    else:
        _logger.error('search the product request error, style color: %s', style_color)
    return search_product


def check_product(search_product):
    response = requests.get(
        "https://sh-gateway.shihuo.cn/v4/services/sh-goodsapi/public/showcase/attr",
        params={
            "goods_id": search_product.get('goods_id'),
            "style_id": search_product.get('style_id'),
            "v": "7.46.1"
        },
        headers={
            'platform': 'ios',
            'sk': '9MHVBULPWPoKQLVowM8N2POFTcpWomTVHZuusBFHNTTQj9d8UWbj26KKIh5puX7keBjnUvhHv6PFjXnUmoNdtKOqxn1y',
            'Host': 'sh-gateway.shihuo.cn',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 network/wifi shihuo/7.46.1 iPhone13,2 sc(699b35e8082ec37947237ba3ad5ed1a4,appstore) iPhone 12'
        })
    check = False
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        if data is not None:
            list = data.get('list')
            if list is not None and len(list) > 0:
                style_color_data = list[0]
                value = style_color_data.get('value')
                if value is not None and len(value) > 0:
                    check = value[0].upper() == search_product.get('style_color')
    else:
        _logger.error('check product request error, style color: %s', search_product.get('style_color'))
    return check


def discussion_list(search_product):
    list = []
    for i in itertools.count():
        page = i + 1
        request_lists = discussion_list_request(search_product.get('goods_id'), search_product.get('style_id'), page,
                                                search_product.get('style_color'))
        if request_lists is not None and len(request_lists) > 0:
            list += request_lists
        else:
            break
    return list


def discussion_list_request(goods_id, style_id, page, style_color):
    _logger.info('discussion list request, page: %s', page)
    response = requests.get(
        "https://sh-gateway.shihuocdn.cn/v4/services/sh-gocommunity/x/v1/goods/talked-list",
        params={
            "platform": "ios",
            "v": "7.46.1",
            "goods_id": goods_id,
            "style_id": style_id,
            "page": page,
            "tag_id": 0
        },
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 network/wifi shihuo/7.46.1 iPhone13,2 sc(699b35e8082ec37947237ba3ad5ed1a4,appstore) iPhone 12"
        })
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        if data is not None:
            return data.get('list')
    else:
        _logger.error('discussion list request error, style color: %s', style_color)
    return []


def discussion_detail(style_color, discussion_id):
    response = requests.get(
        "https://sh-gateway.shihuocdn.cn/v4/services/sh-gocommunity/x/v1/note/detail/v2",
        params={
            "id": discussion_id
        })
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        if data is not None:
            list = data['list']
            if list is not None:
                return list.get('data')
    else:
        _logger.error('discussion detail request error, style color: %s, id: %s', style_color, discussion_id)
    return None


def comment_list(discussion, product):
    product_id = product.id
    list = []
    user_info = discussion.get('user_info')
    account_id = ""
    if user_info is not None and user_info.get('author_id') is not None:
        account_id = str(user_info.get('author_id'))
    for i in itertools.count():
        page = i + 1
        request_lists = comment_list_request(discussion['id'], page, 10, product.stylecolor)
        comment_lists = request_lists.get('comment')
        if comment_lists is not None and len(comment_lists) > 0:
            for comment in comment_lists:
                product_review = get_product_review_from_comment(product_id, account_id, comment)
                list.append(product_review)
                reply = comment.get('reply')
                if reply is not None and len(reply) > 0:
                    for reply_comment in reply:
                        reply_review = get_product_review_from_comment(product_id, account_id, reply_comment)
                        list.append(reply_review)
        else:
            break
    return list


def get_product_review_from_comment(product_id, account_id, comment):
    return ProductReview(
        account_id=account_id, product_id=product_id, text=comment['content'],
        timestamp=datetime.strptime(comment['created_at'], "%Y-%m-%d"),
        source='shihuo', like_count=comment['praise'], review_user_id=comment['user_id'],
        review_user_name=comment['user_name'])


def comment_list_request(discussion_id, page, page_size, style_color):
    response = requests.get(
        "https://sh-gateway.shihuocdn.cn/v4/services/sh-behaviorapi/app_swoole_comment/getComment/v2",
        params={
            "product_id": discussion_id,
            "page": page,
            "page_size": page_size,
            "type": 8
        })
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get('data')
    else:
        _logger.error('comment list request error, style color: %s, id: %s', style_color, discussion_id)
    return {}
