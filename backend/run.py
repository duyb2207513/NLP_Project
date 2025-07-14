from flask import Flask, request, jsonify
import runpy as np
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins="*")

app = Flask(__name__)

@app.route('/api/v1/')
def hello_world():  # put application's code here
    return 'Hello World! Kết nối backend thành công'

# import routes
from routes import register_app
register_app(app)

if __name__ == '__main__':
    app.run()

