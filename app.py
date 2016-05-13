import sys
import random

from flask import Flask, render_template

app = Flask(__name__)

def rnd_clr():
	colors = ['#9ad3de', 'rgb(252,123,52)', '#3fb0ac', '#fae596', '#dbe9d8', '#f2efe8', '#fccdd3']
	return random.choice(colors)


@app.route("/")
def index():
    return render_template('home.html', bg_color=rnd_clr())


if __name__ == "__main__":
	port = 8000
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	app.run(port=port, debug=True)
