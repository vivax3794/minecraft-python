from .client import Client

server = "127.0.0.1"
username = "python"

c = Client()
c.login(username, server)
