import db

def add_item(title, location, description, user_id):
    sql = """INSERT INTO items (title, location, description, user_id) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, location, description, user_id])