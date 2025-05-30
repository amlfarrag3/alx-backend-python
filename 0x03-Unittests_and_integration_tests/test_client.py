#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org property.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient.org property.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Ensures get_json is called once with expected URL.
        """
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        # Clear memoize cache if needed (depends on your memoize implementation)
        if hasattr(client.org, 'cache_clear'):
            client.org.cache_clear()

        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
