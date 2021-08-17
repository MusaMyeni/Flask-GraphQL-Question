from flask import Blueprint, render_template, request, url_for, flash, redirect
from sqlalchemy.orm.query import Query
from werkzeug.exceptions import abort

from ..database import db
from ..models import Post, Tag

posts = Blueprint("posts", __name__)


@posts.route("/", methods=("GET", "POST"))
def index():
    """
    The index page accepts both the GET and POST method. 
    The GET method will display all posts initially.
    The POST method will display a list of all the posts with the tag label specified in the search bar
    """
    # NB: Creation date not activated yet but will follow a similar principle. 
    # Known Bugs: Searching for an empty string will return 0 results.  
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template("index.html", posts=posts)

    elif request.method == 'POST':
        search_param = request.form['search']
        formatted_search_parameter = "%{}%".format(search_param)
        posts = (
            Post.query.join(Post.tags).filter(Tag.label.like(formatted_search_parameter)).all()
        )
        return render_template("index.html", posts=posts)


@posts.route("/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return render_template("post.html", post=post)


@posts.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag_name = request.form["tag"]

        if not title:
            flash("Title is required!")
        else:
            existing_tag = Tag.query.filter_by(label=tag_name).first()
            if existing_tag:
                new_post = Post(title=title, content=content, tags=[existing_tag])
            elif not existing_tag:
                new_tag = Tag(label=tag_name)
                new_post = Post(title=title, content=content, tags=[new_tag])

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for("posts.index"))
    return render_template("create.html")


@posts.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    post = Post.query.get(post_id).join(Post.tags)
    if not post:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            post.title = title
            post.content = content

            db.session.commit()

            return redirect(url_for("posts.index"))

    return render_template("edit.html", post=post)


@posts.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))
