from django.test import TestCase

# Create tests here.
from django.test import TestCase
from myapp.matching_algorithm import match_users_cosine
from django.contrib.auth.models import User
class MatchingAlgorithmTestCase(TestCase):
    def test_match_users_cosine(self):
        # Create some dummy user data
        user1 = {'id': 1, 'name': 'Alice', 'interests': ['python', 'django', 'data science']}
        user2 = {'id': 2, 'name': 'Bob', 'interests': ['java', 'spring', 'machine learning']}
        user3 = {'id': 3, 'name': 'Charlie', 'interests': ['python', 'django', 'java', 'spring']}
        user4 = {'id': 4, 'name': 'David', 'interests': ['machine learning', 'data science', 'javascript']}

        # Call the function with a user ID
        matched_users = match_users_cosine(1)

        # Check that the returned value is a list
        self.assertIsInstance(matched_users, list)

        # Check that the returned list contains the correct number of users
        self.assertEqual(len(matched_users), 3)

        # Check that the returned list contains the correct users in the correct order
        self.assertEqual(matched_users[0]['id'], 3)
        self.assertEqual(matched_users[1]['id'], 4)
        self.assertEqual(matched_users[2]['id'], 2)
