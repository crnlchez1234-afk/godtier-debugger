# Security hardening: SQL injection protection via parameterized queries

import sqlite3
from typing import Any

def get_user(username: str) -> Any:
    # SECURITY ISSUE: SQL injection vulnerable
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    result = cursor.fetchone()
    conn.close()

    return result

def search_products(category: Any) -> Any:
    # SECURITY ISSUE: No input validation
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE category = ?")

    return cursor.fetchall()
