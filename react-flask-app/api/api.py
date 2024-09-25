import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder="../build", static_url_path='/')
CORS(app)  # Enable CORS

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/time/')
def get_current_time():
    return {'time': "7497"}

if __name__ == '__main__':
    app.run(debug=True)
