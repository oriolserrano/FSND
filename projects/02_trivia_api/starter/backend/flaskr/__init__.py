import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import and_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    [x] TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    [x]TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
    [x]TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.order_by(Category.id).all()
        format_categories = {category.id: category.type for category in categories}
        return jsonify({
          'success': True,
          'categories': format_categories
        })

    '''
    [x]TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions', methods=['GET'])
    def get_question():
        questions = Question.query.order_by(Question.id).all()
        paginated = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()
        format_categories = {category.id: category.type for category in categories}
        if len(questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': paginated,
          'categories': format_categories,
          'total_questions': Question.query.count(),
          'current_category': None, 
        })

    '''
    [x]TODO:
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True
            })

        except:
            abort(422)
            
    '''
    [x]TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        new_answer = data.get("answer", None)
        new_category = data.get("category", None)
        new_difficult = data.get("difficulty", None)
        new_question = data.get("question", None)
        new_answer = data.get("answer", None)
        search = data.get('searchTerm', None)
        try:
            if search:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
                questions_formatted = [question.format() for question in questions]
                
                if len(questions) == 0:
                    abort(404)
                return jsonify({
                  'success': True,
                  'questions': questions_formatted,
                  'total_questions': len(questions_formatted),
                  'current_category': None,
                })

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficult)
                question.insert()
                
                return jsonify({
                  'success': True
                })

        except:
            abort(422)

    '''
    [x]TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    [x]TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_category(category_id):
        questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
        questions_formatted = [question.format() for question in questions]
        current_category = Category.query.get(category_id).format()
        
        if len(questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': questions_formatted,
          'total_questions': len(questions_formatted),
          'current_category': current_category
        })

    '''
    [x]TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        data = request.get_json()
        previous_questions = data.get("previous_questions", None)
        quiz_category = data.get("quiz_category", None)
        category_id = quiz_category['id']
        total_questions_category = Question.query.filter(Question.category == category_id).count()

        if len(previous_questions) != total_questions_category:
            questions = Question.query.filter(and_(Question.category == category_id, Question.id.notin_(previous_questions))).order_by(Question.id).first().format()
        else:
            questions = None
        
        return jsonify({
            'success': True,
            'question': questions
        })

    '''
    [x]TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404,
                     "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
                     "error": 422,
                     "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False,
                        "error": 400,
                        "message": "bad request"}), 400)
    
    return app

    