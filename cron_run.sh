#!/bin/bash

cd /opt/pyth/crawler
source .venv/bin/activate
PYTHON_CMD=`which python`

echo "Updating reviews..."
${PYTHON_CMD} update_reviews.py || exit 1
echo "Updating prices..."
${PYTHON_CMD} update_prices.py || exit 2
echo "Updating ratings..."
${PYTHON_CMD} rating_calc.py || exit 3
echo "Syncing products..."
${PYTHON_CMD} sync_launch_product.py || exit 4