import requests
import pymysql.cursors
import pymysql

products_to_search = []
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lhj198245817',
                             db='launch',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `stylecolor` FROM `products`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for product in result:
            products_to_search.append(product.get('stylecolor'))
finally:
    connection.close()

print("Found products: {}".format(products_to_search))
for product in products_to_search:
    print("Crawling content for {} ... ".format(product))
    search_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D" + \
        product + "&page_type=searchall"
    # response = requests.get(search_url)
    # print(response.json())
