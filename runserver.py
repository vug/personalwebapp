import sys
from factory import create_app

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    app = create_app()
    app.run(port=port, debug=True)
