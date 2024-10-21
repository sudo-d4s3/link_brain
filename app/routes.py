from flask import render_template, flash, request
from app import app
from app.scripts.convert import json_convert
from app.scripts.metadata_content_gatherer import get_metadata_and_content
import json

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET"])
def index():
    return "test"


@app.route("/api/convert_backup", methods=["POST"])
def convert_backup():
    bookjson = json_convert(json.loads(request.data))
    bookjson = get_metadata_and_content(bookjson)
    return bookjson


@app.route("/api/bookmarks", methods=["GET","PATCH"])
def bookmarks():
    pass


@app.route("/api/bookmark/<id>", methods=["GET", "DELETE", "PATCH"])
def bookmark(id):
    return id
