import os

from app.factory import create_app

# config_dict = dict(development='DEVELOPMENT', production='PRODUCTION')
# env = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name='PRODUCTION')

if __name__ == "__main__":
    app.run()
