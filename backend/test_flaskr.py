import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:12345@localhost:5432/"+ self.database_name
                
        setup_db(self.app, self.database_path)
        self.new_question = {"question": "What is the name of the longest river?", "answer": "Nile River", "category": 2, "difficulty": 1}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # create questions relation
            class Question(self.db.Model):
                __tablename__ = 'questions'

                id = self.db.Column(self.db.Integer, primary_key=True)
                question = self.db.Column(self.db.String)
                answer = self.db.Column(self.db.String)
                category = self.db.Column(self.db.String)
                difficulty = self.db.Column(self.db.Integer)
            #create the category relation
            class Category(self.db.Model):
                __tablename__ = 'categories'

                id = self.db.Column(self.db.Integer, primary_key=True)
                type = self.db.Column(self.db.String)
    
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # CATEGORIES TEST
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    # TEST FOR PAGINATED QUESTION
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    # TEST FOR PAGINATED QUESTION FAILURE
    def test_404_paginated_questions_failure(self):
        res = self.client().get("/questions?page=9999")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"resource not found")

    # TEST FOR DELETE QUESTION ENDPOINT
    def test_delete_question(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"],5)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)

    def test_422_delete_question_failure(self):
        res = self.client().delete("/questions/9999")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"unprocessable")

    # TEST FOR NEW QUESTION CREATION
    def test_create_new_question(self):
        res = self.client().post("/questions", json = self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    def test_405_create_new_question_failure(self):
        res = self.client().post("/questions/999", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"Method Not Allowed")


#    TESTS FOR FETCH QUESTION BY CATEGORY
    def test_fetch_question_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"],2)

    def test_404_fetch_question_by_category_failure(self):
        res = self.client().get("/categories/999/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search(self):
        search = {'searchTerm': 'what', }
        result = self.client().post('/search', json=search)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)

    def test_search_not_found(self):
        search = {
            'searchTerm': 'kyjghf hjgjhv,',
        }
        result = self.client().post('/search', json=search)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],  'quiz_category':
                {
                    'id': '2', 'type': 'Art'
                }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

def test_get_quiz_Resource_not_found(self):
        res = self.client().post('/quizzes',json={
            'previous_questions': [] 
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()