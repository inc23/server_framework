import os

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR': 'templates'
}

db_dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'db.db'
