import db

def add_item(title, location, description, user_id, classes):
    sql = """INSERT INTO items (title, location, description, user_id) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, location, description, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_comment(item_id, user_id, comment):
    sql = """INSERT INTO comments (item_id, user_id, comment)
             VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, comment])

def add_image(item_id, image):
    sql = "INSERT INTO images (item_id, image) VALUES (?, ?)"
    db.execute(sql, [item_id, image])


def get_comments(item_id):
    sql = """SELECT comments.comment, users.id user_id, users.username, comments.id
             FROM comments, users
             WHERE comments.item_id = ? AND comments.user_id = users.id
             ORDER BY comments.id DESC"""
    return db.query(sql, [item_id])

def get_comment(comment_id):
    sql = """SELECT comments.id,
                    comments.item_id,
                    comments.user_id,
                    comments.comment,
                    users.username
             FROM comments, users
             WHERE comments.user_id = users.id AND
                   comments.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

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
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, location, description):
    sql = """UPDATE items SET title = ?,
                              location = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, location, description, item_id])

def update_comment(comment_id, content):
    sql = """UPDATE comments SET comment = ?
                          WHERE id = ?"""
    db.execute(sql, [content, comment_id])

def remove_item(item_id):
    sql = "DELETE FROM comments WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
