import json
from datetime import datetime

def json_to_dict(file_path):
    with open(file_path, "r") as file:
        dict_data = json.load(file)
    return dict_data

file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/swiggy_json_data/" +  "Extract_data.json"
list_data = json_to_dict(file_path)
# print(list_data)
print(type(list_data))


import mysql.connector # Must include .connector


try:
    print("Connecting...")
    # Connection logic here
    connection = mysql.connector.connect(
        # host="3306",
        host="localhost",
        user="root",
        password="actowiz",
        port ="3306",
        database = "web_scraping_db"

    )
    cursor = connection.cursor()

    # show all databases
    #  databases create .
    # cursor.execute("create database web_scraping_db")
    cursor.execute("SHOW DATABASES")
    print("---all DATABASES---")
    for db in cursor:
        print(db[0])

    # this is create new table in web_scraping_db 
    # cursor.execute("CREATE TABLE swiggy_products  ( id INT AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(100), product_id VARCHAR(50), price DECIMAL(10,2), quantity VARCHAR(100), discount_percentage INT, product_mrp DECIMAL(10, 2), is_available BOOLEAN DEFAULT TRUE ) ")
    # cursor.execute("CREATE TABLE swiggy_product_images  ( id INT AUTO_INCREMENT PRIMARY KEY, swiggy_product_id INT, image_url TEXT,  FOREIGN KEY (swiggy_product_id) REFERENCES swiggy_products(id) ) ")

    # insert data in table
    parent_sql = """INSERT INTO swiggy_products
                            (product_name, product_id, price, quantity, discount_percentage, product_mrp, is_available)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    child_sql = """INSERT INTO swiggy_product_images 
                           (swiggy_product_id, image_url ) 
                           VALUES (%s, %s )"""

    for product_dict in list_data:
        parent_values = (
            product_dict["product_name"],
            product_dict["product_id"],
            product_dict["price"],
            product_dict["quantity"],
            product_dict["discount_percentage"],
            product_dict["product_mrp"],
            product_dict["is_available"]
        )
        cursor.execute(parent_sql,parent_values)
        last_parant_id = cursor.lastrowid

        image_url_data = []
        for url_str in product_dict["image_url"]:
            url_tuple = ( last_parant_id, url_str )
            image_url_data.append(url_tuple)
        cursor.executemany(child_sql, image_url_data)
        connection.commit()


except Exception as e:
    print(f"Error: {e}")

print("yes : now ")