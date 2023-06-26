import os


settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR': 'templates'
}
db_dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'db.db'
secret_JWT = 'yNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCIsICJuYW1lIjogIkpvaG4gRG9lIiwgImFkbWluIjogdHJ1ZX0'
echo_sql = True
media_path = os.path.dirname(os.path.abspath(__file__))
media_folder = 'media'
media = os.path.join(media_path, media_folder)