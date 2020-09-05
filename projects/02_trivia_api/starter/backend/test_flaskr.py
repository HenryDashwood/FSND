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
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
            "answer": "Maya Angelou",
            "difficulty": 2,
            "category": 4
        }

        self.search_string = {
            "searchTerm": "st question que"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_paginated_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 'Science')

    def test_404_paginated_questions_by_invalid_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_new_question(self):
        question = Question(
            question='test question question',
            answer='test question answer',
            difficulty=1,
            category=1
        )

        res = self.client().post('/questions', json=question.format())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

        self.client().delete(f"/questions/{int(data['created'])}")

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post('/questions/1000', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_delete_question(self):
        question = Question(
            question='test question question',
            answer='test question answer',
            difficulty=1,
            category=1
        )
        question.insert()
        question_id = question.id

        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == int(data['deleted'])
        ).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable')

    def test_search_questions(self):
        question = Question(
            question='test question question',
            answer='test question answer',
            difficulty=1,
            category=1
        )
        question.insert()
        question_id = question.id

        res = self.client().post('questions/search', json=self.search_string)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

        self.client().delete(f"/questions/{question_id}")

    def test_play(self):
        res = self.client().get('/categories/1/questions')
        num_questions = len(json.loads(res.data)['questions'])

        previous_questions = []
        while len(previous_questions) < num_questions:
            res = self.client().post(
                '/quizzes',
                json={
                    "previous_questions": previous_questions,
                    "quiz_category": {"id": 1, "type": "Science"}
                }
            )
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])

            previous_questions.append(
                Question.query.get(data['question']['id']).format()
            )

    def test_404_play_invalid_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [],
                "quiz_category": {"id": 100, "type": "Nonexistent"}
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_play_when_no_more_questions(self):
        previous_questions = [q.format() for q in Question.query.all()]
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": previous_questions,
                "quiz_category": {"id": 0, "type": "All"}
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
