from flask import Flask, render_template
from routes.post_routes import post_bp
from routes.user_routes import user_bp
from controllers.post_controller import list_posts

app = Flask(__name__)
app.secret_key = "secret_key"

app.register_blueprint(post_bp)
app.register_blueprint(user_bp)

@app.route("/")
def home():
    posts = list_posts(published=True)
    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
