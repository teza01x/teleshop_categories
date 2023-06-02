import sqlite3
from config import *


def user_exists(user_id):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user_info WHERE user_id = ?", (user_id,))
    exists = bool(len(result.fetchall()))

    conn.close()

    return exists


def add_user(user_id):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info (user_id, category, start_menu) VALUES(?, ?, ?)", (user_id, None, None,))

    conn.commit()
    conn.close()


def add_start_menu_id(user_id, menu_id):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET start_menu = ? WHERE user_id = ?", (menu_id, user_id,))

    conn.commit()
    conn.close()


def check_start_menu_id(user_id):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()
    cursor.execute("SELECT start_menu FROM user_info WHERE user_id = ?", (user_id,))
    id_menu = cursor.fetchone()[0]

    conn.close()

    return id_menu


def get_category_items(category_name):
    conn = sqlite3.connect(data_base_products)
    cursor = conn.cursor()


    cursor.execute(f"SELECT name, price FROM {category_name}")
    items = cursor.fetchall()

    conn.close()

    return items

def get_item_info(category_name, item_name):
    conn = sqlite3.connect(data_base_products)
    cursor = conn.cursor()


    cursor.execute(f"SELECT item_code, name, description, price FROM {category_name} WHERE name = ?", (item_name,))
    items = cursor.fetchall()
    conn.close()

    return items


def add_user_category(user_id, current_category):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET category = ? WHERE user_id = ?", (current_category, user_id,))

    conn.commit()
    conn.close()


def check_user_category(user_id):
    conn = sqlite3.connect(data_base_users)
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM user_info WHERE user_id = ?", (user_id,))
    category_id = cursor.fetchone()[0]

    conn.close()

    return category_id

