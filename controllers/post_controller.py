from models.post import Post
from flask import flash, redirect, url_for, abort, session

def list_posts(published=True):
    return Post.get_by_status(is_published=published)

def get_post(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        abort(404)
    return post

def create_post(form):
    title = form.get("title")
    body = form.get("body")
    is_published = True if form.get("publish") == "on" else False
    author = session.get("username", "admin")  # Use session username as author

    if not title or not body:
        flash("Title and body are required!", "error")
        return redirect(url_for("posts.new_post"))

    post = Post(title, body, author, is_published)
    Post.save(post)
    flash("Post saved successfully!", "success")
    return redirect(url_for("posts.show_posts"))

def update_post(post_id, form):
    title = form.get("title")
    body = form.get("body")
    is_published = True if form.get("publish") == "on" else False

    if not title or not body:
        flash("Title and body are required!", "error")
        return redirect(url_for("posts.edit_post", post_id=post_id))

    updated_data = {
        "title": title,
        "body": body,
        "is_published": is_published
    }

    if Post.update(post_id, updated_data):
        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.post_detail", post_id=post_id))
    else:
        flash("Post not found!", "error")
        return redirect(url_for("posts.show_posts"))

def list_drafts():
    return Post.get_by_status(is_published=False)


