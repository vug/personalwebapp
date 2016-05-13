import sys

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home.html')


if __name__ == "__main__":
	port = 8000
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	app.run(port=port, debug=True)
