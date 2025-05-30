#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit test class for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repo names"""

        # Mock get_json to return a list of repo dicts
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Mock _public_repos_url to return a specific URL
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            # Call the method under test
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Expected result
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Assert mocks were each called once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

    
        
    
