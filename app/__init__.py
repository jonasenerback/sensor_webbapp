from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

from app import routes
