from typing import Any
import sqlite3



def handle_login(username: str, password: Any) -> Any:
    # SECURITY ISSUE: SQL injection + plain password
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    return user is not None

def handle_search(category: Any, sort_by: Any) -> Any:
    # SECURITY ISSUE: Multiple injection points
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM products WHERE category='{category}' ORDER BY {sort_by}"
    cursor.execute(query)

    return cursor.fetchall()

def get_user_data(user_id: str) -> Any:
    # SECURITY ISSUE: No input validation
    conn = sqlite3.connect('data.db')
    query = f"SELECT * FROM user_data WHERE id={user_id}"
    return conn.execute(query).fetchone()
