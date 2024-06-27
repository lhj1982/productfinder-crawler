import json
import logging
from flask import Flask
from sqlalchemy import create_engine
from .sync_launch_handler import get_launches
from .sync_launch_handler import get_product
from .sync_launch_handler import convert_feed_to_product
from .sync_launch_handler import search_product_from_db
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl

from .token_client import get_oscar_token

_logger = logging.getLogger(__name__)

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')


def send_slack_notification():
    global engine
    engine = create_engine(app.config.get(
        'SQLALCHEMY_DATABASE_URI'), echo=True)
    oscar_data = {
        'oscar_issuer': app.config.get('OSCAR_ISSUER'),
        'client_id': app.config.get('PRODUCT_FINDER_ID'),
        'client_secret': app.config.get('PRODUCT_FINDER_SECRET'),
        'scopes': app.config.get('TOKEN_SCOPES')
    }

    oscar_token = get_oscar_token(oscar_data)
    notification_objects = create_notification_objects(oscar_token)
    if notification_objects is not None and len(notification_objects) > 0:
        compose_message_and_send(notification_objects)
        _logger.info('Sent message to slack')
    else:
        _logger.info('No message send to slack')


def create_notification_objects(oscar_token):
    now = datetime.utcnow()
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    hour_after_24 = current_hour + timedelta(hours=24)
    start_date = current_hour.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_date = hour_after_24.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    launches = get_launches(oscar_token, start_date, end_date)
    slack_messages = []
    for launch in launches:
        try:
            product_id = launch.get('productId')
            feed = get_product(product_id, oscar_token)
            product = convert_feed_to_product(feed, product_id)
            db_products = search_product_from_db(engine, product.get('style_color'))
            if db_products is not None and len(db_products) > 0:
                _logger.info('this styleColor already exists in db, styleColor: %s, launchId: %s',
                             product.get('style_color'), launch.get('id'))

                if launch.get('forecastedVisitors') is not None and db_products[0].rating is not None:
                    trend = ""
                    if db_products[0].rating <= 49 and launch.get('forecastedVisitors') >= 200000:
                        trend = (":chart_with_downwards_trend:")
                    if db_products[0].rating >= 70 and launch.get('forecastedVisitors') <= 5000:
                        trend = (":chart_with_upwards_trend:")
                slack_message = {
                    'styleColor': product.get('style_color'),
                    'launchId': launch.get('id'),
                    'name': db_products[0].name,
                    'startDate': launch.get('startEntryDate'),
                    'forecast': launch.get('forecastedVisitors'),
                    'tier': launch.get('operationalTier'),
                    'score': db_products[0].rating,
                    'url': product.get('image_url'),
                    'trend': trend
                }
                slack_messages.append(slack_message)
                _logger.info(slack_messages)
            else:
                _logger.info('this styleColor does not exist in db, styleColor: %s, launchId: %s',
                             product.get('style_color'), launch.get('id'))
        except Exception as e:
            _logger.error('Error when getting launch product from db, launchId: %s error: %s', launch.get('id'), e)
    return slack_messages


def compose_message_and_send(notification_objects):
    now = datetime.utcnow()
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    hour_after_24 = current_hour + timedelta(hours=24)
    start_date = current_hour.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_date = hour_after_24.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    for notification_object in notification_objects:
        attachments = []
        attachment = {
            "color": "#50C878",
            "blocks": []
        }
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<https://adminops-int.prod.commerce.nikecloud.com.cn/launchadminv3/launches/list?start={start_date}&end={end_date}|{notification_object['styleColor']}> \n *LaunchId:* {notification_object['launchId']} \n *Name:* {notification_object['name']}  \n *StartDate:* {notification_object['startDate']} \n *Forecast:* {notification_object['forecast']} \n *Tier:* {notification_object['tier']} \n *Score:* {notification_object['score']} {notification_object['trend']}"
            },
            "accessory": {
                "type": "image",
                "image_url": f"{notification_object['url']}",
                "alt_text": "Product image"
            }
        }
        attachment["blocks"].append(block)
        attachments.append(attachment)

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        client = WebClient(token=app.config.get('SLACK_TOKEN'), ssl=ssl_context)

        now = datetime.utcnow()
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        hour_after_24 = current_hour + timedelta(hours=24)
        start_date = current_hour.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_date = hour_after_24.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        try:
            response = client.chat_postMessage(
                channel=app.config.get('SLACK_CHANNEL'),
                text="Upcoming launches in 24 hours",
                attachments=json.dumps(attachments)
            )
            print(response)
        except SlackApiError as e:
            print(f"Sending notification to slack fail： {e}")