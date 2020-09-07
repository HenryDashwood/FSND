import json
import unittest
from models import Movies, Actors
from app import create_app
from flask_sqlalchemy import SQLAlchemy


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client

        self.new_movie = {
            "title": "test title",
            "release_date": "1995-09-14"
        }

        self.updated_movie = {
            "title": "updated test title",
            "release_date": "1995-09-14"
        }

        self.new_actor = {
            "name": "Henry Dashwood",
            "age": 24,
            "gender": "male"
        }

        self.updated_actor = {
            "name": "Henry Dashwood",
            "age": 25,
            "gender": "male"
        }

        self.executive_producer = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzNmM4MTM1YjQ2ODAwMTNhYmI2ZWYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NTA1NjU1LCJleHAiOjE1OTk1MTI4NTUsImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.DYcG5UJxlf-OcEjq4vQWE4fzUfVHG_wu3EJRcoyaGuaCmYwFQS5lgdbeHpsu_u-efjqP2rx4Y3PUXHth6mBLEC668-XkHtvRpbMkRIUMmsFW3qNUdk3EoxrCVy8Ln9XCl-YQxoQxBIqpNCg24soXG5_y1ooK7Pv_7LcpANf1pxlSZFgdNp5Vv4pNIJ977AdyPk77hZbucX1Cv9stxZ3YyLtd6Ly7soE21EQWSCe3xn3lq1U_9uzBmC7PM5ybX4fyew75XjYquTmPTMvCylzIo088miwpfwee0oCcs68ZNGH-OajZl6cZ9hLXBFIGrD5QjN56y7LfZihqAkcyMm-z1Q'
        }

        self.casting_director = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzNmM4MTM1YjQ2ODAwMTNhYmI2ZWYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NTA1NjU1LCJleHAiOjE1OTk1MTI4NTUsImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.DYcG5UJxlf-OcEjq4vQWE4fzUfVHG_wu3EJRcoyaGuaCmYwFQS5lgdbeHpsu_u-efjqP2rx4Y3PUXHth6mBLEC668-XkHtvRpbMkRIUMmsFW3qNUdk3EoxrCVy8Ln9XCl-YQxoQxBIqpNCg24soXG5_y1ooK7Pv_7LcpANf1pxlSZFgdNp5Vv4pNIJ977AdyPk77hZbucX1Cv9stxZ3YyLtd6Ly7soE21EQWSCe3xn3lq1U_9uzBmC7PM5ybX4fyew75XjYquTmPTMvCylzIo088miwpfwee0oCcs68ZNGH-OajZl6cZ9hLXBFIGrD5QjN56y7LfZihqAkcyMm-z1Q'
        }

        self.casting_assistant = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzNmM4MTM1YjQ2ODAwMTNhYmI2ZWYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NTA1NjU1LCJleHAiOjE1OTk1MTI4NTUsImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.DYcG5UJxlf-OcEjq4vQWE4fzUfVHG_wu3EJRcoyaGuaCmYwFQS5lgdbeHpsu_u-efjqP2rx4Y3PUXHth6mBLEC668-XkHtvRpbMkRIUMmsFW3qNUdk3EoxrCVy8Ln9XCl-YQxoQxBIqpNCg24soXG5_y1ooK7Pv_7LcpANf1pxlSZFgdNp5Vv4pNIJ977AdyPk77hZbucX1Cv9stxZ3YyLtd6Ly7soE21EQWSCe3xn3lq1U_9uzBmC7PM5ybX4fyew75XjYquTmPTMvCylzIo088miwpfwee0oCcs68ZNGH-OajZl6cZ9hLXBFIGrD5QjN56y7LfZihqAkcyMm-z1Q'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_create_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie(self):
        res = self.client().patch(
            f"/movies/1",
            json=self.updated_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        res = self.client().delete(
            f"/movies/{data['movie']['id']}",
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_get_actor(self):
        res = self.client().get(
            '/actors',
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_update_actor(self):
        res = self.client().patch(
            f"/actors/1",
            json=self.updated_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        res = self.client().delete(
            f"/actors/{data['actor']['id']}",
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_rbac_no_headers(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 500)

    def test_rbac_fail_wrong_permissions(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.casting_assi
        )
        self.assertEqual(res.status_code, 500)

    def test_404(self):
        res = self.client().get(
            '/nonexistent',
            headers=self.executive_producer
        )
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
