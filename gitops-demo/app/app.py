from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    message = os.getenv("APP_MESSAGE", "Default GitOps Message")
    return f"<h1>{message}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
