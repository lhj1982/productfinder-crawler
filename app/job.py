# TO BE REMOVED!!!
import logging
from sqlalchemy import text
from sqlalchemy.orm import Session

_logger = logging.getLogger("app")


def sync_product_info(engine):
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

