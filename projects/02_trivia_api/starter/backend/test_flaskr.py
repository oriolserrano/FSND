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
    def test_get_categories(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        # in the main page the current_category has the value none, so we check if the key exists
        self.assertTrue("current_category" in data.keys())

    def test_get_questions_of_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_insert_question(self):
        question_value = "Who whon the golden ball in 2021?"
        answer_value = "Messi"
        category_value = '6'
        difficutly_value = 6
        new_question = {"question": question_value,
                        "answer": answer_value,
                        "category": category_value,
                        'difficutly': difficutly_value}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)
        pass

    def test_delete_question(self):
        question_id = 100000
        question = Question(question="q1", answer="a1", category=1, difficulty=3)
        # The id is not in the initialize method, so we add it later
        question.id = question_id
        question.insert()
        res = self.client().delete("/questions/100000")
        data = json.loads(res.data)
        question_deleted = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question_deleted, None)

    def test_get_book_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "title"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 2)
        # in the main page the current_category has the value none, so we check if the key exists
        self.assertTrue("current_category" in data.keys())

    def test_quiz_questions(self):
        res = self.client().post('/quizzes', json={"previous_questions": "",
                                                   "quiz_category": {
                                                       "type": "Geography",
                                                       "id": "3"}
                                                   })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_quiz_final_question(self):
        res = self.client().post('/quizzes', json={"previous_questions": [1,2,3],
                                                   "quiz_category": {
                                                       "type": "Science",
                                                       "id": "1"}
                                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], None) 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()