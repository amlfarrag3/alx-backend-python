#!/usr/bin/env python3
""" unittest of client module functions """
import unittest
from typing import Dict, List, Mapping
from unittest.mock import patch, Mock, PropertyMock, create_autospec
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ class to test client functions
        inside class
    """
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, name: str, mock_get: Mock):
        """ method that test org method in GithubOrgClient class """
        test_class: GithubOrgClient = GithubOrgClient(name)
        test_class.org()
        mock_get.assert_called_once_with(
            'https://api.github.com/orgs/{}'.format(name))

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_prop: PropertyMock):
        """ test method public repo url"""
        mock_prop.return_value = {'repos_url': 'pla'}
        call_class: GithubOrgClient = GithubOrgClient("pla")
        result: str = call_class._public_repos_url
        self.assertEqual(result, 'pla')

    @patch('client.get_json')
    def test_public_repos(self, mock_get: Mock):
        """ test public repos attribute"""
        mock_get.return_value: List = [{'name': 'a', 'license': None}]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value: str = 'pla'
            test_class: GithubOrgClient = GithubOrgClient('pla')
            result: List = test_class.public_repos()
            mock_url.assert_called_once()
            self.assertEqual(result, ['a'])
        mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Mapping, key: str, expected: bool):
        """ test has license method """
        mock_func = create_autospec(GithubOrgClient.has_license)
        mock_func.return_value = expected
        result: bool = mock_func(repo, key)
        self.assertEqual(result, expected)
        mock_func.assert_called_once_with(repo, key)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ integration test for whole class in client file """
    @classmethod
    def setUpClass(cls):
        """set up all requirements needed fot tests"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload)),
        ]
        cls.test_class = GithubOrgClient('pla')

    def test_public_repos(self):
        """ test public repo method """
        result: List = self.test_class.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """ test public repo method with check license """
        result: List = self.test_class.public_repos("apache-2.0")
        self.assertEqual(result, self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """ tear down all setups in first of test """
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
