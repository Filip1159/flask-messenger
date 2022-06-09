from server import create_app
from server.socket import socket


# app runner
# allows app to run in debug mode - showing all requests, responses and errors in console
# 0.0.0.0 - run app on each network interface of device
app = create_app()
if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0")
