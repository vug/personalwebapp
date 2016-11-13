import argparse

from factory import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='port to listen to', default=8000)
    args = parser.parse_args()

    app = create_app()
    app.run(port=args.port, debug=True)
