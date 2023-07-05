import os

host = '127.0.0.1'
port = 5000
web_socket = f'http://{host}:{port}/' if port != 80 else f'http://{host}/'
app_name = 'app'
apps = ['user', 'post']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_settings = {
    'BASE_DIR': [os.path.join(os.path.join(BASE_DIR, app_name), app) for app in apps],
    'TEMPLATES_DIR': 'templates'
}
db_dir_path = BASE_DIR
db_name = 'db.db'
secret_JWT = 'yNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCIsICJuYW1lIjogIkpvaG4gRG9lIiwgImFkbWluIjogdHJ1ZX0'
echo_sql = True
media_folder = 'media/'
static_folder = 'static/'
media = os.path.join(BASE_DIR, media_folder)
media_html = os.path.join(web_socket, media_folder)
static = os.path.join(BASE_DIR, static_folder)

