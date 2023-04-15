from app import app, mongo
from bson import json_util, ObjectId
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

import flask
import json

@app.route('/ratings', methods=['POST'])
def add_rating():
	_json = request.json
	_contentId = _json['contentId']
	_userId = _json['userId']
	_score = _json['score']
	# validate the received values
	if _contentId and _userId and _score and request.method == 'POST':
		# save details
		rating = mongo.db.ratings.insert_one({'contentId': ObjectId(_contentId), 'userId': ObjectId(_userId), 'score': _score})
		resp = jsonify(str(rating.inserted_id) + ' - rating added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/ratings')
def ratings():
	ratings = mongo.db.ratings.find()
	data = []
	
        # Find all queries in login collection
	for item in ratings:
		data.append({'_id' : str(item['_id']), 'contentId' : str(item['contentId']), 'userId' : str(item['userId']), 'score' : item['score']})

	return json.dumps(data, indent=4, default=json_util.default)
		
@app.route('/ratings/<id>')
def rating(id):
	rating = mongo.db.ratings.find_one({'_id': ObjectId(id)})
	
	if rating:

		data = []

		data.append({'_id' : str(rating['_id']), 'contentId' : str(rating['contentId']), 'userId' : str(rating['userId']), 'score' : rating['score']})

		return json.dumps(data, indent=4, default=json_util.default)
	else:
		return not_found()

@app.route('/ratings', methods=['PUT'])
def update_rating():
	_json = request.json
	_id = _json['_id']
	_score = _json['score']		
	# validate the received values

	if _id and _score and request.method == 'PUT':

		filter = { '_id': ObjectId(_id) }	
		values = { "$set": { 'score': _score } }

		# save edits
		mongo.db.ratings.update_one(filter, values)
		resp = jsonify(str(_id) + ' - rating updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/ratings/<id>', methods=['DELETE'])
def delete_rating(id):
	mongo.db.ratings.delete_one({'_id': ObjectId(id)})
	resp = jsonify(str(id) + ' - rating deleted successfully!')
	resp.status_code = 200
	return resp
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
