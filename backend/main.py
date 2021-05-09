from flask import Flask
from flask_cors import CORS
from dynaconf import settings
from apis import blueprint as api

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.DEBUG)
