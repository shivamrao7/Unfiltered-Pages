from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

user_bp = Blueprint('users', __name__)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.find_user(username)

        if user and user["password"] == password:
            session['user_id'] = user.get('id', username)
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for("posts.show_posts"))
        else:
            flash("Invalid credentials", "error")
            return render_template("login.html")
    
    return render_template("login.html")

@user_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.find_user(username):
            flash("Username already exists!", "error")
            return render_template("signup.html")
        
        new_user = User(username, password)
        if User.save_user(new_user):
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("users.login"))
        else:
            flash("Username already exists!", "error")
            return render_template("signup.html")

    return render_template("signup.html")

