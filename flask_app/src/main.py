from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import close_db


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../static')
    app.config.from_object(Config)
    CORS(app)


# register blueprints
from .routes.auth import bp as auth_bp
from .routes.tables import bp as tables_bp
from .routes.vision import bp as vision_bp
from .routes.robot import bp as robot_bp


app.register_blueprint(auth_bp)
app.register_blueprint(tables_bp)
app.register_blueprint(vision_bp)
app.register_blueprint(robot_bp)


# teardown
app.teardown_appcontext(close_db)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/health')
def health():
    return {'status': 'ok'}


return app


if __name__ == '__main__':
app = create_app()
app.run(host='0.0.0.0', port=5000, debug=True)