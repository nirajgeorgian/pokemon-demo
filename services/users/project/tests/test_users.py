# services/users/project/tests/test_users.py

import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensures the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensures a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                "/users",
                data = json.dumps({
                    'username': 'dodo',
                    'email': 'dodo@example.com',
                    'password': 'greaterthaneight'
                }),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('dodo@example.com successfully signed up!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users",
                data = json.dumps({}),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post( '/users',
                data=json.dumps({'email': 'dodo@example.com', 'password': 'random'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'dodo',
                    'email': 'dodo@example.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'dodo',
                    'email': 'dodo@example.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/dodo')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('dodo', 'dodo@example.com', 'greaterthaneight')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('dodo', data['data']['username'])
            self.assertIn('dodo@example.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensures error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            response = self.client.post(
            '/users',
            data = json.dumps(dict(
                    username='test',
                    email='test@test.com')),
                    content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('dodo', 'dodo@example.com', 'greaterthaneight')
        add_user('duck', 'duck@example.com', 'greaterthaneight')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('dodo', data['data']['users'][0]['username'])
            self.assertIn('dodo@example.com', data['data']['users'][0]['email'])
            self.assertIn('duck', data['data']['users'][1]['username'])
            self.assertIn('duck@example.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()