from flask import Blueprint, render_template

views = Blueprint('views', __name__)

# home function runs, whenever we go to '/' directory


@views.route('/')
def home():
    return render_template("home.html")
