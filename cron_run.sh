#!/bin/bash

cd /opt/pyth/crawler
source .venv/bin/activate
PYTHON_CMD=`which python`

echo "Syncing products..."
${PYTHON_CMD} sync_launch_product.py || exit 1
echo "Updating reviews..."
${PYTHON_CMD} update_reviews.py || exit 2
echo "Updating prices..."
${PYTHON_CMD} update_prices.py || exit 3
echo "Updating ratings..."
${PYTHON_CMD} rating_calc.py || exit 4
echo "Sending message..."
${PYTHON_CMD} send_slack_notification.py || exit 5