from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hi, I am Ugur! This is my personal web app."


if __name__ == "__main__":
    app.run()
