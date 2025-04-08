import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """SELECT items.id, items.title, users.id user_id, users.username,
                    COUNT(comments.id) as comment_count
             FROM items
             JOIN users ON items.user_id = users.id
             LEFT JOIN comments ON items.id = comments.item_id
             WHERE items.user_id = ?
             GROUP BY items.id, users.id
             ORDER BY items.id DESC"""
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        None
