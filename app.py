import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    location = request.form["location"]
    if not location or len(location) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    user_id = session["user_id"]
    
    classes = []
    section = request.form["section"]
    if section:
        classes.append(("Aihe", section))

    items.add_item(title, location, description, user_id, classes)

    return redirect("/")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, comment)

    return redirect("/item/" + str(item_id))

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    return render_template("show_item.html", item=item, classes=classes, comments=comments)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    location = request.form["location"]
    if not location or len(location) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 50:
        abort(403)

    items.update_item(item_id, title, location, description)
    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)

            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/edit_comment/<int:comment_id>")
def edit_comment(comment_id):
    require_login()
    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_comment.html", comment=comment)

@app.route("/update_comment", methods=["POST"])
def update_comment():
    require_login()
    comment_id = request.form["comment_id"]
    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    content = request.form["content"]
    if not content or len(content) > 1000:
        abort(403)

    items.update_comment(comment_id, content)
    return redirect("/item/" + str(comment["item_id"]))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()
    comment = items.get_comment(comment_id)
    user_id = session["user_id"]

    if comment["user_id"] != user_id:
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment, item_id=comment["item_id"])

    if request.method == "POST":
        item_id = request.form.get("item_id")
        if not item_id:
            abort(400, description="Item ID missing")

        if "remove" in request.form:
            items.remove_comment(comment_id)
            return redirect("/item/" + str(item_id))
        else:
            return redirect("/item/" + str(item_id))




@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return render_template("user_created.html")

    password_hash = generate_password_hash(password1)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
    
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
