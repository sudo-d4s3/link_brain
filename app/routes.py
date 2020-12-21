from flask import render_template, flash
from app import app, db
from app.models import *
from app.forms import BookmarkForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    bookmarks = Bookmarks.query.all()
    form = BookmarkForm()
    if form.validate_on_submit():
        bookmark = Bookmarks(title=form.title.data, link=form.link.data)
        db.session.add(bookmark)

        tags = form.tags.data
        tags = tags.split('; ')
        for tag in tags:
            if Tag.query.filter_by(name=tag.lower()).first() is not None:
                t = Tag.query.filter_by(name=tag.lower()).first()
                bookmark.tags.append(t)
            else:
                t = Tag(name=tag.lower())
                bookmark.tags.append(t)
        
        db.session.add(bookmark)

        db.session.commit()
        flash('Bookmark Saved!')
    return render_template('index.html', bookmarks=bookmarks, form=form)
