import os

host = '127.0.0.1'
port = 5000
template_settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR': 'templates'
}
db_dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'db.db'
secret_JWT = 'yNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCIsICJuYW1lIjogIkpvaG4gRG9lIiwgImFkbWluIjogdHJ1ZX0'
echo_sql = True
main_path = os.path.dirname(os.path.abspath(__file__))
media_folder = 'media'
static_folder = 'static'
media = os.path.join(main_path, media_folder)
static = os.path.join(main_path, static_folder)
from app.user.model import User
user_model = User
