from flask import render_template, flash
from app import app, db
from app.models import *
from app.forms import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    bookmarks = Bookmarks.query.all()
    bform = BookmarkForm()
    sform = SearchForm()
    if bform.submit_bookmark.data and bform.validate:
        bookmark = Bookmarks(title=bform.title.data, link=bform.link.data)
        db.session.add(bookmark)

        tags = bform.tags.data
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
    if sform.submit_search.data and sform.validate():
        bookmark = []
        tags = sform.search.data
        tags = tags.split('; ')

        for tag in tags:
            bookmark += Bookmarks.query.filter(Bookmarks.tags.any(name=tag)).all()

        for x in range(len(bookmark)):
            for y in range(len(bookmark)):
                if x+y >= len(bookmark):
                    break
                if bookmark[y] == bookmark[y+x]:
                    bookmark.pop(x)
        
        return render_template('index.html', bookmarks=bookmark, bform=bform, sform=sform)
    return render_template('index.html', bookmarks=bookmarks, bform=bform, sform=sform)
