"""
conftest.py — Shared fixtures and configuration for the API test suite.
Works with pytest + pytest-html for CI/CD reporting.
"""

import pytest
import requests


# ── Base URL ──────────────────────────────────────────────────────────────────
BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT  = 10


# ── Session-scoped HTTP client ─────────────────────────────────────────────────
@pytest.fixture(scope="session")
def api_client():
    """
    Reusable requests.Session for the entire test run.
    Set default headers, base URL, and timeout here.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept":       "application/json",
        # Add auth token from env if required:
        # "Authorization": f"Bearer {os.getenv('API_TOKEN', '')}",
    })
    session.base_url = BASE_URL
    session.default_timeout = TIMEOUT
    yield session
    session.close()


# ── Helper: build full URL ─────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def url(api_client):
    """Return a callable that joins base_url + path."""
    def _url(path: str) -> str:
        return f"{api_client.base_url}{path}"
    return _url


# ── Sample payload fixtures ───────────────────────────────────────────────────
@pytest.fixture
def new_post_payload():
    return {
        "title":  "CI Test Post",
        "body":   "Created by automated pytest run.",
        "userId": 1,
    }

@pytest.fixture
def new_comment_payload():
    return {
        "postId": 1,
        "name":   "CI Tester",
        "email":  "ci@example.com",
        "body":   "Automated comment from pytest.",
    }