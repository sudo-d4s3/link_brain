from flask import render_template
from app import app
from app.models import Bookmarks

@app.route('/')
@app.route('/index')
def index():
    bookmarks = Bookmarks.query.all()
    return render_template('index.html', bookmarks=bookmarks)
