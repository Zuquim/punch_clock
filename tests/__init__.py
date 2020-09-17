from typing import Optional

import pytest

from app import create_app


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def get(
    client,
    path: str,
    follow_redirects: bool = True,
    **kwargs,
):
    return client.get(path, follow_redirects=follow_redirects)


def post(
    client,
    path: str,
    data: Optional[dict] = None,
    json: Optional[dict] = None,
    follow_redirects: bool = True,
    **kwargs,
):
    return client.post(path, data=data, json=json, follow_redirects=follow_redirects)


def api_dummy_user(
    app,
    client,
    cpf: str = "12345678900",
    full_name: str = "Foo Bar",
    email: str = "foo@bar.com",
):
    """Create dummy user to use in tests."""

    # Making test user
    return post(
        client,
        path="/api/new/user",
        json=dict(
            cpf=cpf,
            full_name=full_name,
            email=email,
        ),
    )


def api_dummy_punch(app, client, user_id: int = 1, punch_type: str = "in"):
    """Create dummy punch to use in tests."""

    # Making test punch
    return post(
        client, path="/api/new/punch", json=dict(user_id=user_id, punch_type=punch_type)
    )
