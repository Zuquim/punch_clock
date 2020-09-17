from re import match

from tests import *


def test_root(app, client):
    """Testing root path."""

    r = get(client=client, path="/")
    assert 200 == r.status_code
    assert "/" == r.json["path"]
    assert "Punch Clock v0.1.0" == r.json["message"]
    assert match(
        "^202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9]+:[0-5][0-9]:[0-5][0-9]$",
        r.json["datetime"],
    )


def test_list_users(app, client):
    """Testing show/users path."""

    api_dummy_user(app, client, "32165498700", "Jesse Pinkman", "jesse@crystalz.org")
    api_dummy_user(
        app, client, "98763532112", "Walter White", "heisenberg@crystalz.org"
    )
    r = get(client, "/api/list/users")
    assert 200 == r.status_code
    exp = {
        "users": [
            {
                "id": 1,
                "full_name": "Jesse Pinkman",
                "cpf": "32165498700",
                "email": "jesse@crystalz.org",
            },
            {
                "id": 2,
                "full_name": "Walter White",
                "cpf": "98763532112",
                "email": "heisenberg@crystalz.org",
            },
        ]
    }
    assert "1" == r.json["users"][0]["id"]
    assert "Jesse Pinkman" == r.json["users"][0]["full_name"]
    assert "32165498700" == r.json["users"][0]["cpf"]
    assert "jesse@crystalz.org" == r.json["users"][0]["email"]
    assert "2" == r.json["users"][1]["id"]
    assert "Walter White" == r.json["users"][1]["full_name"]
    assert "98763532112" == r.json["users"][1]["cpf"]
    assert "heisenberg@crystalz.org" == r.json["users"][1]["email"]
