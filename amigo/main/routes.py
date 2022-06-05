from flask import Flask, render_template, Blueprint, redirect, url_for

from amigo.main.utils.data_utils import get_data, encode_url

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/steam")
def send_request():
    encoded_url = encode_url()
    return redirect(encoded_url)

@main.route("/process")
def process():
    try:
        get_data()
    except KeyError:
        return redirect(url_for("errors.notfound"))
        
    return redirect(url_for("main.waiting"))

@main.route("/waiting")
def waiting():
    return render_template("waiting.html")

@main.route("/chat")
def chat():
    return render_template("chat.html")
