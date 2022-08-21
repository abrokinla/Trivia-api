import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func
from models import db, setup_db, Category, Question


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# PAGINATE FUNCTION
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
    
    

    # CORS HEADERS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # AFTER_REQUEST HEADERS
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

    # FETCH QUESTIONS ENDPOINT
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
        
    # DELETE QUESTION ENDPOINT
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

    
    # CREATE QUESTIONS ENDPOINT
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
    
    # SEARCH FOR QUESTIONS ENDPOINT

    @app.route('/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm', None)
            question_query= Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
            formatted_result =  paginate_questions(request, question_query)
            # categories = Category.query.all() #query the database to fetch all available categories
            # formatted_category = {Category.id:Category.type for Category in categories}#format the fetched records
            
            if len(formatted_result)==0:
                abort(404)
                
            
            return jsonify({
                'success':True,
                'questions':formatted_result,
                'total_questions':len(formatted_result)
                
            })

        except:
            abort(404)

    # FETCH QUESTIONS BY CATEGORY ID ENDPOINT
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

    # PLAY QUIZ ENDPOINT.
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        prev_quest = body.get('previous_questions')

        try:
            if (quiz_category['id'] == 0):
                question_query = Question.query.filter(Question.id.notin_(prev_quest)).all()
                question = paginate_questions(request, question_query)
                rndIndex = random.randint(0, len(question)-1)
                next_quest = question[rndIndex]
                return jsonify({
                    'success': True,
                    'NextQuestions': next_quest
                })
            else:
                question_query = Question.query.filter(Question.category==quiz_category["id"]).filter(Question.id.notin_(prev_quest)).all()
                question = paginate_questions(request, question_query)
                rndIndex = random.randint(0, len(question)-1)
                next_quest = question[rndIndex]
                return jsonify({
                    'success': True,
                    'nextQuestions': next_quest
                })
        except:            
            abort(404)

#ERROR HANDLERS

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
                }), 404
        

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
                }),422
            
        

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
            }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 405, 
            "message": "Method Not Allowed"
            }), 405
    

    return app

