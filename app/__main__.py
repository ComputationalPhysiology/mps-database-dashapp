import logging
from app.main import app


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run_server(debug=True, port=8001)
