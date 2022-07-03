import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func
from models import db, setup_db, Category, Question


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
    
    

    # """
    # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    # """
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # """
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    # """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response




    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # """
    @app.route('/categories')
    def fetch_categories():
        categories = Category.query.all() #query the database to fetch all available categories
        formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records
        #return a dict of fetched categories
        return jsonify({
            'success':True,
            'categories': formatted_category
            # 'category':categories.type
        })

    # """
    # @TODO:
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # """
    @app.route('/questions')
    def get_questions():
        #fetch questions
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)


        #fetch category
        categories = Category.query.all() #query the database to fetch all available categories
        formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records
        
        if len(current_questions)== 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions': current_questions,
            'total_questions':len(questions),
            'categories':formatted_category,
            
        })
        
    # """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # """
    
    # """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            # categories = Category.query.all() #query the database to fetch all available categories
            # formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records


            return jsonify({
                'success':True,
                'deleted':question_id,
                'question': current_questions,
                'total_questions':len(questions)
                # 'categories':formatted_category
            })
        except:
            abort(422)

    
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    @app.route('/questions', methods =['POST'])
    def create_questions():

        body = request.get_json()
        newQuestion = body.get('question', None)
        newAnswer = body.get('answer', None)
        newCategory =body.get('category', None)
        newDifficulty = body.get('difficulty', None)

        try:
            question = Question(question=newQuestion, answer=newAnswer, category=newCategory, \
                difficulty=newDifficulty)
            question.insert()

            questions= Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            categories = Category.query.all() #query the database to fetch all available categories
            formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records

            return jsonify({
                'success':True,
                'created':Question.id,
                'questions':current_questions,
                'total_questions':len(Question.query.all()),
                'categories': formatted_category
            })
        except:
            abort(422)
    
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.

    @app.route('/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')
            selection= db.session.query(Question).filter(Question.question.ilike('%'+search_term+'%')).all()
            
            categories = Category.query.all() #query the database to fetch all available categories
            formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records

            # result_length = len(result)
            if selection:
                formatted_result =  paginate_questions(request, selection)
            
                return jsonify({
                    'success':True,
                    'questions':formatted_result,
                    'total_questions':len(selection),
                    'categories':formatted_category,
                })

        except:
            abort(404)

    # @TODO:
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def fetch_questions_by_category(category_id):
        

        categories = Category.query.all() #query the database to fetch all available categories
        formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records
        
        
        try:
            selection = Question.query.filter(Question.category == category_id).all()
            # formatted_questions = [question.format() for question in questions]
            current_question = paginate_questions(request, selection)
            print(current_question)

            if len(current_question) == 0:
                abort(404)


            
            return jsonify({
                'success':True,
                'questions': current_question,
                'total_questions': len(selection),
                'categories':formatted_category,
                'current_category':category_id
            })

        except:
            abort(404)

    # """
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        prev_quest = body.get('previous_questions')

        try:
            if (quiz_category['id'] == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=quiz_category['id']).all()

            rndIndex = random.randint(0, len(questions)-1)
            next_quest = questions[rndIndex]
           
            while next_quest.id not in prev_quest:
                next_qstn = questions[rndIndex]
                return jsonify({
                    'success': True,
                    'question': {
                        "answer": next_qstn.answer,
                        "category": next_qstn.category,
                        "difficulty": next_qstn.difficulty,
                        "id": next_qstn.id,
                        "question": next_qstn.question
                    },
                    'previousQuestions': prev_quest
                })

        except:            
            abort(404)



    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # """

    # """
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # """
        

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}), 405
    

    return app

