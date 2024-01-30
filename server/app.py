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

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    
    message_ascending = Message.query.order_by(Message.created_at.asc()).all()
    
    if request.method == 'GET':
        message_list = [i.to_dict() for i in message_ascending ]
        response = make_response(jsonify(message_list), 200)
        
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username']
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        response = make_response(jsonify(new_message.to_dict()), 201)
        
        
        return response

@app.route('/messages/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def messages_by_id(id):
    
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        response = make_response(jsonify(message.to_dict()), 200)
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response = make_response({"message": "Entry Deleted succesfully"}, 200)
        return response
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        
        db.session.add(message)
        db.session.commit()
        
        response = make_response(jsonify(message.to_dict()), 200)
        
        return response

if __name__ == '__main__':
    app.run(port=5555)