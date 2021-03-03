import unittest
from project_creator import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.expected_username_repo = "username/repo"

    def test_repo_url_convert_full_git(self):
        url = "https://github.com/username/repo.git"
        username_repo = main.convert_repo_url(url)
        self.assertEqual(username_repo, self.expected_username_repo)

    def test_repo_url_convert_full(self):
        url = "https://github.com/username/repo"
        username_repo = main.convert_repo_url(url)
        self.assertEqual(username_repo, self.expected_username_repo)

    def test_repo_url_convert(self):
        url = "username/repo"
        username_repo = main.convert_repo_url(url)
        self.assertEqual(username_repo, self.expected_username_repo)
