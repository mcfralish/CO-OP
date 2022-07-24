import email
from operator import mod
import os
import random
from flask import Flask, flash, render_template, redirect, request, json
from dotenv import find_dotenv, load_dotenv
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from requests import session
from models import db, Users, Coops

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)

avatars = [
    "/static/imgs/avatars/avatar1.jpg",
    "/static/imgs/avatars/avatar2.jpg",
    "/static/imgs/avatars/avatar3.jpg",
    "/static/imgs/avatars/avatar4.jpg",
    "/static/imgs/avatars/avatar5.jpg",
    "/static/imgs/avatars/avatar6.png",
    "/static/imgs/avatars/avatar7.jpg",
    "/static/imgs/avatars/avatar8.jpg",
]
states = us_state_to_abbrev = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
    "District of Columbia",
    "American Samoa",
    "Guam",
    "Northern Mariana Islands",
    "Puerto Rico",
    "United States Minor Outlying Islands",
    "U.S. Virgin Islands",
]
categories = [
    "Accomodations and Food Service",
    "Health Care",
    "Manufacturing and Engineering",
    "Technology",
    "Design",
]
# Initialize db and create all tables if not already.
db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads  current user"""
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    """index page: Will show 3 random communities along with a snippet about our goals"""

    all_coops = Coops.query.all()

    if len(all_coops) < 3:
        upto3 = len(all_coops)
    else:
        upto3 = 3

    displayed_coops = random.sample(all_coops, upto3)

    return render_template("index.html", coops=displayed_coops)


@app.route("/header")
def header():
    authenticated = current_user.is_authenticated
    avatar_path = None
    if authenticated:
        avatar_path = Users.query.filter_by(id=current_user.id).first().icon
    return render_template(
        "header.html", authenticated=authenticated, avatar_path=avatar_path
    )


@app.route("/signUp", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        data = request.form

        if data["pw"] != data["verify"]:
            flash("Password does not match")
            return redirect("/signUp")

        if Users.query.filter_by(uid=data["uid"]).first():
            flash("That CO-OP Id is registered to another user.")
            return redirect("/signUp")

        if Users.query.filter_by(email=data["email"]).first():
            flash("That email address is already registered. Try signing in.")
            return redirect("/signUp")

        new_user = Users(
            email=data["email"],
            uid=data["uid"],
            pw=data["pw"],
            fname=data["fname"],
            lname=data["lname"],
            icon=avatars[int(data["icon"])],
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f"Welcome to CO-OP, {data['fname']} {data['lname']}!")
        return redirect("/")

    return render_template("signUp.html", avatars=avatars)


@app.route("/signIn", methods=["GET", "POST"])
def signIn():
    if request.method == "POST":
        data = request.form

        visitor = Users.query.filter_by(uid=data["uid"]).first()

        if not visitor:
            flash("No such username. Retry or Create an account now.")
            return redirect("/signIn")

        if visitor.pw != data["pw"]:
            flash("Incorrect Password")
            return redirect("/signIn")

        login_user(visitor)
        flash(f"Welcom back to CO-OP, {visitor.fname} {visitor.lname}!")
        return redirect("/")

    return render_template("signIn.html")


@app.route("/logout")
def logout():
    flash("Thank you for using CO-OP. Please come again.")
    logout_user()
    return redirect("/")


@app.route("/co-ops")
def coops():
    authenticated = current_user.is_authenticated
    return render_template(
        "coops.html", authenticated=authenticated, categories=categories
    )


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data = request.form
        new_coop = Coops(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            city=data["city"],
            state=data["state"],
            link=data["link"],
            pic_link=data["pic-link"],
        )

        db.session.add(new_coop)
        db.session.commit()
        return redirect("/co-ops")

    return render_template("create.html", states=states, categories=categories)


@app.route("/coop_query", methods=["GET"])
def coop_query():
    category = request.args["category"]
    if category == "all":
        coops = Coops.query.all()
    else:
        coops = Coops.query.filter_by(category=category).all()

    coops.sort(key=lambda x: x.name)
    return render_template("coop_query.html", coops=coops)


@app.route("/checklist")
def checklist():
    return render_template("checklist.html")


@app.route("/description")
def site_description():
    return render_template("description.html")


@app.route("/about")
def about():
    return render_template("about.html")


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
