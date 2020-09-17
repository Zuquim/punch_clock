from re import match

from tests import *


def test_api_create_user_success(app, client):
    """User creation API success tests."""

    # User creation
    r = post(
        client,
        path="/api/new/user",
        json=dict(
            full_name="Jesse Pinkman",
            cpf="12345678900",
            email="blue@crystalz.org",
        ),
    )
    assert 201 == r.status_code
    assert "create" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert (
        "User (full_name='Jesse Pinkman'; cpf=12345678900; email=blue@crystalz.org) created successfully"
        == r.json["message"]
    )


def test_api_create_user_fail(app, client):
    """User creation API fail tests."""

    # Creating dummy user
    api_dummy_user(app, client)

    # Fail creating existing user
    r = post(
        client,
        path="/api/new/user",
        json=dict(
            full_name="Jesse Pinkman",
            cpf="12345678900",
            email="blue@crystalz.org",
        ),
    )
    assert 200 == r.status_code
    assert f") already exists!" in r.json["message"]


def test_api_update_user_success(app, client):
    """User update API success tests."""

    # Making test user
    api_dummy_user(app, client)
    api_dummy_user(app, client, "32165498700", "Saul Goodman", "saul@bettercall.org")

    # Updating user full_name and email
    r = post(
        client,
        path="/api/update/user",
        json=dict(
            user_id=1,
            full_name="Walter White",
            email="heisenberg@crystalz.org",
        ),
    )
    assert 200 == r.status_code
    assert "update" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert (
        "User (full_name='Walter White'; cpf=12345678900; email=heisenberg@crystalz.org) updated successfully"
        == r.json["message"]
    )

    # Updating user cpf
    r = post(
        client,
        path="/api/update/user",
        json=dict(
            user_id=1,
            cpf="65498732100",
        ),
    )
    assert 200 == r.status_code
    assert "update" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert (
        "User (full_name='Walter White'; cpf=65498732100; email=heisenberg@crystalz.org) updated successfully"
        == r.json["message"]
    )

    # Updating all user attributes
    r = post(
        client,
        path="/api/update/user",
        json=dict(
            user_id=1,
            full_name="Jesse Pinkman",
            cpf="98732165400",
            email="blue@crystalz.org",
        ),
    )
    assert 200 == r.status_code
    assert "update" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert (
        "User (full_name='Jesse Pinkman'; cpf=98732165400; email=blue@crystalz.org) updated successfully"
        == r.json["message"]
    )


def test_api_update_user_fail(app, client):
    """User update API fail tests."""

    # Making test user
    api_dummy_user(app, client, email="foo@bar.com")

    # Fail missing essential attribute
    r = post(
        client,
        path="/api/update/user",
        json=dict(
            full_name="Jesse Pinkman",
            cpf="12378965400",
            email="blue@glass.org",
        ),
    )
    assert 400 == r.status_code
    assert (
        "JSON must contain the following attribute: user_id | Optionally it may also contain: cpf, email, full_name"
        == r.json["message"]
    )

    # Fail updating non existing user
    r = post(
        client,
        path="/api/update/user",
        json=dict(
            user_id=666,
            full_name="Jesse Pinkman",
            cpf="12378965400",
            email="blue@glass.org",
        ),
    )
    assert 205 == r.status_code
    assert "User (id=666) does not exist!" == r.json["message"]


def test_get_user(app, client):
    """Testing /api/list/users path."""

    api_dummy_user(app, client, "32165498700", "Jesse Pinkman", "jesse@crystalz.org")
    r = get(client, "/api/get/user/1")
    assert 200 == r.status_code
    exp = {
        "user": {
            "id": 1,
            "full_name": "Jesse Pinkman",
            "cpf": "32165498700",
            "email": "jesse@crystalz.org",
        }
    }
    assert "1" == r.json["user"]["id"]
    assert "Jesse Pinkman" == r.json["user"]["full_name"]
    assert "32165498700" == r.json["user"]["cpf"]
    assert "jesse@crystalz.org" == r.json["user"]["email"]
