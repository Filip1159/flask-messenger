from server import create_app, socket


app = create_app()
if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0")
