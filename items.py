import db

def add_item(title, location, description, user_id):
    sql = """INSERT INTO items (title, location, description, user_id) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, location, description, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.location,
                    items.description,
                    users.id user_id,
                    users.username
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = ?"""
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, location, description):
    sql = """UPDATE items SET title = ?,
                              location = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, location, description, item_id])