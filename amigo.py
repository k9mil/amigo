from amigo import create_app, socketio

import amigo.main.events

app = create_app()

if __name__ == "__main__":
    socketio.run(app)