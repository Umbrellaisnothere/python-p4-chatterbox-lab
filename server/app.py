from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by("created_at").all()
        return jsonify([message.to_dict() for message in messages]), 200
    elif request.method == "POST":
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'id': new_message.id,
            'body': new_message.body,
            'username': new_message.username,
        }), 201
    # else KeyError:
    # return jsonify({"error": "Invalid data"}), 400

@app.route('/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.get(id)
    if request.method == "GET":
        return jsonify(message.to_dict()), 200
    
    elif request.method == "PATCH":
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return jsonify({}), 204

if __name__ == '__main__':
    app.run(port=5555)
