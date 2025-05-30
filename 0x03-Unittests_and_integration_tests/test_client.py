#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test class for GithubOrgClient.
    """

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient.

        This test mocks:
        - get_json to simulate API response with a list of repositories.
        - _public_repos_url to simulate the internal URL used for fetching repos.

        It checks that:
        - The correct list of repository names is returned.
        - The mocked get_json and _public_repos_url are each called once.
        """
        # Define mock payload returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Mock the _public_repos_url property to return a test URL
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testo
