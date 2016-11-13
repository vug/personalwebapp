"""
Run the application using Flask's simple webserver via

python runserver.py

command. Default port is 8000. To set the port indicate it via --port argument

python runserver.py --port 5000
"""
import argparse

from factory import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='port to listen to', default=8000)
    args = parser.parse_args()

    app = create_app()
    app.run(port=args.port, debug=True)
