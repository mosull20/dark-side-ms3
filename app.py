import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/get_reviews")
def get_reviews():
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    reviews = list(mongo.db.reviews.find({"$text": {"$search": query}}))
    return render_template("reviews.html", reviews=reviews)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # if username does not already exist
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
            }
        mongo.db.users.insert_one(register)
        # put new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # password does not match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get session user's name from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    reviews = list(mongo.db.reviews.find(
        {"added_by": session["user"]}
    ))
    if session["user"]:
        return render_template("profile.html", username=username, reviews=reviews)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = {
            "category_name": request.form.get("category_name"),
            "title_name": request.form.get("title_name"),
            "author_name": request.form.get("author_name"),
            "synopsis": request.form.get("synopsis"),
            "user_review": request.form.get("user_review"),
            "added_by": session["user"]
        }
        mongo.db.reviews.insert_one(review)
        flash("Your review has been successfully added")
        return redirect(url_for("profile", username=session["user"]))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_review.html", categories=categories)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":
        updated_review = {
            "category_name": request.form.get("category_name"),
            "title_name": request.form.get("title_name"),
            "author_name": request.form.get("author_name"),
            "synopsis": request.form.get("synopsis"),
            "user_review": request.form.get("user_review"),
            "added_by": session["user"]
            }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, updated_review)
        flash("Your review has been successfully updated")
        return redirect(url_for("profile", username=session["user"]))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_review.html", review=review, categories=categories)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Your review has been deleted")
    return redirect(url_for("profile", username=session["user"]))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
