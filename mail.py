from flask import Flask
from flask_mailman import Mail, EmailMessage

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='msdhariom2003@gmail.com',
    MAIL_PASSWORD='krfs ynck jmmi juik',
    MAIL_DEFAULT_SENDER = 'msdhariom2003@gmail.com'
)

mail = Mail(app)

@app.route("/")
def index():
    return "Hello, Flask-Mailman App"

@app.route("/send")
def send():
    msg = EmailMessage(
        subject="Hello!",
        body="This is a test message from Flask-Mailman.",
        to=["suprimraja@gmail.com"]
    )
    msg.send()
    return "Email sent!"

if __name__ == "__main__":
    app.run(debug=True)