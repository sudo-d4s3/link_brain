from flask import render_template, flash
from app import app, db
from app.models import Bookmarks
from app.forms import BookmarkForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    bookmarks = Bookmarks.query.all()
    form = BookmarkForm()
    if form.validate_on_submit():
        bookmark = Bookmarks(title=form.title.data, link=form.link.data)
        db.session.add(bookmark)
        db.session.commit()
        flash('Bookmark Saved!')
    return render_template('index.html', bookmarks=bookmarks, form=form)
