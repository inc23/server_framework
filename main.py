from server.server import Server
from app.main import app


Server(framework=app)
