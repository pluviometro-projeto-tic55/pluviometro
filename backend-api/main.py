import os
from src import create_app, socketio
from src.scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':

    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 5000)
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    if not debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        start_scheduler(app)

    socketio.run(app, host=host, port=port, debug=debug)