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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        category = Category.query.filter(Category.type == "science").one_or_none()        
        self.new_question = {
            'question': 'How many miles away from earth is the moon?',
            'answer': '238,900',
            'category': category,
            'difficulty': 5
        }
        
        self.new_question_missing_answer = {
            'question': 'In what year was Mike Tyson the boxer?',
            'category': 'sports',
            'difficulty': '4'
        }
        
        self.search_term = {
            'searchTerm': 'soccer'
        }
        
        self.previous_questions = {
            'previous_questions': [], 
            'quiz_category': {
                'type':'Science', 
                'id': '1'
            }
        }
        
        """ restore question used in delete test after each test """
        ali = Question.query.filter(Question.question ==
                                    "What boxer's original name is Cassius Clay?").one_or_none()        
        if ali is None:
            question = Question(
                question="What boxer's original name is Cassius Clay?",
                answer="Muhammad Ali",
                category=4,
                difficulty=1
            )
            question.insert()

        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        
    def tearDown(self):
        """Executed after reach test"""
                  
        """ Delete question used in create test after each test """
        question_to_delete = Question.query.filter(Question.question ==
                              "How many miles away from earth is the moon?")
        if question_to_delete:
            question_to_delete.delete()

    """Test GET categories"""
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200, "The status code was not 200")
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    """Test 405 delete categories"""
    def test_405_delete_categories(self):
        response = self.client().delete('/categories')
        data = json.loads(response.data)

        # Assert
        self.assertEqual(405, response.status_code)
        
    """ Test GET question"""
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200, f"Status code {response.status_code} was not expected")
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) <= 10 and len(data['questions']) > 0)
        self.assertTrue(data['total_questions'])
            
    """ Test 404 invalid page number"""
    def test_404_questions_page_not_found(self):
        response = self.client().get('/questions/page=4000')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    """ Test to make sure we can delete an existing question """
    def test_delete_question(self):
        question = Question.query.filter(Question.question == "What boxer's original name is Cassius Clay?").one_or_none()
        self.assertIsNotNone(
            question, "please make sure the question exists before testing delete")        
        question_id = str(question.id)
        response = self.client().delete(f'questions/{question_id}')
        data = json.loads(response.data)
        question = Question.query.get(question.id)
        
        # Assert
        self.assertIsNone(question)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], int(question_id))

    
    """ Test to make sure we get 404 when trying to delete a question
        that doesn't exist. """
    def test_404_no_question_to_delete(self):
        book = Question.query.get(50000)
        self.assertIsNone(book)

        response = self.client().delete('questions/50000')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
    
    """ Test that can create a question"""
    def test_create_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        my_new_question = Question.query.filter(Question.question == self.new_question['question']).one_or_none()
        
        # Assert
        self.assertTrue(data['success'], "the success result was False")
        self.assertEqual(self.new_question['question'], my_new_question.question)


    """ Test that we get a 422 (unprocessable entity) when trying to create a question with missing answer """
    def test_422_create_question_missing_answer(self):
        response = self.client().post('/questions', json=self.new_question_missing_answer)
        data = json.loads(response.data)

        self.assertFalse(data['success'], "The success result was True")
        self.assertEqual(422, response.status_code)
       
       
    """ Test that we get correct questions after entering a search term"""
    def test_search_question(self):
        filtered_questions = Question.query.filter(Question.question.ilike(f"%{self.search_term['searchTerm']}%")).all()

        response = self.client().post('/questions/search_results', json=self.search_term)
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'], "The success result was False")
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(filtered_questions), data['total_questions'])
        
        
    """ Test that we get 422 (unprocessable entity) if search term is None"""
    def test_422_search_term_none(self):        
        response = self.client().post('/questions/search_results',
                                      json={'wrong_key': 'test'})
        data = json.loads(response.data)

        self.assertEqual(422, response.status_code)
        self.assertFalse(data['success'], "The success result was True")        
        
    
    """ Test that quizes only returns questions not seen before """
    def test_quizzes(self):
        
        myCategory = Category.query.filter(
            Category.type == 'Art').one_or_none()
        gogh_questions = Question.query.filter(Question.question.ilike('%'+ 'gogh' +'%')).all()
        question_ids = [question.id for question in gogh_questions]        
        all_questions = Question.query.all()
        
        response = self.client().post(f'quizzes', json={
            "previous_questions": question_ids, "quiz_category": {"type": "Art", "id": str(myCategory.id)}})
        data = json.loads(response.data)
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])
        self.assertTrue(str(data['question']['id']) not in gogh_questions)
        
    
    """ Test that we get questions by category"""
    def test_questions_by_category(self):
        sports = Category.query.filter(Category.type == 'Sports').one_or_none()
        
        response = self.client().get(f'/categories/{sports.id}/questions')
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'], "The success result was False")
        self.assertTrue(len(data['questions']))
        
        
    
    """ Test that we get a 404 (method not found) when trying to get questions with
    providing a wrong categoryid """
    def test_404_questions_wrong_category_id(self):
        response = self.client().get('/categories/998/questions',
                                      json=self.new_question_missing_answer)
        data = json.loads(response.data)

        self.assertFalse(data['success'], "The success result was True")
        self.assertEqual(404, response.status_code)
    
                
    # helper methods
        
    
    #nice SELF.SEARCHQUESTION SEARCH_ANSWER, DIFFICULT


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
