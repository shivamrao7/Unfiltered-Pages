from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.post_controller import (
    list_posts,
    get_post,
    create_post,
    update_post,
    list_drafts
)

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

# ✅ Login route
@post_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "admin" and password == "1234":
        session['user_id'] = username
        session['username'] = username
        flash("Login successful!", "success")
        return redirect(url_for("posts.show_posts"))
    else:
        flash("Invalid credentials. Try again.")
        return redirect(url_for("home"))

# ✅ Show published posts
@post_bp.route("/", methods=["GET"])
def show_posts():
    posts = list_posts(published=True)
    return render_template("posts.html", posts=posts)

# ✅ Show post details
@post_bp.route("/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    post = get_post(post_id)
    return render_template("post_details.html", post=post)

# ✅ New post form + submission
@post_bp.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        return create_post(request.form)
    return render_template("post_form.html")

# ✅ Edit existing post
@post_bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        return update_post(post_id, request.form)
    post = get_post(post_id)
    return render_template("post_form.html", post=post)

# ✅ Show drafts (unpublished posts)
@post_bp.route("/drafts", methods=["GET"])
def drafts():
    posts = list_drafts()
    return render_template("posts.html", posts=posts, title="Drafts")
