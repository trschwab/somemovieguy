from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite or PostgreSQL database (example uses SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usernames.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database (create tables)
with app.app_context():
    db.create_all()

# Route to add a username
@app.route('/api/usernames', methods=['POST'])
def add_username():
    data = request.get_json()
    username = data.get('name')
    if username:
        user = User(name=username)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Username saved successfully'}), 200
    return jsonify({'message': 'Failed to save username'}), 400

# Route to fetch all usernames
@app.route('/api/usernames', methods=['GET'])
def get_usernames():
    users = User.query.all()
    usernames = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(usernames), 200

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
