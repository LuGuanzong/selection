import os

from app.factory import create_app

config_dict = dict(devlopment='DEVELOPMENT', production='PRODUCTION')
env = os.environ.get('FLASK_ENV', 'devlopment')

app = create_app(config_name=config_dict[env])

if __name__ == "__main__":
    app.run()
