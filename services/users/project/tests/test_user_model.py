# services/users/project/tests/test_user_model.py

import unittest

from project import db
from project.api.models import User
from project.tests.utils import add_user
from project.tests.base import BaseTestCase

from sqlalchemy.exc import IntegrityError

class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'greaterthaneight')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertNotEqual(user.password, 'greaterthaneight')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com', 'greaterthaneight')
        duplicate_user = User( username='justatest', email='test2@test.com', password='greaterthaneight')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com', 'greaterthaneight')
        duplicate_user = User( username='justatest', email='test2@test.com', password='greaterthaneight')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('justatest1', 'test1@test.com', 'greaterthaneight')
        user_two = add_user('justatest2', 'test2@test.com', 'greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_to_json(self):
        user = add_user('justatest', 'test@test.com', 'greaterthaneight')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    if __name__ == '__main__':
        unittest.main()
