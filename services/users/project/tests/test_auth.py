# services/users/project/tests/test_auth.py

import json

from project import db
from project.api.models import User
from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    pass