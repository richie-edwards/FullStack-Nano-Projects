import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Initializing CORS with the app
    '''
    CORS(app)

    '''
    Using the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')

        return response

    '''
    Pagination function that returns the correct amount
    of books per page in the expected format based on the
    model's format function.
    '''
    def paginate_questions(request, questions):
        formatted_questions = [question.format() for question in questions]
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return formatted_questions[start:end]

    '''
    GET request that returns all available categories
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        return jsonify({
            "success": True,
            "categories": {
                category.id: category.type for category in categories
            },
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.all()

        if(len(paginate_questions(request, questions)) == 0):
            abort(404)

        return jsonify({
            "success": True,
            "questions": paginate_questions(request, questions),
            "total_questions": len(questions),
            "categories": {
                category.id: category.type for category in categories
            },
            "current_category": "hard coded category"
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        try:
            question.delete()
            questions = Question.query.order_by(Question.id).all()
            
            return jsonify({
            "success": True,
            "deleted": question.id,
            "questions": paginate_questions(request, questions),
            "total_questions": len(questions)
            })

        except:
            abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end
    of the last page of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        if ('question' not in data
            or 'answer' not in data
            or 'category' not in data
            or 'difficulty' not in data):
                abort(422)

        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')

        try:
            question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            question.insert()
        except:
            abort(422)  # unprocessable entity

        return jsonify({
            "success": True
        })

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search_results', methods=['POST'])
    def search_questions():        
        data = request.get_json()        
        search_term = data.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "total_questions": len(questions),
            "current_category": ''
        })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        available_categories = Category.query.filter(
            Category.id == category_id).all()
        questions = []
        if len(available_categories) == 0:
            print(category_id, available_categories)
            abort(404)

        questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()

        return jsonify({
            "success": True,
            "questions": paginate_questions(request, questions)
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            body = request.get_json()
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            questions = []
            valid_questions = []
            result = valid_questions

            if category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category['id'])

            for question in questions:
                if question.id not in previous_questions:
                    valid_questions.append(question)

            # Force end of quiz if no more questions.
            # Send random question if more than 1 remain
            total_valid_questions = len(valid_questions)
            if total_valid_questions == 0:
                result = None
            elif total_valid_questions > 1:
                result = valid_questions[random.randrange(
                    0, len(valid_questions)-1, 1)].format()
            elif total_valid_questions == 1:
                result = valid_questions[0].format()

            return jsonify({
                "success": True,
                "question": result
            })
        except:
            abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
        
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    return app
