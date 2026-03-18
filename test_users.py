"""
test_users.py — Tests for /users endpoint (read-only resource).
"""


class TestGetUsers:

    def test_list_users_200(self, api_client, url):
        resp = api_client.get(url("/users"), timeout=api_client.default_timeout)
        assert resp.status_code == 200

    def test_user_schema(self, api_client, url):
        """Spot-check nested address and company fields."""
        resp = api_client.get(url("/users/1"), timeout=api_client.default_timeout)
        user = resp.json()
        assert "name"    in user
        assert "email"   in user
        assert "address" in user and "city"    in user["address"]
        assert "company" in user and "name"    in user["company"]

    def test_user_email_format(self, api_client, url):
        """All user emails contain '@'."""
        resp = api_client.get(url("/users"), timeout=api_client.default_timeout)
        for user in resp.json():
            assert "@" in user["email"], f"Bad email for user {user['id']}: {user['email']}"

    def test_users_by_query_param(self, api_client, url):
        """Filter by userId query param returns only matching records."""
        resp = api_client.get(
            url("/posts"),
            params={"userId": 1},
            timeout=api_client.default_timeout,
        )
        assert resp.status_code == 200
        posts = resp.json()
        assert all(p["userId"] == 1 for p in posts), "Filtering by userId returned wrong records"