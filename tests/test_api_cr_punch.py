from re import match
from time import sleep

from tests import *


def test_api_create_punch_success(app, client):
    """Punch creation API success tests."""

    # Dummy user creation
    api_dummy_user(app, client)

    # Punching IN
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            user_id=1,
            punch_type="in",
        ),
    )
    assert 200 == r.status_code
    assert "create" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert "User (id=1) punch(es) created successfully" == r.json["message"]

    # Punching OUT
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            user_id=1,
            punch_type="out",
        ),
    )
    assert 200 == r.status_code
    assert "create" == r.json["action"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )
    assert "user_id=1" == r.json["target"]
    assert "User (id=1) punch(es) created successfully" == r.json["message"]


def test_api_create_punch_fail(app, client):
    """Punch creation API fail tests."""

    # Creating dummy punch
    api_dummy_punch(app, client)

    # Fail punching non existing user
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            user_id=666,
            punch_type="out",
        ),
    )
    assert 400 == r.status_code
    assert "User (id=666) does not exist!" == r.json["message"]

    # Missing attribute (user_id)
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            punch_type="out",
        ),
    )
    assert 400 == r.status_code
    assert (
        "JSON must contain the following attributes: user_id; punch_type(in/out); | Missing attribute: 'user_id'"
        == r.json["message"]
    )

    # Missing attribute (punch_type)
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            user_id=666,
        ),
    )
    assert 400 == r.status_code
    assert (
        "JSON must contain the following attributes: user_id; punch_type(in/out); | Missing attribute: 'punch_type'"
        == r.json["message"]
    )

    # Wrong punch_type
    r = post(
        client,
        path="/api/new/punch",
        json=dict(
            user_id=1,
            punch_type="wrong",
        ),
    )
    assert 400 == r.status_code
    assert (
        "JSON must contain the following attributes: user_id; punch_type(in/out); | Missing attribute: 'punch_type must be either in or out'"
        == r.json["message"]
    )


def test_get_users_punches(app, client):
    """Testing /api/get/punches/user path."""

    api_dummy_user(app, client, "32165498700", "Jesse Pinkman", "jesse@crystalz.org")
    api_dummy_punch(app, client, 1, "in")
    sleep(2)
    api_dummy_punch(app, client, 1, "out")
    api_dummy_punch(app, client, 1, "in")
    sleep(3)
    api_dummy_punch(app, client, 1, "out")
    r = get(client, "/api/get/punches/user/1")
    assert 200 == r.status_code
    assert 5 == r.json["total_time"]
    assert "1" == r.json["punches"][0]["id"]
    assert "1" == r.json["punches"][0]["user_id"]
    assert "in" == r.json["punches"][0]["punch_type"]
    assert "2" == r.json["punches"][1]["id"]
    assert "1" == r.json["punches"][1]["user_id"]
    assert "out" == r.json["punches"][1]["punch_type"]
