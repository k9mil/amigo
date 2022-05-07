from flask import Flask, render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")