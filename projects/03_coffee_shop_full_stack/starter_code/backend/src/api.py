import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
#Token1
#eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklOdm5oZjZHSDNpc0dRc1JYTUdkaCJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdDNob2gxYi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFlYjFiM2JhM2NmMjUwMDY4YjhhYWNlIiwiYXVkIjoiY29mZWVzaG9wIiwiaWF0IjoxNjQyNzk3ODg3LCJleHAiOjE2NDI4MDUwODcsImF6cCI6IkNtRERTamt1YlA3VlV3R3JuMmJ5ZGM1RjVkNXNXTjUyIiwic2NvcGUiOiIifQ.6g39QeoZt1esnlVvNHOLV5FpaLlz2Ed_9twh9IXAqRc6PY1G7-SkMZ2wWidyaGJJmTwx232ssi6bwOAmJyFmKm8W2wRvaaHED_J9LYao5oBL2ie3r_ZCVmYnvFn14YU390R_KNUnP4f3xnKSMc0g9Rlz5ONc6BGyruRKxQkkRYMRzlSOrACZGGZ78-uqV1lYCva9ovuWULWdLIMa6_phXcwcAoNs0qudNxlWb0ZS9zCSUnukWBAh6GU7LP8XyEwP3zYjV2RAKqU0oY1myK8PBrBik9VC3mpztDbr4um4GnWD44O07i2gYimFYrK8KwK8IcMgMJcqn_ntgFiT2z44Vw
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint

    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.order_by(Drink.id).all()]
        
        if len(drinks) == 0:
            abort(400)
        
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except:
        abort(422)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail", methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_deail(payload):

    try:
        drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]

        if len(drinks) == 0:
            abort(400)
 
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except:
        abort(422)
     

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        data = request.get_json()
        #new_recipe is a python object, so we have to use json.dumps to parse it to a JSON string
        new_recipe = json.dumps(data['recipe'])
        new_title = data['title']
        
        new_drink = Drink(recipe=new_recipe, title=new_title)

        new_drink.insert()
        
        return jsonify({
            'success': True,
            'drinks': new_drink.long()
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        data = request.get_json()
        new_recipe = json.dumps(data['recipe'])
        new_title = data['title']
        print(data)
        print(id)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        print(drink.id)
        drink.recipe = new_recipe
        drink.title = new_title
        drink.update()
        
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()
        
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(422)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
