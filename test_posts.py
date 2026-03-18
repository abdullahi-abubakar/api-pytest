"""
test_posts.py — CRUD tests for the /posts endpoint.
Target: https://jsonplaceholder.typicode.com  (swap BASE_URL for your real API)
"""

import pytest


class TestGetPosts:
    """GET /posts — list and single-resource reads."""

    def test_list_posts_status_200(self, api_client, url):
        """Endpoint returns HTTP 200."""
        resp = api_client.get(url("/posts"), timeout=api_client.default_timeout)
        assert resp.status_code == 200

    def test_list_posts_returns_json_array(self, api_client, url):
        """Response body is a non-empty JSON array."""
        resp = api_client.get(url("/posts"), timeout=api_client.default_timeout)
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_list_posts_item_schema(self, api_client, url):
        """Each post has the expected keys with correct types."""
        resp = api_client.get(url("/posts"), timeout=api_client.default_timeout)
        post = resp.json()[0]
        assert "id"     in post and isinstance(post["id"],     int)
        assert "userId" in post and isinstance(post["userId"], int)
        assert "title"  in post and isinstance(post["title"],  str)
        assert "body"   in post and isinstance(post["body"],   str)

    def test_get_single_post(self, api_client, url):
        """GET /posts/{id} returns the correct resource."""
        resp = api_client.get(url("/posts/1"), timeout=api_client.default_timeout)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1

    def test_get_nonexistent_post_404(self, api_client, url):
        """Requesting a missing resource returns 404."""
        resp = api_client.get(url("/posts/99999"), timeout=api_client.default_timeout)
        assert resp.status_code == 404

    @pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
    def test_parametrized_post_ids(self, api_client, url, post_id):
        """Multiple post IDs all return 200 with matching id field."""
        resp = api_client.get(url(f"/posts/{post_id}"), timeout=api_client.default_timeout)
        assert resp.status_code == 200
        assert resp.json()["id"] == post_id

    def test_response_time_under_threshold(self, api_client, url):
        """Response time for a single post is under 2 seconds."""
        resp = api_client.get(url("/posts/1"), timeout=api_client.default_timeout)
        assert resp.elapsed.total_seconds() < 2.0, (
            f"Slow response: {resp.elapsed.total_seconds():.2f}s"
        )

    def test_content_type_header(self, api_client, url):
        """Response Content-Type includes 'application/json'."""
        resp = api_client.get(url("/posts/1"), timeout=api_client.default_timeout)
        assert "application/json" in resp.headers.get("Content-Type", "")
    
    def test_get_single_post(self, api_client, url):
        resp = api_client.get(url("/posts/7"), timeout=api_client.default_timeout)
        
        # Add a print statement to see the JSON
        print("\nAPI RESPONSE:", resp.json()) 
        
        assert resp.status_code == 200


class TestCreatePost:
    """POST /posts — resource creation."""

    def test_create_post_returns_201(self, api_client, url, new_post_payload):
        """Creating a post returns HTTP 201."""
        resp = api_client.post(
            url("/posts"),
            json=new_post_payload,
            timeout=api_client.default_timeout,
        )
        assert resp.status_code == 201

    def test_create_post_response_includes_id(self, api_client, url, new_post_payload):
        """Server assigns an id to the new resource."""
        resp = api_client.post(
            url("/posts"),
            json=new_post_payload,
            timeout=api_client.default_timeout,
        )
        data = resp.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_post_echoes_payload(self, api_client, url, new_post_payload):
        """Response body reflects the submitted fields."""
        resp = api_client.post(
            url("/posts"),
            json=new_post_payload,
            timeout=api_client.default_timeout,
        )
        data = resp.json()
        assert data["title"]  == new_post_payload["title"]
        assert data["body"]   == new_post_payload["body"]
        assert data["userId"] == new_post_payload["userId"]

    def test_create_post_missing_title_handled(self, api_client, url):
        """Submitting without a title still gets a server response (no 5xx crash)."""
        resp = api_client.post(
            url("/posts"),
            json={"body": "no title", "userId": 1},
            timeout=api_client.default_timeout,
        )
        # Adjust assertion to match your API's validation behaviour
        assert resp.status_code in (201, 400, 422)


class TestUpdatePost:
    """PUT/PATCH /posts/{id} — updates."""

    def test_put_updates_post(self, api_client, url, new_post_payload):
        """Full PUT replace returns 200 with updated data."""
        resp = api_client.put(
            url("/posts/1"),
            json={**new_post_payload, "id": 1},
            timeout=api_client.default_timeout,
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == new_post_payload["title"]

    def test_patch_updates_title_only(self, api_client, url):
        """PATCH with partial payload returns 200."""
        resp = api_client.patch(
            url("/posts/1"),
            json={"title": "Patched by CI"},
            timeout=api_client.default_timeout,
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Patched by CI"


class TestDeletePost:
    """DELETE /posts/{id}."""

    def test_delete_post_returns_200(self, api_client, url):
        """Deleting an existing resource returns 200 (or 204)."""
        resp = api_client.delete(url("/posts/1"), timeout=api_client.default_timeout)
        assert resp.status_code in (200, 204)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
