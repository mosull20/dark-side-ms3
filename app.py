import os
import requests
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


# Functions
# function to check if valid image url
# code from Stack Overflow,
# https://stackoverflow.com/questions/10543940/check-if-a-url-to-an-image-is-up-and-exists-in-python
def is_url_image(img_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(img_url)
    if r.headers.get("content-type", '') in image_formats:
        return True
    return False


# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Get book reviews only
@app.route("/book_reviews")
def book_reviews():
    reviews = list(mongo.db.reviews.find({"category_name": "Book"}))
    return render_template("reviews.html", reviews=reviews)


# Get movie reviews only
@app.route("/movie_reviews")
def movie_reviews():
    reviews = list(mongo.db.reviews.find({"category_name": "Movie"}))
    return render_template("reviews.html", reviews=reviews)


# Get tv show reviews only
@app.route("/tvshow_reviews")
def tvshow_reviews():
    reviews = list(mongo.db.reviews.find({"category_name": "TV Show"}))
    return render_template("reviews.html", reviews=reviews)


# Get all reviews
@app.route("/get_reviews")
def get_reviews():
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


# search functionality
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    reviews = list(mongo.db.reviews.find({"$text": {"$search": query}}))
    return render_template("reviews.html", reviews=reviews)


# sort-by functionality
# sort all reviews by title name, ascending order
@app.route("/sort_reviews")
def sort_reviews():
    reviews = list(mongo.db.reviews.find().sort("title_name", 1))
    return render_template("reviews.html", reviews=reviews)


# sort all book reviews by title name, ascending order
@app.route("/sort_book_reviews")
def sort_book_reviews():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "Book"}).sort("title_name", 1))
    return render_template("reviews.html", reviews=reviews)


# sort all movie reviews by title name, ascending order
@app.route("/sort_movie_reviews")
def sort_movie_reviews():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "Movie"}).sort("title_name", 1))
    return render_template("reviews.html", reviews=reviews)


# sort all tv show reviews by title name, ascending order
@app.route("/sort_tvshow_reviews")
def sort_tvshow_reviews():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "TV Show"}).sort("title_name", 1))
    return render_template("reviews.html", reviews=reviews)


# sort all reviews by rating, descending order
@app.route("/sort_reviews_rating")
def sort_reviews_rating():
    reviews = list(mongo.db.reviews.find().sort("rating", -1))
    return render_template("reviews.html", reviews=reviews)


# sort book reviews by rating, descending order
@app.route("/sort_book_reviews_rating")
def sort_book_reviews_rating():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "Book"}).sort("rating", -1))
    return render_template("reviews.html", reviews=reviews)


# sort movie reviews by rating, descending order
@app.route("/sort_movie_reviews_rating")
def sort_movie_reviews_rating():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "Movie"}).sort("rating", -1))
    return render_template("reviews.html", reviews=reviews)


# sort tv show reviews by rating, descending order
@app.route("/sort_tvshow_reviews_rating")
def sort_tvshow_reviews_rating():
    reviews = list(mongo.db.reviews.find(
        {"category_name": "TV Show"}).sort("rating", -1))
    return render_template("reviews.html", reviews=reviews)


# User registration
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


# User login
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


# User profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get session user's name from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    reviews = list(mongo.db.reviews.find(
        {"added_by": session["user"]}
    ))
    if session["user"]:
        return render_template(
            "profile.html", username=username, reviews=reviews)

    return redirect(url_for("login"))


# User log out
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# User add review functionality
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":

        # check image url if one provided by user
        review_image = request.form.get("image_url")
        image_url = ""
        if review_image:
            # function call to verify image
            if is_url_image(review_image):
                image_url = review_image
                flash("Image verified")
            else:
                image_url = "../static/images/new-zombie.jpg"
                flash("Image not valid, will apply default image instead")

        review = {
            "category_name": request.form.get("category_name"),
            "title_name": request.form.get("title_name").title(),
            "author_name": request.form.get("author_name"),
            "synopsis": request.form.get("synopsis"),
            "rating": request.form.get("rating"),
            "user_review": request.form.get("user_review"),
            "image_url": image_url,
            "added_by": session["user"]
        }
        mongo.db.reviews.insert_one(review)
        flash("Your review has been successfully added")
        return redirect(url_for("profile", username=session["user"]))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_review.html", categories=categories)


# User edit review functionality
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":

        # check image url if one provided by user
        review_image = request.form.get("image_url")
        image_url = ""
        if review_image:
            # function call to verify image
            if is_url_image(review_image):
                image_url = review_image
                flash("Image verified")
            else:
                image_url = "../static/images/new-zombie.jpg"
                flash("Image not valid, will apply default image instead")

        updated_review = {
            "category_name": request.form.get("category_name"),
            "title_name": request.form.get("title_name").title(),
            "author_name": request.form.get("author_name"),
            "synopsis": request.form.get("synopsis"),
            "rating": request.form.get("rating"),
            "user_review": request.form.get("user_review"),
            "image_url": image_url
            }
        mongo.db.reviews.update_one(
            {"_id": ObjectId(review_id)}, {"$set": updated_review})
        flash("Your review has been successfully updated")
        return redirect(url_for("profile", username=session["user"]))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_review.html", review=review, categories=categories)


# User delete review functionality
@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Your review has been deleted")
    return redirect(url_for("profile", username=session["user"]))


# Contact page form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thank you, your message has been successfully sent.")
    return render_template("contact.html")


# error handling code from
# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html", error=error), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
